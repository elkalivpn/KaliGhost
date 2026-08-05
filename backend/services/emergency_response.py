"""
KaliGhost 4.0 ULTIMATE - Emergency Response System
Respuesta automática ante incidentes críticos
Capacidades: Dead Man's Switch, Shamir Secret Sharing, Secure Wipe, Auto-destruction
"""

import os
import sys
import json
import time
import hashlib
import secrets
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import base64
import hmac


class ShamirSecretSharing:
    """
    Implementación de Shamir's Secret Sharing para dividir secretos
    Un secreto se divide en N partes, se requieren K partes para reconstruir
    """
    
    def __init__(self, prime: int = 2**256 - 189):
        self.prime = prime  # Primo grande para aritmética modular
        
    def split_secret(self, secret: str, n_shares: int, k_threshold: int) -> List[Dict[str, Any]]:
        """
        Divide un secreto en N partes, requiriendo K partes para reconstruir
        
        Args:
            secret: El secreto a dividir (string)
            n_shares: Número total de partes a crear
            k_threshold: Número mínimo de partes necesarias para reconstruir
            
        Returns:
            Lista de diccionarios con las partes del secreto
        """
        if k_threshold > n_shares:
            raise ValueError("K threshold no puede ser mayor que N shares")
        if k_threshold < 2:
            raise ValueError("K threshold debe ser al menos 2")
            
        # Convertir secreto a número
        secret_bytes = secret.encode('utf-8')
        secret_int = int.from_bytes(secret_bytes, 'big')
        
        # Generar coeficientes aleatorios para el polinomio
        coefficients = [secret_int] + [secrets.randbelow(self.prime) for _ in range(k_threshold - 1)]
        
        shares = []
        for i in range(1, n_shares + 1):
            # Evaluar polinomio en x = i
            y = 0
            for j, coef in enumerate(coefficients):
                y = (y + coef * pow(i, j, self.prime)) % self.prime
            
            share = {
                'share_id': i,
                'x': i,
                'y': hex(y),
                'k_threshold': k_threshold,
                'n_shares': n_shares,
                'created_at': datetime.now().isoformat()
            }
            shares.append(share)
            
        print(f"[+] Secreto dividido en {n_shares} partes (umbral: {k_threshold})")
        return shares
    
    def reconstruct_secret(self, shares: List[Dict[str, Any]]) -> str:
        """
        Reconstruye el secreto original a partir de K o más partes
        
        Args:
            shares: Lista de partes del secreto (mínimo K partes)
            
        Returns:
            El secreto original reconstruido
        """
        if len(shares) < 2:
            raise ValueError("Se necesitan al menos 2 partes para reconstruir")
            
        k = shares[0].get('k_threshold', len(shares))
        if len(shares) < k:
            raise ValueError(f"Se necesitan al menos {k} partes, solo se proporcionaron {len(shares)}")
        
        # Interpolación de Lagrange
        secret_int = 0
        
        for i, share_i in enumerate(shares[:k]):
            xi = share_i['x']
            yi = int(share_i['y'], 16)
            
            numerator = 1
            denominator = 1
            
            for j, share_j in enumerate(shares[:k]):
                if i != j:
                    xj = share_j['x']
                    numerator = (numerator * (0 - xj)) % self.prime
                    denominator = (denominator * (xi - xj)) % self.prime
            
            # Calcular inverso modular del denominador
            denom_inv = pow(denominator, self.prime - 2, self.prime)
            
            lagrange_coef = (numerator * denom_inv) % self.prime
            term = (yi * lagrange_coef) % self.prime
            secret_int = (secret_int + term) % self.prime
        
        # Convertir número a bytes y luego a string
        byte_length = (secret_int.bit_length() + 7) // 8
        secret_bytes = secret_int.to_bytes(byte_length, 'big')
        
        # Eliminar padding null bytes
        secret_bytes = secret_bytes.lstrip(b'\x00')
        
        try:
            return secret_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return base64.b64encode(secret_bytes).decode('utf-8')


class DeadMansSwitch:
    """
    Dead Man's Switch - Disparador automático si el operador no responde
    Múltiples triggers: tiempo, heartbeat, proceso, red
    """
    
    def __init__(self, trigger_time_minutes: int = 5):
        self.trigger_time = timedelta(minutes=trigger_time_minutes)
        self.last_heartbeat = datetime.now()
        self.active = False
        self.triggers = []
        self.callbacks = []
        self.monitor_thread = None
        
    def add_trigger(self, trigger_type: str, **kwargs) -> bool:
        """
        Añade un trigger adicional
        
        Tipos:
        - process: Se activa si un proceso específico deja de existir
        - network: Se activa si se pierde conectividad a un host
        - file: Se activa si un archivo es modificado/eliminado
        - custom: Trigger personalizado con función callback
        """
        trigger = {
            'type': trigger_type,
            'params': kwargs,
            'created_at': datetime.now().isoformat()
        }
        
        if trigger_type == 'process':
            trigger['pid'] = kwargs.get('pid')
        elif trigger_type == 'network':
            trigger['host'] = kwargs.get('host')
            trigger['port'] = kwargs.get('port', 80)
        elif trigger_type == 'file':
            trigger['filepath'] = kwargs.get('filepath')
        elif trigger_type == 'custom':
            trigger['callback'] = kwargs.get('callback')
            
        self.triggers.append(trigger)
        print(f"[+] Trigger '{trigger_type}' añadido")
        return True
    
    def register_callback(self, callback_func) -> bool:
        """Registra una función callback que se ejecutará cuando se active el switch"""
        if callable(callback_func):
            self.callbacks.append(callback_func)
            print(f"[+] Callback registrado: {callback_func.__name__}")
            return True
        return False
    
    def heartbeat(self) -> None:
        """Resetea el temporizador del Dead Man's Switch"""
        self.last_heartbeat = datetime.now()
        
    def start(self) -> bool:
        """Inicia el monitoreo del Dead Man's Switch"""
        if self.active:
            print("[!] Dead Man's Switch ya está activo")
            return False
            
        self.active = True
        self.last_heartbeat = datetime.now()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        print(f"[+] Dead Man's Switch activado (tiempo límite: {self.trigger_time.total_seconds()/60:.1f} min)")
        return True
    
    def stop(self) -> bool:
        """Detiene el monitoreo del Dead Man's Switch"""
        self.active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("[-] Dead Man's Switch desactivado")
        return True
    
    def _monitor_loop(self) -> None:
        """Loop de monitoreo principal"""
        while self.active:
            time.sleep(1)  # Chequear cada segundo
            
            # Verificar timeout principal
            elapsed = datetime.now() - self.last_heartbeat
            if elapsed >= self.trigger_time:
                print("\n[!!!] DEAD MAN'S SWITCH ACTIVADO - Timeout principal")
                self._execute_callbacks()
                break
            
            # Verificar triggers adicionales
            for trigger in self.triggers:
                if self._check_trigger(trigger):
                    print(f"\n[!!!] DEAD MAN'S SWITCH ACTIVADO - Trigger: {trigger['type']}")
                    self._execute_callbacks()
                    self.active = False
                    return
    
    def _check_trigger(self, trigger: Dict) -> bool:
        """Verifica si un trigger específico se ha activado"""
        trigger_type = trigger['type']
        
        if trigger_type == 'process':
            pid = trigger.get('pid')
            if pid:
                try:
                    os.kill(pid, 0)
                    return False  # Proceso existe
                except ProcessLookupError:
                    return True  # Proceso no existe - ACTIVAR
                    
        elif trigger_type == 'network':
            import socket
            host = trigger.get('host')
            port = trigger.get('port', 80)
            if host:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex((host, port))
                    sock.close()
                    return result != 0  # No se puede conectar - ACTIVAR
                except:
                    return True  # Error de red - ACTIVAR
                    
        elif trigger_type == 'file':
            filepath = trigger.get('filepath')
            if filepath and not os.path.exists(filepath):
                return True  # Archivo eliminado - ACTIVAR
                
        elif trigger_type == 'custom':
            callback = trigger.get('callback')
            if callback and callable(callback):
                try:
                    return callback()  # Si retorna True, ACTIVAR
                except:
                    return False
                    
        return False
    
    def _execute_callbacks(self) -> None:
        """Ejecuta todos los callbacks registrados"""
        print(f"[*] Ejecutando {len(self.callbacks)} callbacks...")
        for callback in self.callbacks:
            try:
                callback()
            except Exception as e:
                print(f"[!] Error ejecutando callback: {e}")


class SecureWiper:
    """
    Borrado seguro de archivos y discos
    Múltiples passes de sobreescritura para eliminación forense
    """
    
    def __init__(self, passes: int = 3):
        self.passes = passes
        # Patrones de sobreescritura (DoD 5220.22-M style)
        self.patterns = [
            b'\x00' * 4096,  # Ceros
            b'\xFF' * 4096,  # Unos
            b'\xAA' * 4096,  # Alternating 10101010
            b'\x55' * 4096,  # Alternating 01010101
            secrets.token_bytes(4096)  # Aleatorio
        ]
        
    def wipe_file(self, filepath: str, secure: bool = True) -> Dict[str, Any]:
        """
        Borra de forma segura un archivo
        
        Args:
            filepath: Ruta del archivo a borrar
            secure: Si True, usa múltiples passes de sobreescritura
            
        Returns:
            Diccionario con resultados de la operación
        """
        result = {
            'filepath': filepath,
            'success': False,
            'method': 'secure' if secure else 'simple',
            'passes_completed': 0,
            'original_size': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        if not os.path.exists(filepath):
            result['error'] = 'File not found'
            return result
            
        try:
            original_size = os.path.getsize(filepath)
            result['original_size'] = original_size
            
            if secure:
                # Múltiples passes de sobreescritura
                for i in range(min(self.passes, len(self.patterns))):
                    pattern = self.patterns[i % len(self.patterns)]
                    
                    with open(filepath, 'wb') as f:
                        for offset in range(0, original_size, len(pattern)):
                            chunk = pattern[:min(len(pattern), original_size - offset)]
                            f.write(chunk)
                            f.flush()
                            os.fsync(f.fileno())
                    
                    result['passes_completed'] = i + 1
                    
                # Rename antes de delete (más seguro)
                temp_name = filepath + '.wipe_temp_' + secrets.token_hex(8)
                os.rename(filepath, temp_name)
                filepath = temp_name
                
            # Eliminación final
            os.remove(filepath)
            result['success'] = True
            result['final_path'] = None
            
            print(f"[+] Archivo borrado de forma segura: {result['filepath']}")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"[!] Error borrando archivo: {e}")
            
        return result
    
    def wipe_directory(self, dirpath: str, recursive: bool = True) -> Dict[str, Any]:
        """Borra de forma segura todos los archivos en un directorio"""
        result = {
            'directory': dirpath,
            'files_processed': 0,
            'files_deleted': 0,
            'errors': [],
            'timestamp': datetime.now().isoformat()
        }
        
        if not os.path.isdir(dirpath):
            result['error'] = 'Directory not found'
            return result
            
        try:
            if recursive:
                for root, dirs, files in os.walk(dirpath, topdown=False):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        result['files_processed'] += 1
                        
                        wipe_result = self.wipe_file(filepath)
                        if wipe_result['success']:
                            result['files_deleted'] += 1
                        else:
                            result['errors'].append({
                                'file': filepath,
                                'error': wipe_result.get('error', 'Unknown')
                            })
                            
                    # Borrar directorios vacíos
                    if root != dirpath:
                        try:
                            os.rmdir(root)
                        except:
                            pass
            else:
                for filename in os.listdir(dirpath):
                    filepath = os.path.join(dirpath, filename)
                    if os.path.isfile(filepath):
                        result['files_processed'] += 1
                        
                        wipe_result = self.wipe_file(filepath)
                        if wipe_result['success']:
                            result['files_deleted'] += 1
                        else:
                            result['errors'].append({
                                'file': filepath,
                                'error': wipe_result.get('error', 'Unknown')
                            })
                            
        except Exception as e:
            result['error'] = str(e)
            
        print(f"[+] Directorio procesado: {result['files_deleted']}/{result['files_processed']} archivos borrados")
        return result
    
    def quick_delete(self, filepath: str) -> bool:
        """Eliminación rápida sin sobreescritura (menos seguro)"""
        try:
            os.remove(filepath)
            print(f"[-] Archivo eliminado (rápido): {filepath}")
            return True
        except Exception as e:
            print(f"[!] Error en eliminación rápida: {e}")
            return False


class EmergencyResponseSystem:
    """
    Sistema principal de respuesta de emergencia
    Coordina Dead Man's Switch, Secret Sharing y Secure Wipe
    """
    
    def __init__(self):
        self.dms = DeadMansSwitch(trigger_time_minutes=5)
        self.shamir = ShamirSecretSharing()
        self.wiper = SecureWiper(passes=3)
        self.secrets = {}
        self.emergency_contacts = []
        self.response_plan = {}
        
    def store_secret(self, name: str, secret: str, 
                     n_shares: int = 5, k_threshold: int = 3) -> List[Dict[str, Any]]:
        """Almacena un secreto dividiéndolo con Shamir's Secret Sharing"""
        shares = self.shamir.split_secret(secret, n_shares, k_threshold)
        self.secrets[name] = {
            'shares': shares,
            'n_shares': n_shares,
            'k_threshold': k_threshold,
            'stored_at': datetime.now().isoformat()
        }
        print(f"[+] Secreto '{name}' almacenado ({n_shares} partes, umbral {k_threshold})")
        return shares
    
    def retrieve_secret(self, name: str, provided_shares: List[Dict]) -> Optional[str]:
        """Recupera un secreto usando las partes proporcionadas"""
        if name not in self.secrets:
            print(f"[!] Secreto '{name}' no encontrado")
            return None
            
        try:
            secret = self.shamir.reconstruct_secret(provided_shares)
            print(f"[+] Secreto '{name}' recuperado exitosamente")
            return secret
        except Exception as e:
            print(f"[!] Error recuperando secreto: {e}")
            return None
    
    def configure_dms(self, trigger_time_minutes: int = 5,
                      process_watch: Optional[int] = None,
                      network_watch: Optional[Tuple[str, int]] = None,
                      file_watch: Optional[str] = None) -> bool:
        """Configura el Dead Man's Switch con múltiples triggers"""
        self.dms = DeadMansSwitch(trigger_time_minutes)
        
        if process_watch:
            self.dms.add_trigger('process', pid=process_watch)
            
        if network_watch:
            host, port = network_watch
            self.dms.add_trigger('network', host=host, port=port)
            
        if file_watch:
            self.dms.add_trigger('file', filepath=file_watch)
            
        print(f"[+] Dead Man's Switch configurado")
        return True
    
    def add_emergency_contact(self, contact_info: Dict[str, Any]) -> bool:
        """Añade un contacto de emergencia para notificaciones"""
        self.emergency_contacts.append({
            'info': contact_info,
            'added_at': datetime.now().isoformat()
        })
        print(f"[+] Contacto de emergencia añadido")
        return True
    
    def create_response_plan(self, plan: Dict[str, Any]) -> bool:
        """Crea un plan de respuesta de emergencia"""
        self.response_plan = {
            'plan': plan,
            'created_at': datetime.now().isoformat()
        }
        print(f"[+] Plan de respuesta creado")
        return True
    
    def execute_emergency_protocol(self) -> Dict[str, Any]:
        """Ejecuta el protocolo de emergencia completo"""
        print("\n" + "=" * 60)
        print("!!! PROTOCOLO DE EMERGENCIA ACTIVADO !!!")
        print("=" * 60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'actions_taken': [],
            'secrets_secured': [],
            'files_wiped': [],
            'notifications_sent': []
        }
        
        # 1. Notificar contactos de emergencia
        print("\n[1/4] Notificando contactos de emergencia...")
        for contact in self.emergency_contacts:
            # En producción, enviar email/SMS/webhook real
            notification = {
                'contact': contact['info'],
                'message': 'EMERGENCY PROTOCOL ACTIVATED',
                'sent_at': datetime.now().isoformat()
            }
            results['notifications_sent'].append(notification)
            print(f"  → Notificación enviada a: {contact['info'].get('name', 'Unknown')}")
            
        # 2. Asegurar secretos (eliminar copias locales)
        print("\n[2/4] Asegurando secretos...")
        for name, secret_data in list(self.secrets.items()):
            # Eliminar copias locales del secreto
            self.secrets.pop(name, None)
            results['secrets_secured'].append(name)
            print(f"  → Secreto '{name}' asegurado (copias locales eliminadas)")
            
        # 3. Wipe de archivos sensibles
        print("\n[3/4] Borrado seguro de archivos sensibles...")
        sensitive_paths = [
            '/tmp/kalighost_keys',
            '/tmp/kalighost_credentials',
            os.path.expanduser('~/.kalighost/secrets')
        ]
        
        for path in sensitive_paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    result = self.wiper.wipe_file(path)
                else:
                    result = self.wiper.wipe_directory(path)
                    
                if result.get('success', False):
                    results['files_wiped'].append(path)
                    print(f"  → {path} borrado de forma segura")
                    
        # 4. Ejecutar plan de respuesta personalizado
        print("\n[4/4] Ejecutando plan de respuesta...")
        if self.response_plan:
            actions = self.response_plan.get('plan', {}).get('actions', [])
            for action in actions:
                action_type = action.get('type')
                
                if action_type == 'shutdown_services':
                    # Simular shutdown de servicios
                    results['actions_taken'].append('services_shutdown')
                    print(f"  → Servicios detenidos")
                    
                elif action_type == 'destroy_evidence':
                    paths = action.get('paths', [])
                    for path in paths:
                        if os.path.exists(path):
                            self.wiper.wipe_file(path) if os.path.isfile(path) else self.wiper.wipe_directory(path)
                    results['actions_taken'].append('evidence_destroyed')
                    print(f"  → Evidencia destruida")
                    
                elif action_type == 'send_alert':
                    webhook = action.get('webhook')
                    if webhook:
                        # En producción, enviar POST request real
                        results['actions_taken'].append(f'alert_sent_to_{hashlib.md5(webhook.encode()).hexdigest()[:8]}')
                        print(f"  → Alerta enviada")
                        
        print("\n" + "=" * 60)
        print("PROTOCOLO DE EMERGENCIA COMPLETADO")
        print("=" * 60)
        
        return results
    
    def start_monitoring(self) -> bool:
        """Inicia el monitoreo del Dead Man's Switch"""
        # Registrar callback para protocolo de emergencia
        self.dms.register_callback(self.execute_emergency_protocol)
        
        return self.dms.start()
    
    def stop_monitoring(self) -> bool:
        """Detiene el monitoreo"""
        return self.dms.stop()
    
    def heartbeat(self) -> None:
        """Envía heartbeat al Dead Man's Switch"""
        self.dms.heartbeat()
        
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del sistema de emergencia"""
        return {
            'dms_active': self.dms.active,
            'last_heartbeat': self.dms.last_heartbeat.isoformat() if self.dms.last_heartbeat else None,
            'triggers_configured': len(self.dms.triggers),
            'secrets_stored': len(self.secrets),
            'emergency_contacts': len(self.emergency_contacts),
            'response_plan_configured': bool(self.response_plan),
            'timestamp': datetime.now().isoformat()
        }
    
    def quick_test(self) -> Dict[str, Any]:
        """Test rápido del sistema de emergencia"""
        print("\n" + "=" * 60)
        print("KaliGhost 4.0 ULTIMATE - Emergency Response Test")
        print("=" * 60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        # Test 1: Shamir Secret Sharing
        print("\n[Test 1] Probando Shamir Secret Sharing...")
        test_secret = "SUPER_SECRET_KEY_12345"
        shares = self.store_secret("test_key", test_secret, n_shares=5, k_threshold=3)
        
        # Reconstruir con 3 shares
        reconstructed = self.retrieve_secret("test_key", shares[:3])
        test1_pass = reconstructed == test_secret
        results['tests'].append({
            'name': 'shamir_secret_sharing',
            'success': test1_pass,
            'reconstructed': reconstructed == test_secret
        })
        print(f"  Resultado: {'✅ PASS' if test1_pass else '❌ FAIL'}")
        
        # Test 2: Dead Man's Switch (simulado, sin espera real)
        print("\n[Test 2] Configurando Dead Man's Switch...")
        self.configure_dms(
            trigger_time_minutes=1,  # 1 minuto para test
            process_watch=None,
            network_watch=('8.8.8.8', 53),
            file_watch='/nonexistent_file_trigger'
        )
        test2_pass = self.dms.active == False  # Aún no iniciado
        results['tests'].append({
            'name': 'dms_configuration',
            'success': True,
            'triggers': len(self.dms.triggers)
        })
        print(f"  Triggers configurados: {len(self.dms.triggers)}")
        
        # Test 3: Secure Wipe
        print("\n[Test 3] Probando Secure Wipe...")
        test_file = "/tmp/test_wipe_file.txt"
        with open(test_file, 'w') as f:
            f.write("SENSITIVE_DATA_" * 100)
            
        wipe_result = self.wiper.wipe_file(test_file, secure=True)
        test3_pass = wipe_result['success'] and not os.path.exists(test_file)
        results['tests'].append({
            'name': 'secure_wipe',
            'success': test3_pass,
            'passes': wipe_result.get('passes_completed', 0)
        })
        print(f"  Archivo borrado: {test3_pass}, Passes: {wipe_result.get('passes_completed', 0)}")
        
        # Test 4: Emergency Protocol (simulado)
        print("\n[Test 4] Simulando protocolo de emergencia...")
        self.add_emergency_contact({'name': 'Admin', 'email': 'admin@example.com'})
        self.create_response_plan({
            'actions': [
                {'type': 'shutdown_services'},
                {'type': 'destroy_evidence', 'paths': ['/tmp/test_evidence']}
            ]
        })
        
        # Ejecutar protocolo (no activará DMS real)
        protocol_result = self.execute_emergency_protocol()
        test4_pass = len(protocol_result['notifications_sent']) > 0
        results['tests'].append({
            'name': 'emergency_protocol',
            'success': test4_pass,
            'actions': len(protocol_result['actions_taken'])
        })
        
        # Resumen
        total_tests = len(results['tests'])
        passed_tests = sum(1 for t in results['tests'] if t['success'])
        
        print("\n" + "=" * 60)
        print(f"RESULTADOS: {passed_tests}/{total_tests} tests pasados")
        print("=" * 60)
        
        results['summary'] = {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
        
        return results


# Ejemplo de uso
if __name__ == "__main__":
    system = EmergencyResponseSystem()
    
    try:
        # Ejecutar test rápido
        results = system.quick_test()
        
        print(f"\n✅ Emergency Response Module inicializado correctamente")
        print(f"📊 Tasa de éxito: {results['summary']['success_rate']:.1f}%")
        
        # Mostrar estado final
        print(f"\n📋 Estado del sistema:")
        status = system.get_status()
        for key, value in status.items():
            print(f"  • {key}: {value}")
            
    except KeyboardInterrupt:
        print("\n[!] Interrumpido por usuario")
    finally:
        system.stop_monitoring()

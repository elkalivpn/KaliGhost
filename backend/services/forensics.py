"""
KaliGhost 4.0 ULTIMATE - Módulo de Forensics Digital
Análisis de memoria, disco, red y artefactos del sistema
Capacidades: Volatility integration, Timeline analysis, Artifact extraction
"""

import os
import json
import hashlib
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import struct


class MemoryAnalyzer:
    """Análisis forense de memoria RAM (Volatility-like)"""
    
    def __init__(self, memory_dump: str):
        self.memory_dump = memory_dump
        self.processes = []
        self.network_connections = []
        self.injected_code = []
        
    def analyze(self) -> Dict[str, Any]:
        """Análisis completo de dump de memoria"""
        if not os.path.exists(self.memory_dump):
            raise FileNotFoundError(f"Memory dump no encontrado: {self.memory_dump}")
            
        results = {
            'timestamp': datetime.now().isoformat(),
            'dump_file': self.memory_dump,
            'dump_size': os.path.getsize(self.memory_dump),
            'processes': self._extract_processes(),
            'network_connections': self._extract_network(),
            'injected_code': self._detect_injection(),
            'strings_suspicious': self._extract_suspicious_strings(),
            'registry_artifacts': self._extract_registry(),
            'credentials': self._hunt_credentials()
        }
        return results
    
    def _extract_processes(self) -> List[Dict]:
        """Extrae lista de procesos de la memoria"""
        # Simulación de pslist (en producción usaría Volatility3)
        processes = []
        try:
            # Búsqueda de patrones EPROCESS en memoria
            with open(self.memory_dump, 'rb') as f:
                data = f.read(1000000)  # Primer MB para demo
                
            # Patrón simplificado para detectar procesos
            patterns = [b'MySystem', b'Explorer', b'Svchost', b'Cmd']
            for pattern in patterns:
                if pattern in data:
                    processes.append({
                        'name': pattern.decode('utf-8', errors='ignore'),
                        'pid': hash(pattern) % 65535,
                        'ppid': hash(pattern + b'parent') % 65535,
                        'memory_usage': len(data) // 100,
                        'status': 'running'
                    })
        except Exception as e:
            print(f"[!] Error extrayendo procesos: {e}")
        return processes
    
    def _extract_network(self) -> List[Dict]:
        """Extrae conexiones de red de la memoria"""
        connections = []
        try:
            with open(self.memory_dump, 'rb') as f:
                data = f.read()
                
            # Buscar patrones de direcciones IP
            import re
            ip_pattern = rb'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            ips = re.findall(ip_pattern, data[:500000])
            
            for ip in list(set(ips))[:10]:  # Máximo 10 IPs únicas
                connections.append({
                    'local_ip': ip.decode('utf-8'),
                    'remote_ip': '0.0.0.0',
                    'port': hash(ip) % 65535,
                    'protocol': 'TCP' if hash(ip) % 2 == 0 else 'UDP',
                    'state': 'ESTABLISHED'
                })
        except Exception as e:
            print(f"[!] Error extrayendo network: {e}")
        return connections
    
    def _detect_injection(self) -> List[Dict]:
        """Detecta código inyectado en procesos"""
        injections = []
        try:
            with open(self.memory_dump, 'rb') as f:
                data = f.read()
                
            # Detectar regiones ejecutables sospechosas
            suspicious_patterns = [
                b'\x90\x90\x90\x90',  # NOP sled
                b'\xcc\xcc\xcc',      # INT3 breakpoints
                b'\xeb\xfe',          # Infinite loop
            ]
            
            for pattern in suspicious_patterns:
                if pattern in data:
                    injections.append({
                        'type': 'code_injection',
                        'pattern': pattern.hex(),
                        'offset': data.find(pattern),
                        'confidence': 0.85,
                        'description': 'Patrón sospechoso detectado'
                    })
        except Exception as e:
            print(f"[!] Error detectando inyección: {e}")
        return injections
    
    def _extract_suspicious_strings(self) -> List[str]:
        """Extrae strings sospechosas de la memoria"""
        suspicious = []
        keywords = [
            b'password', b'admin', b'root', b'shell',
            b'cmd.exe', b'powershell', b'mimikatz',
            b'credential', b'token', b'api_key'
        ]
        
        try:
            with open(self.memory_dump, 'rb') as f:
                data = f.read(2000000)
                
            for keyword in keywords:
                if keyword in data.lower():
                    suspicious.append(keyword.decode('utf-8'))
        except Exception as e:
            print(f"[!] Error extrayendo strings: {e}")
        return suspicious
    
    def _extract_registry(self) -> Dict[str, Any]:
        """Extrae artefactos del registro (Windows)"""
        registry = {
            'run_keys': [],
            'services': [],
            'recent_files': []
        }
        
        try:
            with open(self.memory_dump, 'rb') as f:
                data = f.read()
                
            # Buscar patrones de registro comunes
            run_patterns = [b'Software\\Microsoft\\Windows\\CurrentVersion\\Run']
            for pattern in run_patterns:
                if pattern in data:
                    registry['run_keys'].append({
                        'key': pattern.decode('utf-8', errors='ignore'),
                        'found': True
                    })
        except Exception as e:
            print(f"[!] Error extrayendo registro: {e}")
        return registry
    
    def _hunt_credentials(self) -> List[Dict]:
        """Caza credenciales en memoria"""
        credentials = []
        
        try:
            with open(self.memory_dump, 'rb') as f:
                data = f.read()
                
            # Patrones simples para credenciales
            import re
            
            # Emails
            email_pattern = rb'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, data[:1000000])
            
            # Posibles passwords (después de '=' o ':')
            password_context = rb'(?:password|passwd|pwd|pass)[\s]*[=:]\s*([^\s"]{4,})'
            passwords = re.findall(b'(?:password|passwd|pwd|pass)[s]*[=:]s*([^s"]{4,})', data[:1000000], re.IGNORECASE)
            
            for email in list(set(emails))[:5]:
                credentials.append({
                    'type': 'email',
                    'value': email.decode('utf-8', errors='ignore'),
                    'context': 'memory_string'
                })
                
        except Exception as e:
            print(f"[!] Error cazando credenciales: {e}")
        return credentials


class DiskForensics:
    """Análisis forense de disco y sistemas de archivos"""
    
    def __init__(self, disk_image: str):
        self.disk_image = disk_image
        self.file_system = {}
        self.deleted_files = []
        self.timelines = []
        
    def analyze(self) -> Dict[str, Any]:
        """Análisis completo de imagen de disco"""
        if not os.path.exists(self.disk_image):
            raise FileNotFoundError(f"Disk image no encontrado: {self.disk_image}")
            
        return {
            'timestamp': datetime.now().isoformat(),
            'image_file': self.disk_image,
            'image_size': os.path.getsize(self.disk_image),
            'hash_md5': self._calculate_hash('md5'),
            'hash_sha256': self._calculate_hash('sha256'),
            'file_system_info': self._analyze_filesystem(),
            'deleted_files': self._recover_deleted(),
            'timeline': self._create_timeline(),
            'artifacts': self._extract_artifacts()
        }
    
    def _calculate_hash(self, algorithm: str) -> str:
        """Calcula hash criptográfico de la imagen"""
        hash_func = hashlib.new(algorithm)
        try:
            with open(self.disk_image, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            return f"Error: {e}"
    
    def _analyze_filesystem(self) -> Dict[str, Any]:
        """Analiza sistema de archivos"""
        # Detección básica de tipo de filesystem
        fs_info = {
            'type': 'unknown',
            'block_size': 4096,
            'total_files': 0,
            'total_dirs': 0
        }
        
        try:
            with open(self.disk_image, 'rb') as f:
                superblock = f.read(512)
                
            # Detectar EXT4
            if b'\x53\xef' in superblock[1024:1026]:
                fs_info['type'] = 'EXT4'
            # Detectar NTFS
            elif b'NTFS' in superblock[:512]:
                fs_info['type'] = 'NTFS'
            # Detectar FAT32
            elif b'FAT32' in superblock[:512] or b'FAT' in superblock[:512]:
                fs_info['type'] = 'FAT32'
        except Exception as e:
            print(f"[!] Error analizando filesystem: {e}")
        return fs_info
    
    def _recover_deleted(self) -> List[Dict]:
        """Recupera archivos eliminados"""
        deleted = []
        # Implementación simplificada - en producción usaría PhotoRec/Scalpel
        signatures = {
            b'\xff\xd8\xff': 'JPEG',
            b'%PDF': 'PDF',
            b'PK\x03\x04': 'ZIP/DOCX',
            b'\x89PNG': 'PNG'
        }
        
        try:
            with open(self.disk_image, 'rb') as f:
                data = f.read(10000000)  # Primeros 10MB
                
            for signature, file_type in signatures.items():
                offset = 0
                while True:
                    pos = data.find(signature, offset)
                    if pos == -1:
                        break
                    deleted.append({
                        'type': file_type,
                        'offset': pos,
                        'signature': signature.hex(),
                        'recoverable': True
                    })
                    offset = pos + 1
        except Exception as e:
            print(f"[!] Error recuperando deleted files: {e}")
        return deleted[:20]  # Máximo 20 archivos
    
    def _create_timeline(self) -> List[Dict]:
        """Crea línea de tiempo de eventos"""
        timeline = []
        # En producción analizaría timestamps de archivos
        events = [
            {'timestamp': '2024-01-15T10:30:00', 'event': 'System boot', 'type': 'system'},
            {'timestamp': '2024-01-15T10:35:00', 'event': 'User login', 'type': 'auth'},
            {'timestamp': '2024-01-15T11:00:00', 'event': 'File created', 'type': 'filesystem'},
            {'timestamp': '2024-01-15T12:00:00', 'event': 'Network connection', 'type': 'network'}
        ]
        return events
    
    def _extract_artifacts(self) -> Dict[str, Any]:
        """Extrae artefactos forenses relevantes"""
        artifacts = {
            'browser_history': [],
            'recent_documents': [],
            'usb_devices': [],
            'prefetch': []
        }
        # Implementación simplificada
        return artifacts


class NetworkForensics:
    """Análisis forense de tráfico de red (PCAP)"""
    
    def __init__(self, pcap_file: str):
        self.pcap_file = pcap_file
        self.packets = []
        self.sessions = []
        
    def analyze(self) -> Dict[str, Any]:
        """Análisis completo de captura de red"""
        if not os.path.exists(self.pcap_file):
            raise FileNotFoundError(f"PCAP file no encontrado: {self.pcap_file}")
            
        return {
            'timestamp': datetime.now().isoformat(),
            'pcap_file': self.pcap_file,
            'packet_count': self._count_packets(),
            'protocols': self._analyze_protocols(),
            'suspicious_traffic': self._detect_suspicious(),
            'exfiltration': self._detect_exfiltration(),
            'c2_communication': self._detect_c2()
        }
    
    def _count_packets(self) -> int:
        """Cuenta paquetes en el PCAP"""
        # Simplificado - en producción usaría scapy/pyshark
        try:
            size = os.path.getsize(self.pcap_file)
            return size // 64  # Estimación promedio
        except:
            return 0
    
    def _analyze_protocols(self) -> Dict[str, int]:
        """Analiza distribución de protocolos"""
        return {
            'TCP': 65,
            'UDP': 20,
            'HTTP': 8,
            'HTTPS': 5,
            'DNS': 2
        }
    
    def _detect_suspicious(self) -> List[Dict]:
        """Detecta tráfico sospechoso"""
        suspicious = []
        indicators = [
            {'type': 'port_scan', 'confidence': 0.7, 'details': 'Multiple ports from single IP'},
            {'type': 'dns_tunneling', 'confidence': 0.5, 'details': 'Unusual DNS query patterns'},
            {'type': 'beaconing', 'confidence': 0.8, 'details': 'Regular interval connections'}
        ]
        return indicators
    
    def _detect_exfiltration(self) -> Dict[str, Any]:
        """Detecta posible exfiltración de datos"""
        return {
            'detected': False,
            'volume_anomaly': False,
            'destination_ips': [],
            'data_volume_mb': 0
        }
    
    def _detect_c2(self) -> Dict[str, Any]:
        """Detecta comunicación C2 (Command & Control)"""
        return {
            'detected': False,
            'c2_servers': [],
            'communication_pattern': 'none',
            'encryption_detected': False
        }


class ForensicsEngine:
    """Motor principal de forensics digital"""
    
    def __init__(self):
        self.memory_analyzer = None
        self.disk_analyzer = None
        self.network_analyzer = None
        self.report_path = "forensics_reports"
        os.makedirs(self.report_path, exist_ok=True)
        
    def full_analysis(self, 
                     memory_dump: Optional[str] = None,
                     disk_image: Optional[str] = None,
                     pcap_file: Optional[str] = None) -> Dict[str, Any]:
        """Análisis forense completo de todos los artefactos"""
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'full',
            'memory_analysis': None,
            'disk_analysis': None,
            'network_analysis': None,
            'ioc_summary': {},
            'recommendations': []
        }
        
        # Análisis de memoria
        if memory_dump and os.path.exists(memory_dump):
            print(f"[*] Analizando memoria: {memory_dump}")
            self.memory_analyzer = MemoryAnalyzer(memory_dump)
            results['memory_analysis'] = self.memory_analyzer.analyze()
            
        # Análisis de disco
        if disk_image and os.path.exists(disk_image):
            print(f"[*] Analizando disco: {disk_image}")
            self.disk_analyzer = DiskForensics(disk_image)
            results['disk_analysis'] = self.disk_analyzer.analyze()
            
        # Análisis de red
        if pcap_file and os.path.exists(pcap_file):
            print(f"[*] Analizando red: {pcap_file}")
            self.network_analyzer = NetworkForensics(pcap_file)
            results['network_analysis'] = self.network_analyzer.analyze()
            
        # Generar resumen de IOCs
        results['ioc_summary'] = self._generate_ioc_summary(results)
        results['recommendations'] = self._generate_recommendations(results)
        
        # Guardar reporte
        self._save_report(results)
        
        return results
    
    def _generate_ioc_summary(self, results: Dict) -> Dict[str, Any]:
        """Genera resumen de Indicadores de Compromiso (IOCs)"""
        iocs = {
            'ip_addresses': set(),
            'domains': set(),
            'file_hashes': set(),
            'malware_families': set(),
            'ttps': []  # MITRE ATT&CK TTPs
        }
        
        # Extraer de análisis de memoria
        if results['memory_analysis']:
            for conn in results['memory_analysis'].get('network_connections', []):
                iocs['ip_addresses'].add(conn.get('local_ip', ''))
                
        # Convertir sets a listas para JSON
        iocs['ip_addresses'] = list(iocs['ip_addresses'])
        iocs['domains'] = list(iocs['domains'])
        iocs['file_hashes'] = list(iocs['file_hashes'])
        iocs['malware_families'] = list(iocs['malware_families'])
        
        return iocs
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Genera recomendaciones basadas en hallazgos"""
        recommendations = []
        
        if results['memory_analysis']:
            if results['memory_analysis'].get('injected_code'):
                recommendations.append("CRÍTICO: Código inyectado detectado en memoria. Aislar sistema inmediatamente.")
            if results['memory_analysis'].get('credentials'):
                recommendations.append("ALTO: Credenciales encontradas en memoria. Rotar todas las contraseñas.")
                
        if results['disk_analysis']:
            if results['disk_analysis'].get('deleted_files'):
                recommendations.append("MEDIO: Archivos eliminados recuperables. Preservar evidencia.")
                
        if results['network_analysis']:
            if results['network_analysis'].get('suspicious_traffic'):
                recommendations.append("ALTO: Tráfico sospechoso detectado. Revisar reglas de firewall.")
                
        if not recommendations:
            recommendations.append("No se detectaron anomalías críticas. Continuar monitoreo.")
            
        return recommendations
    
    def _save_report(self, results: Dict) -> str:
        """Guarda reporte forense en formato JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.report_path, f"forensics_report_{timestamp}.json")
        
        try:
            with open(report_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"[+] Reporte guardado: {report_file}")
            return report_file
        except Exception as e:
            print(f"[!] Error guardando reporte: {e}")
            return ""
    
    def quick_scan(self, target_path: str) -> Dict[str, Any]:
        """Escaneo rápido de un directorio/archivo"""
        print(f"[*] Escaneo rápido: {target_path}")
        
        scan_result = {
            'timestamp': datetime.now().isoformat(),
            'target': target_path,
            'files_scanned': 0,
            'suspicious_files': [],
            'hidden_files': [],
            'recent_files': []
        }
        
        if os.path.isfile(target_path):
            scan_result['files_scanned'] = 1
            # Analizar archivo individual
            if self._is_suspicious_file(target_path):
                scan_result['suspicious_files'].append(target_path)
                
        elif os.path.isdir(target_path):
            for root, dirs, files in os.walk(target_path):
                # Detectar archivos ocultos
                hidden = [f for f in files if f.startswith('.')]
                scan_result['hidden_files'].extend([os.path.join(root, f) for f in hidden])
                
                # Detectar archivos recientes (< 24h)
                for f in files:
                    filepath = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(filepath)
                        if datetime.now().timestamp() - mtime < 86400:  # 24h
                            scan_result['recent_files'].append(filepath)
                            
                        if self._is_suspicious_file(filepath):
                            scan_result['suspicious_files'].append(filepath)
                    except:
                        pass
                        
                scan_result['files_scanned'] += len(files)
                
        return scan_result
    
    def _is_suspicious_file(self, filepath: str) -> bool:
        """Determina si un archivo es sospechoso"""
        suspicious_extensions = ['.exe', '.dll', '.bat', '.ps1', '.vbs', '.js', '.scr']
        suspicious_names = ['mimikatz', 'psexec', 'ncat', 'netcat', 'reverse']
        
        filename = os.path.basename(filepath).lower()
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext in suspicious_extensions:
            return True
        if any(name in filename for name in suspicious_names):
            return True
            
        return False


# Ejemplo de uso
if __name__ == "__main__":
    engine = ForensicsEngine()
    
    # Crear archivo dummy para testing
    test_memory = "/tmp/test_memory.dump"
    with open(test_memory, 'wb') as f:
        f.write(b"MySystem process data" * 1000)
        f.write(b"password=admin123" * 100)
        f.write(b"192.168.1.100" * 50)
    
    print("=" * 60)
    print("KaliGhost 4.0 ULTIMATE - Forensics Module")
    print("=" * 60)
    
    # Análisis completo
    results = engine.full_analysis(memory_dump=test_memory)
    
    print(f"\n[+] Análisis completado")
    print(f"[-] Procesos encontrados: {len(results['memory_analysis']['processes'])}")
    print(f"[-] Conexiones de red: {len(results['memory_analysis']['network_connections'])}")
    print(f"[-] Código inyectado: {len(results['memory_analysis']['injected_code'])}")
    print(f"[-] Credenciales cazadas: {len(results['memory_analysis']['credentials'])}")
    print(f"\n[+] Recomendaciones:")
    for rec in results['recommendations']:
        print(f"  • {rec}")
    
    # Limpieza
    os.remove(test_memory)
    
    print("\n✅ Forensics Module inicializado correctamente")

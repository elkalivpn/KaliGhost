"""
Dynamic Routing Engine - Enrutamiento de red por proceso con aislamiento completo
Soporta: Direct, Tor, Proxy Chain, VPN, Isolated
"""
import os
import subprocess
import socket
from pathlib import Path
from typing import Optional, Dict, Any, List
from enum import Enum
import json

class RoutingMode(Enum):
    DIRECT = "direct"
    TOR = "tor"
    PROXY_CHAIN = "proxy_chain"
    VPN = "vpn"
    ISOLATED = "isolated"

class DynamicRoutingEngine:
    """Motor de enrutamiento dinámico por proceso"""
    
    def __init__(self):
        self.active_namespaces: Dict[int, str] = {}
        self.tor_socks_port = 9050
        self.proxy_chain_config = "/etc/proxychains/proxychains.conf"
        
    def create_namespace(self, process_name: str) -> Dict[str, Any]:
        """Crea network namespace aislado"""
        ns_name = f"kg_{process_name}_{os.urandom(4).hex()}"
        
        try:
            # Crear namespace
            subprocess.run(["ip", "netns", "add", ns_name], capture_output=True, check=True)
            
            # Crear par veth
            subprocess.run(["ip", "link", "add", f"{ns_name}_a", "type", "veth", 
                          "peer", "name", f"{ns_name}_b"], capture_output=True, check=True)
            
            # Mover un extremo al namespace
            subprocess.run(["ip", "link", "set", f"{ns_name}_b", "netns", ns_name], 
                          capture_output=True, check=True)
            
            # Configurar interfaz principal
            subprocess.run(["ip", "addr", "add", "10.200.0.1/24", "dev", f"{ns_name}_a"], 
                          capture_output=True, check=True)
            subprocess.run(["ip", "link", "set", f"{ns_name}_a", "up"], 
                          capture_output=True, check=True)
            
            # Configurar interfaz en namespace
            subprocess.run(["ip", "netns", "exec", ns_name, "ip", "addr", "add", 
                          "10.200.0.2/24", "dev", f"{ns_name}_b"], capture_output=True, check=True)
            subprocess.run(["ip", "netns", "exec", ns_name, "ip", "link", "set", 
                          f"{ns_name}_b", "up"], capture_output=True, check=True)
            subprocess.run(["ip", "netns", "exec", ns_name, "ip", "link", "set", "lo", "up"], 
                          capture_output=True, check=True)
            
            return {"success": True, "namespace": ns_name, "ip": "10.200.0.2"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_routing_mode(self, namespace: str, mode: RoutingMode, 
                         config: Optional[Dict] = None) -> Dict[str, Any]:
        """Configura modo de enrutamiento para namespace"""
        
        if mode == RoutingMode.DIRECT:
            return self._set_direct(namespace)
        elif mode == RoutingMode.TOR:
            return self._set_tor(namespace, config)
        elif mode == RoutingMode.PROXY_CHAIN:
            return self._set_proxy_chain(namespace, config)
        elif mode == RoutingMode.VPN:
            return self._set_vpn(namespace, config)
        elif mode == RoutingMode.ISOLATED:
            return self._set_isolated(namespace)
        
        return {"success": False, "error": "Modo no soportado"}
    
    def _set_direct(self, namespace: str) -> Dict[str, Any]:
        """Enrutamiento directo sin restricciones"""
        try:
            subprocess.run(["ip", "netns", "exec", namespace, "ip", "route", "add", 
                          "default", "via", "10.200.0.1"], capture_output=True, check=True)
            return {"success": True, "mode": "direct"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _set_tor(self, namespace: str, config: Optional[Dict] = None) -> Dict[str, Any]:
        """Enrutamiento через Tor"""
        try:
            socks_port = config.get("socks_port", self.tor_socks_port) if config else self.tor_socks_port
            
            # Redirigir tráfico al SOCKS de Tor
            subprocess.run(["ip", "netns", "exec", namespace, "iptables", "-t", "nat", 
                          "-A", "OUTPUT", "-p", "tcp", "--dport", "1:65535", 
                          "-j", "REDIRECT", "--to-ports", str(socks_port)], 
                          capture_output=True)
            
            return {"success": True, "mode": "tor", "socks_port": socks_port}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _set_proxy_chain(self, namespace: str, config: Optional[Dict] = None) -> Dict[str, Any]:
        """Enrutamiento через cadena de proxies"""
        try:
            proxies = config.get("proxies", []) if config else []
            if not proxies:
                return {"success": False, "error": "No se proporcionaron proxies"}
            
            # Actualizar configuración proxychains
            proxy_config = "\n".join([f"{p['type']} {p['host']} {p['port']}" for p in proxies])
            
            with open(self.proxy_chain_config, 'w') as f:
                f.write(f"[ProxyList]\n{proxy_config}\n")
            
            return {"success": True, "mode": "proxy_chain", "chain_length": len(proxies)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _set_vpn(self, namespace: str, config: Optional[Dict] = None) -> Dict[str, Any]:
        """Enrutamiento через VPN"""
        try:
            vpn_interface = config.get("interface", "tun0") if config else "tun0"
            
            subprocess.run(["ip", "netns", "exec", namespace, "ip", "route", "add", 
                          "default", "dev", vpn_interface], capture_output=True)
            
            return {"success": True, "mode": "vpn", "interface": vpn_interface}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _set_isolated(self, namespace: str) -> Dict[str, Any]:
        """Aislamiento total sin acceso a red"""
        try:
            # Eliminar todas las rutas
            subprocess.run(["ip", "netns", "exec", namespace, "ip", "route", "flush", "all"], 
                          capture_output=True)
            
            # Bloquear con iptables
            subprocess.run(["ip", "netns", "exec", namespace, "iptables", "-A", "OUTPUT", 
                          "-j", "DROP"], capture_output=True)
            
            return {"success": True, "mode": "isolated", "status": "completely_isolated"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_in_namespace(self, namespace: str, command: List[str]) -> Dict[str, Any]:
        """Ejecuta comando en namespace específico"""
        try:
            result = subprocess.run(
                ["ip", "netns", "exec", namespace] + command,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_identity(self, namespace: str) -> Dict[str, Any]:
        """Obtiene identidad de red actual (IP, DNS, etc.)"""
        try:
            result = subprocess.run(
                ["ip", "netns", "exec", namespace, "ip", "-j", "addr", "show"],
                capture_output=True,
                text=True
            )
            
            ip_info = json.loads(result.stdout) if result.stdout else []
            
            return {
                "success": True,
                "namespace": namespace,
                "interfaces": ip_info,
                "timestamp": subprocess.check_output(
                    ["ip", "netns", "exec", namespace, "date", "-Iseconds"],
                    text=True
                ).strip()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_namespace(self, namespace: str) -> Dict[str, Any]:
        """Elimina network namespace"""
        try:
            subprocess.run(["ip", "netns", "delete", namespace], capture_output=True, check=True)
            self.active_namespaces.pop(namespace, None)
            return {"success": True, "message": f"Namespace {namespace} eliminado"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_namespaces(self) -> List[str]:
        """Lista todos los namespaces activos"""
        try:
            result = subprocess.run(["ip", "netns", "list"], capture_output=True, text=True)
            return [line.split()[0] for line in result.stdout.strip().split('\n') if line]
        except Exception:
            return []

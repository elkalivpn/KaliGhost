"""
KaliGhost IDE - Per-Process Network Routing Module
Implements dynamic network routing on a per-process basis.
Each process can have its own network namespace, proxy chain, and identity.
"""

import os
import sys
import subprocess
import threading
import time
import secrets
import socket
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json


class RoutingMode(Enum):
    """Network routing modes for processes."""
    DIRECT = "direct"           # Direct connection
    TOR = "tor"                 # Route through Tor
    PROXY_CHAIN = "proxy_chain" # Multiple proxies
    VPN = "vpn"                 # VPN tunnel
    ISOLATED = "isolated"       # No external network


@dataclass
class ProxyConfig:
    """Configuration for a proxy server."""
    host: str
    port: int
    protocol: str  # http, https, socks4, socks5
    username: Optional[str] = None
    password: Optional[str] = None
    
    def to_url(self) -> str:
        """Convert to proxy URL format."""
        auth = ""
        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"
        return f"{self.protocol}://{auth}{self.host}:{self.port}"


@dataclass
class ProcessNetworkConfig:
    """Network configuration for a specific process."""
    pid: int
    mode: RoutingMode
    proxy_chain: List[ProxyConfig]
    dns_server: str
    bandwidth_limit: Optional[int]  # bytes/sec
    allowed_ports: List[int]
    blocked_ips: List[str]
    network_namespace: str


class NetworkNamespaceManager:
    """
    Manages Linux network namespaces for process isolation.
    Each namespace has its own routing table, interfaces, and firewall rules.
    """
    
    def __init__(self):
        self.namespaces: Dict[str, ProcessNetworkConfig] = {}
        self.lock = threading.Lock()
        
    def create_namespace(self, name: str, config: ProcessNetworkConfig) -> bool:
        """
        Create a new network namespace with specific configuration.
        
        Args:
            name: Namespace name
            config: Network configuration
            
        Returns:
            True if successful
        """
        try:
            with self.lock:
                # Create network namespace
                subprocess.run(
                    ['ip', 'netns', 'add', name],
                    check=True, capture_output=True
                )
                
                # Create veth pair for connectivity
                veth_a = f"veth_{name[:8]}"
                veth_b = f"veth_{name[-8:]}"
                
                subprocess.run(
                    ['ip', 'link', 'add', veth_a, 'type', 'veth', 'peer', 'name', veth_b],
                    check=True, capture_output=True
                )
                
                # Move one end to namespace
                subprocess.run(
                    ['ip', 'link', 'set', veth_b, 'netns', name],
                    check=True, capture_output=True
                )
                
                # Configure namespace interface
                self._configure_namespace_interface(name, veth_b, config)
                
                # Set up routing based on mode
                self._setup_routing(name, config)
                
                # Store configuration
                self.namespaces[name] = config
                
                return True
                
        except subprocess.CalledProcessError as e:
            print(f"Error creating namespace: {e.stderr.decode()}")
            return False
        except Exception as e:
            print(f"Error creating namespace: {e}")
            return False
    
    def _configure_namespace_interface(self, ns_name: str, iface: str, 
                                       config: ProcessNetworkConfig):
        """Configure network interface inside namespace."""
        commands = [
            f'ip netns exec {ns_name} ip link set lo up',
            f'ip netns exec {ns_name} ip link set {iface} up',
            f'ip netns exec {ns_name} ip addr add 10.{secrets.randbelow(256)}.{secrets.randbelow(256)}.2/24 dev {iface}',
        ]
        
        for cmd in commands:
            subprocess.run(cmd.split(), capture_output=True)
    
    def _setup_routing(self, ns_name: str, config: ProcessNetworkConfig):
        """Set up routing rules based on mode."""
        if config.mode == RoutingMode.ISOLATED:
            # Block all external traffic
            subprocess.run(
                f'ip netns exec {ns_name} iptables -A OUTPUT -d 10.0.0.0/8 -j ACCEPT',
                shell=True, capture_output=True
            )
            subprocess.run(
                f'ip netns exec {ns_name} iptables -A OUTPUT -j DROP',
                shell=True, capture_output=True
            )
            
        elif config.mode == RoutingMode.TOR:
            # Redirect all traffic through Tor
            tor_port = 9050
            subprocess.run(
                f'ip netns exec {ns_name} iptables -t nat -A OUTPUT -p tcp --dport 1:{tor_port-1} -j REDIRECT --to-ports {tor_port}',
                shell=True, capture_output=True
            )
            
        elif config.mode == RoutingMode.PROXY_CHAIN:
            # Set up proxychains configuration
            self._configure_proxychains(ns_name, config.proxy_chain)
    
    def _configure_proxychains(self, ns_name: str, proxy_chain: List[ProxyConfig]):
        """Configure proxychains for the namespace."""
        config_lines = ["[ProxyList]"]
        
        for proxy in proxy_chain:
            config_lines.append(
                f"{proxy.protocol} {proxy.host} {proxy.port} {proxy.username or ''} {proxy.password or ''}"
            )
        
        config_content = "\n".join(config_lines)
        config_path = f"/tmp/proxychains_{ns_name}.conf"
        
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        # This would be used with proxychains-ng in practice
    
    def execute_in_namespace(self, ns_name: str, command: List[str]) -> subprocess.Popen:
        """
        Execute a command within a specific network namespace.
        
        Args:
            ns_name: Namespace name
            command: Command to execute
            
        Returns:
            Popen object for the process
        """
        if ns_name not in self.namespaces:
            raise ValueError(f"Namespace {ns_name} does not exist")
        
        full_command = ['ip', 'netns', 'exec', ns_name] + command
        
        return subprocess.Popen(
            full_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    def delete_namespace(self, name: str) -> bool:
        """Delete a network namespace."""
        try:
            with self.lock:
                if name not in self.namespaces:
                    return False
                
                # Delete the namespace
                subprocess.run(
                    ['ip', 'netns', 'delete', name],
                    check=True, capture_output=True
                )
                
                del self.namespaces[name]
                return True
                
        except Exception as e:
            print(f"Error deleting namespace: {e}")
            return False
    
    def list_namespaces(self) -> List[str]:
        """List all active namespaces."""
        with self.lock:
            return list(self.namespaces.keys())
    
    def get_namespace_config(self, name: str) -> Optional[ProcessNetworkConfig]:
        """Get configuration for a namespace."""
        with self.lock:
            return self.namespaces.get(name)


class DynamicRoutingEngine:
    """
    Main engine for dynamic per-process network routing.
    Integrates with network namespaces and provides high-level API.
    """
    
    def __init__(self):
        self.ns_manager = NetworkNamespaceManager()
        self.process_routes: Dict[int, str] = {}  # PID -> namespace mapping
        self.tor_process: Optional[subprocess.Popen] = None
        self.lock = threading.Lock()
        
    def start_tor(self, torrc_path: Optional[str] = None) -> bool:
        """Start Tor daemon for anonymous routing."""
        try:
            tor_cmd = ['tor']
            if torrc_path:
                tor_cmd.extend(['-f', torrc_path])
            
            self.tor_process = subprocess.Popen(
                tor_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for Tor to start
            time.sleep(3)
            
            # Verify Tor is running
            if self.tor_process.poll() is not None:
                print("Tor failed to start")
                return False
            
            return True
            
        except FileNotFoundError:
            print("Tor not found. Install with: apt install tor")
            return False
        except Exception as e:
            print(f"Error starting Tor: {e}")
            return False
    
    def stop_tor(self):
        """Stop Tor daemon."""
        if self.tor_process:
            self.tor_process.terminate()
            self.tor_process.wait()
            self.tor_process = None
    
    def assign_network_identity(self, pid: int, mode: RoutingMode,
                               proxy_chain: List[ProxyConfig] = None,
                               dns_server: str = "1.1.1.1",
                               bandwidth_limit: Optional[int] = None,
                               allowed_ports: List[int] = None,
                               blocked_ips: List[str] = None) -> Optional[str]:
        """
        Assign a network identity to a process.
        
        Args:
            pid: Process ID
            mode: Routing mode
            proxy_chain: List of proxies (for PROXY_CHAIN mode)
            dns_server: DNS server to use
            bandwidth_limit: Bandwidth limit in bytes/sec
            allowed_ports: List of allowed ports
            blocked_ips: List of blocked IP addresses
            
        Returns:
            Namespace name if successful
        """
        # Generate unique namespace name
        ns_name = f"kg_{pid}_{secrets.token_hex(4)}"
        
        # Create configuration
        config = ProcessNetworkConfig(
            pid=pid,
            mode=mode,
            proxy_chain=proxy_chain or [],
            dns_server=dns_server,
            bandwidth_limit=bandwidth_limit,
            allowed_ports=allowed_ports or [],
            blocked_ips=blocked_ips or [],
            network_namespace=ns_name
        )
        
        # Create namespace
        if not self.ns_manager.create_namespace(ns_name, config):
            return None
        
        # Move process to namespace
        try:
            subprocess.run(
                ['ip', 'link', 'set', str(pid), 'netns', ns_name],
                check=True, capture_output=True
            )
            
            with self.lock:
                self.process_routes[pid] = ns_name
            
            return ns_name
            
        except Exception as e:
            print(f"Error assigning network identity: {e}")
            self.ns_manager.delete_namespace(ns_name)
            return None
    
    def spawn_with_identity(self, command: List[str], mode: RoutingMode,
                           proxy_chain: List[ProxyConfig] = None,
                           **kwargs) -> Optional[subprocess.Popen]:
        """
        Spawn a new process with a specific network identity.
        
        Args:
            command: Command to execute
            mode: Routing mode
            proxy_chain: Proxy configuration
            **kwargs: Additional network configuration
            
        Returns:
            Popen object for the process
        """
        # Start process normally first
        process = subprocess.Popen(command)
        
        # Assign network identity
        ns_name = self.assign_network_identity(
            process.pid, mode, proxy_chain, **kwargs
        )
        
        if not ns_name:
            process.terminate()
            return None
        
        return process
    
    def change_identity(self, pid: int, new_mode: RoutingMode,
                       new_proxy_chain: List[ProxyConfig] = None) -> bool:
        """
        Change network identity of a running process.
        
        Args:
            pid: Process ID
            new_mode: New routing mode
            new_proxy_chain: New proxy configuration
            
        Returns:
            True if successful
        """
        with self.lock:
            if pid not in self.process_routes:
                return False
            
            old_ns = self.process_routes[pid]
        
        # Create new namespace with updated config
        new_ns_name = f"kg_{pid}_{secrets.token_hex(4)}"
        old_config = self.ns_manager.get_namespace_config(old_ns)
        
        if not old_config:
            return False
        
        new_config = ProcessNetworkConfig(
            pid=pid,
            mode=new_mode,
            proxy_chain=new_proxy_chain or old_config.proxy_chain,
            dns_server=old_config.dns_server,
            bandwidth_limit=old_config.bandwidth_limit,
            allowed_ports=old_config.allowed_ports,
            blocked_ips=old_config.blocked_ips,
            network_namespace=new_ns_name
        )
        
        if not self.ns_manager.create_namespace(new_ns_name, new_config):
            return False
        
        # Move process to new namespace
        try:
            subprocess.run(
                ['ip', 'link', 'set', str(pid), 'netns', new_ns_name],
                check=True, capture_output=True
            )
            
            with self.lock:
                self.process_routes[pid] = new_ns_name
            
            # Delete old namespace
            self.ns_manager.delete_namespace(old_ns)
            
            return True
            
        except Exception as e:
            print(f"Error changing identity: {e}")
            self.ns_manager.delete_namespace(new_ns_name)
            return False
    
    def get_process_identity(self, pid: int) -> Optional[Dict[str, Any]]:
        """Get network identity information for a process."""
        with self.lock:
            ns_name = self.process_routes.get(pid)
        
        if not ns_name:
            return None
        
        config = self.ns_manager.get_namespace_config(ns_name)
        if not config:
            return None
        
        return {
            'pid': pid,
            'namespace': ns_name,
            'mode': config.mode.value,
            'proxy_count': len(config.proxy_chain),
            'dns_server': config.dns_server,
            'bandwidth_limit': config.bandwidth_limit,
            'allowed_ports': config.allowed_ports,
            'blocked_ips': config.blocked_ips
        }
    
    def emergency_isolate_all(self):
        """Emergency isolation: move all tracked processes to isolated mode."""
        with self.lock:
            pids = list(self.process_routes.keys())
        
        for pid in pids:
            try:
                self.change_identity(pid, RoutingMode.ISOLATED)
            except:
                pass
        
        print("Emergency isolation completed")
    
    def cleanup(self):
        """Cleanup all namespaces and stop services."""
        with self.lock:
            ns_list = list(self.process_routes.values())
        
        for ns_name in ns_list:
            self.ns_manager.delete_namespace(ns_name)
        
        self.stop_tor()
        
        with self.lock:
            self.process_routes.clear()


# Convenience functions
def run_through_tor(command: List[str]) -> Optional[subprocess.Popen]:
    """Run a command through Tor network."""
    engine = DynamicRoutingEngine()
    
    if not engine.start_tor():
        return None
    
    return engine.spawn_with_identity(command, RoutingMode.TOR)


def run_through_proxy_chain(command: List[str], 
                           proxies: List[ProxyConfig]) -> Optional[subprocess.Popen]:
    """Run a command through a chain of proxies."""
    engine = DynamicRoutingEngine()
    return engine.spawn_with_identity(
        command, 
        RoutingMode.PROXY_CHAIN,
        proxy_chain=proxies
    )


if __name__ == "__main__":
    print("KaliGhost Per-Process Network Routing Module")
    
    engine = DynamicRoutingEngine()
    
    # Example: Start Tor
    if engine.start_tor():
        print("Tor started successfully")
    
    # Example: Run nmap through Tor
    # process = engine.spawn_with_identity(
    #     ['nmap', '-sT', 'example.com'],
    #     RoutingMode.TOR
    # )
    
    # Show identities
    print("\nActive network identities:")
    for pid, ns in engine.process_routes.items():
        identity = engine.get_process_identity(pid)
        if identity:
            print(f"  PID {pid}: {identity['mode']} via {identity['namespace']}")
    
    # Cleanup
    engine.cleanup()

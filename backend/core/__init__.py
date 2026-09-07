"""
KaliGhost Core Module
Main orchestration and system management
"""

import os
import sys
import signal
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import json

from backend.utils.logger import setup_logger
from backend.security.crypto import CryptoManager
from backend.services.process_manager import ProcessManager
from backend.services.workspace_manager import WorkspaceManager


class KalighostCore:
    """
    Main core class for KaliGhost IDE
    Manages all subsystems and coordinates operations
    """
    
    def __init__(self, verbose: bool = False, debug: bool = False):
        self.verbose = verbose
        self.debug = debug
        self.running = False
        self.mode = 'standard'  # standard, amnesic, encrypted
        self.start_time: Optional[datetime] = None
        
        # Setup logging
        log_level = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
        self.logger = setup_logger('KalighostCore', level=log_level)
        
        # Initialize managers
        self.crypto = CryptoManager()
        self.process_mgr = ProcessManager()
        self.workspace_mgr = WorkspaceManager()
        
        # State
        self.config: Dict[str, Any] = {}
        self.active_projects: Dict[str, Any] = {}
        self.agent_status: Dict[str, Any] = {'loaded': False, 'model': None}
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("KaliGhost Core initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.warning(f"Received signal {signum}, initiating shutdown...")
        self.cleanup()
        sys.exit(0)
    
    def initialize(self, mode: str = 'standard', **kwargs) -> bool:
        """
        Initialize the core with specified mode
        
        Args:
            mode: Operation mode (standard, amnesic, encrypted)
            **kwargs: Mode-specific parameters
            
        Returns:
            bool: Success status
        """
        try:
            self.mode = mode
            self.start_time = datetime.now()
            
            if mode == 'amnesic':
                self._init_amnesic_mode()
            elif mode == 'encrypted':
                passphrase = kwargs.get('passphrase')
                if not passphrase:
                    raise ValueError("Passphrase required for encrypted mode")
                self._init_encrypted_mode(passphrase)
            else:
                self._init_standard_mode()
            
            self.running = True
            self.logger.info(f"Core initialized in {mode} mode")
            return True
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {str(e)}")
            return False
    
    def _init_standard_mode(self):
        """Initialize standard operation mode"""
        workspace_path = Path.home() / '.kalighost' / 'workspaces'
        workspace_path.mkdir(parents=True, exist_ok=True)
        self.config['workspace'] = str(workspace_path)
        self.config['persistence'] = True
        self.config['encryption'] = False
    
    def _init_amnesic_mode(self):
        """Initialize amnesic mode - no disk traces"""
        import tempfile
        workspace_path = Path(tempfile.mkdtemp(prefix='kalighost_'))
        self.config['workspace'] = str(workspace_path)
        self.config['persistence'] = False
        self.config['encryption'] = False
        self.config['auto_wipe'] = True
        self.logger.warning("Amnesic mode enabled - all data will be lost on exit")
    
    def _init_encrypted_mode(self, passphrase: str):
        """Initialize encrypted persistence mode"""
        from backend.security.volumes import EncryptedVolume
        
        volume_path = Path.home() / '.kalighost' / 'encrypted_volume'
        volume = EncryptedVolume(volume_path, passphrase)
        
        if not volume.mount():
            raise RuntimeError("Failed to mount encrypted volume")
        
        workspace_path = volume.mount_point / 'workspaces'
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        self.config['workspace'] = str(workspace_path)
        self.config['persistence'] = True
        self.config['encryption'] = True
        self.config['volume'] = volume
        self.logger.info("Encrypted volume mounted successfully")
    
    def start_services(self) -> bool:
        """Start all backend services"""
        try:
            # Start API server
            from backend.api.server import APIServer
            self.api_server = APIServer(self)
            self.api_server.start()
            
            # Start WebSocket server
            from backend.api.websocket import WebSocketServer
            self.ws_server = WebSocketServer(self)
            self.ws_server.start()
            
            # Start agent if configured
            if self.config.get('auto_agent', False):
                self.load_agent()
            
            self.logger.info("All services started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start services: {str(e)}")
            return False
    
    def stop_services(self):
        """Stop all backend services"""
        self.logger.info("Stopping services...")
        
        # Unload agent
        if self.agent_status['loaded']:
            self.unload_agent()
        
        # Stop servers
        if hasattr(self, 'ws_server'):
            self.ws_server.stop()
        if hasattr(self, 'api_server'):
            self.api_server.stop()
        
        self.logger.info("All services stopped")
    
    def load_agent(self, model: str = 'uncensored-v1', gpu: bool = False) -> bool:
        """Load AI agent with specified model"""
        try:
            from yrays_agent.core import YraysAgent
            
            self.agent = YraysAgent(model=model, gpu=gpu)
            if self.agent.load():
                self.agent_status = {'loaded': True, 'model': model, 'gpu': gpu}
                self.logger.info(f"Agent loaded: {model}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to load agent: {str(e)}")
            return False
    
    def unload_agent(self):
        """Unload current AI agent"""
        if hasattr(self, 'agent') and self.agent_status['loaded']:
            self.agent.unload()
            self.agent_status = {'loaded': False, 'model': None}
            self.logger.info("Agent unloaded")
    
    def query_agent(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Send query to AI agent"""
        if not self.agent_status['loaded']:
            raise RuntimeError("No agent loaded")
        
        return self.agent.query(prompt, context)
    
    def create_project(self, name: str, encrypt: bool = False) -> Dict:
        """Create a new project workspace"""
        project = self.workspace_mgr.create_project(name, encrypt)
        self.active_projects[name] = project
        self.logger.info(f"Project created: {name}")
        return project
    
    def open_project(self, name: str) -> Dict:
        """Open existing project"""
        project = self.workspace_mgr.open_project(name)
        self.active_projects[name] = project
        self.logger.info(f"Project opened: {name}")
        return project
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'running': self.running,
            'mode': self.mode,
            'uptime': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            'agent': self.agent_status,
            'active_projects': list(self.active_projects.keys()),
            'workspace': self.config.get('workspace'),
            'encryption': self.config.get('encryption', False),
            'amnesic': self.mode == 'amnesic'
        }
    
    def cleanup(self):
        """Clean up resources before shutdown"""
        self.logger.info("Cleaning up resources...")
        
        # Stop services
        self.stop_services()
        
        # Wipe temp data in amnesic mode
        if self.mode == 'amnesic' and self.config.get('auto_wipe'):
            import shutil
            workspace = self.config.get('workspace')
            if workspace and Path(workspace).exists():
                shutil.rmtree(workspace, ignore_errors=True)
                self.logger.info("Temporary data wiped")
        
        # Unmount encrypted volume
        if self.mode == 'encrypted' and 'volume' in self.config:
            self.config['volume'].unmount()
        
        self.running = False
        self.logger.info("Cleanup complete")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

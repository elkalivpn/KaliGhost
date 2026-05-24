"""
config_manager_lite.py - Lightweight Configuration Manager (No Pydantic dependency)
"""

import os
import yaml
import json
import logging
from typing import Any, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigManagerLite:
    """Lightweight configuration manager without Pydantic"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager"""
        self.config_file = config_file or "config/kalighost_config.yaml"
        self.config: Dict[str, Any] = {}
        self.custom_agents: Dict[str, Dict] = {}
        self.custom_workflows: Dict[str, Dict] = {}
        self.load_configuration()
        
    def load_configuration(self) -> None:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                self.config = {}
    
    def _set_nested_value(self, path: str, value: Any) -> None:
        """Set nested configuration value"""
        keys = path.split(".")
        current = self.config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get configuration value by path"""
        keys = path.split(".")
        current = self.config
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, path: str, value: Any) -> None:
        """Set configuration value at runtime"""
        self._set_nested_value(path, value)
        logger.info(f"Configuration updated: {path} = {value}")
    
    def add_custom_agent(self, agent_id: str, config: Dict[str, Any]) -> None:
        """Add custom agent configuration"""
        self.custom_agents[agent_id] = config
        logger.info(f"Custom agent added: {agent_id}")
    
    def get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """Get agent configuration"""
        if agent_id in self.custom_agents:
            return self.custom_agents[agent_id]
        agent_path = f"agents.{agent_id}"
        return self.get(agent_path, {})
    
    def add_custom_workflow(self, workflow_id: str, workflow: Dict[str, Any]) -> None:
        """Add custom workflow"""
        self.custom_workflows[workflow_id] = workflow
        logger.info(f"Custom workflow added: {workflow_id}")
    
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow configuration"""
        if workflow_id in self.custom_workflows:
            return self.custom_workflows[workflow_id]
        workflow_path = f"workflows.custom.{workflow_id}"
        return self.get(workflow_path, {})
    
    def modify_system_prompt(self, agent_id: str, new_prompt: str) -> None:
        """Modify agent system prompt"""
        if agent_id in self.custom_agents:
            self.custom_agents[agent_id]["system_prompt"] = new_prompt
        else:
            prompt_path = f"agents.{agent_id}.system_prompt"
            self.set(prompt_path, new_prompt)
        logger.info(f"System prompt modified for {agent_id}")
    
    def modify_behavior(self, agent_id: str, **kwargs) -> None:
        """Modify agent behavior"""
        for key, value in kwargs.items():
            if agent_id in self.custom_agents:
                self.custom_agents[agent_id][key] = value
            else:
                param_path = f"agents.{agent_id}.{key}"
                self.set(param_path, value)
        logger.info(f"Behavior modified for {agent_id}: {kwargs}")
    
    def enable_feature(self, feature_path: str) -> None:
        """Enable a feature"""
        self.set(feature_path, True)
        logger.info(f"Feature enabled: {feature_path}")
    
    def disable_feature(self, feature_path: str) -> None:
        """Disable a feature"""
        self.set(feature_path, False)
        logger.info(f"Feature disabled: {feature_path}")
    
    def export_config(self, filepath: str) -> None:
        """Export configuration"""
        config_dict = {
            "system_config": self.config,
            "custom_agents": self.custom_agents,
            "custom_workflows": self.custom_workflows,
        }
        with open(filepath, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)
        logger.info(f"Configuration exported to {filepath}")
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        required_fields = ["core", "agents", "models"]
        for field in required_fields:
            if field not in self.config:
                logger.error(f"Missing required configuration: {field}")
                return False
        logger.info("Configuration validation passed")
        return True


# Global instance
_config_manager: Optional[ConfigManagerLite] = None


def get_config_manager() -> ConfigManagerLite:
    """Get or create configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManagerLite()
    return _config_manager


def configure_agent(agent_id: str, **kwargs) -> None:
    """Configure agent at runtime"""
    manager = get_config_manager()
    manager.modify_behavior(agent_id, **kwargs)


def update_system_prompt(agent_id: str, prompt: str) -> None:
    """Update system prompt"""
    manager = get_config_manager()
    manager.modify_system_prompt(agent_id, prompt)


def set_config_value(path: str, value: Any) -> None:
    """Set configuration value"""
    manager = get_config_manager()
    manager.set(path, value)


def get_config_value(path: str, default: Any = None) -> Any:
    """Get configuration value"""
    manager = get_config_manager()
    return manager.get(path, default)

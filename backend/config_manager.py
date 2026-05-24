"""
config_manager.py - Complete Configuration Management System

Handles all KaliGhost 3.0 configuration with full customization capabilities.
Supports YAML, JSON, environment variables, and runtime modifications.
"""

import os
import json
import yaml
import logging
from typing import Any, Dict, Optional
from pathlib import Path
from dataclasses import dataclass, asdict, field
from pydantic import BaseSettings, Field

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Individual agent configuration"""
    enabled: bool = True
    model: str = "gpt-4"
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 4096
    system_prompt: str = ""
    timeout_seconds: int = 300
    max_retries: int = 3


@dataclass
class ModelConfig:
    """Model configuration"""
    provider: str = "openai"
    api_key: str = ""
    model_name: str = "gpt-4"
    base_url: str = "https://api.openai.com/v1"
    timeout_seconds: int = 60
    max_retries: int = 3


class KaliGhostConfig(BaseSettings):
    """Complete KaliGhost configuration with full customization"""
    
    # Core settings
    app_name: str = Field("KaliGhost 3.0", description="Application name")
    version: str = Field("3.0.0", description="Application version")
    mode: str = Field("production", description="Execution mode")
    debug: bool = Field(False, description="Debug mode")
    
    # Logging
    log_level: str = Field("INFO", description="Logging level")
    log_file: str = Field("logs/kalighost.log", description="Log file path")
    
    # Database
    database_type: str = Field("sqlite", description="Database type")
    database_url: str = Field("sqlite:///./kalighost.db", description="Database URL")
    
    # Cache
    cache_enabled: bool = Field(True, description="Enable caching")
    cache_ttl: int = Field(3600, description="Cache TTL in seconds")
    
    # Security
    jwt_secret: str = Field("", description="JWT secret key")
    jwt_algorithm: str = Field("HS256", description="JWT algorithm")
    api_rate_limit: int = Field(1000, description="API rate limit")
    
    # Models
    model_provider: str = Field("openai", description="LLM provider")
    model_name: str = Field("gpt-4", description="LLM model name")
    model_temperature: float = Field(0.7, description="Model temperature")
    
    # Agents (fully customizable)
    enable_orchestrator: bool = Field(True, description="Enable orchestrator")
    enable_security: bool = Field(True, description="Enable security agent")
    enable_monetization: bool = Field(True, description="Enable monetization")
    enable_threats: bool = Field(True, description="Enable threat agent")
    enable_infrastructure: bool = Field(True, description="Enable infra agent")
    enable_compliance: bool = Field(True, description="Enable compliance agent")
    
    # Integrations
    stripe_enabled: bool = Field(True, description="Enable Stripe")
    stripe_api_key: str = Field("", description="Stripe API key")
    
    # UI
    webchat_port: int = Field(8001, description="WebChat port")
    api_port: int = Field(8000, description="API port")
    monitoring_port: int = Field(3001, description="Monitoring port")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields for custom config


class ConfigManager:
    """Manages all KaliGhost configurations"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager"""
        self.config_file = config_file or "config/kalighost_config.yaml"
        self.config: Dict[str, Any] = {}
        self.custom_agents: Dict[str, Dict] = {}
        self.custom_workflows: Dict[str, Dict] = {}
        self.load_configuration()
        
    def load_configuration(self) -> None:
        """Load configuration from file, environment, and defaults"""
        # Load from YAML file
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f) or {}
            logger.info(f"Loaded configuration from {self.config_file}")
        
        # Override with environment variables
        self._load_env_overrides()
        
    def _load_env_overrides(self) -> None:
        """Override configuration with environment variables"""
        env_mapping = {
            "KALIGHOST_MODE": "core.mode",
            "KALIGHOST_DEBUG": "core.debug",
            "KALIGHOST_LOG_LEVEL": "core.logging.level",
            "OPENAI_API_KEY": "models.primary.api_key",
            "STRIPE_API_KEY": "integrations.stripe.api_key",
            "JWT_SECRET": "security.auth.jwt_secret",
            "DATABASE_URL": "memory.database.connection_string",
        }
        
        for env_var, config_path in env_mapping.items():
            if env_var in os.environ:
                self._set_nested_value(config_path, os.environ[env_var])
                logger.info(f"Override from env: {env_var}")
    
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
        """Get agent configuration (custom or default)"""
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
        """Modify agent behavior (temperature, timeout, retries, etc.)"""
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
    
    def get_all_configs(self) -> Dict[str, Any]:
        """Get all configurations"""
        return {
            "system_config": self.config,
            "custom_agents": self.custom_agents,
            "custom_workflows": self.custom_workflows,
        }
    
    def export_config(self, filepath: str) -> None:
        """Export current configuration to file"""
        with open(filepath, 'w') as f:
            yaml.dump(self.get_all_configs(), f, default_flow_style=False)
        logger.info(f"Configuration exported to {filepath}")
    
    def import_config(self, filepath: str) -> None:
        """Import configuration from file"""
        with open(filepath, 'r') as f:
            imported = yaml.safe_load(f)
        
        self.config.update(imported.get("system_config", {}))
        self.custom_agents.update(imported.get("custom_agents", {}))
        self.custom_workflows.update(imported.get("custom_workflows", {}))
        logger.info(f"Configuration imported from {filepath}")
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        required_fields = ["core", "agents", "models"]
        
        for field in required_fields:
            if field not in self.config:
                logger.error(f"Missing required configuration: {field}")
                return False
        
        logger.info("Configuration validation passed")
        return True
    
    def print_config(self, section: Optional[str] = None) -> None:
        """Print configuration for debugging"""
        if section:
            config_to_print = self.get(section, {})
            section_name = section
        else:
            config_to_print = self.config
            section_name = "All Configurations"
        
        print(f"\n{'='*60}")
        print(f"📋 {section_name}")
        print(f"{'='*60}")
        print(yaml.dump(config_to_print, default_flow_style=False))


# Singleton instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get or create configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def configure_agent(agent_id: str, **kwargs) -> None:
    """Convenient function to configure agent at runtime"""
    manager = get_config_manager()
    manager.modify_behavior(agent_id, **kwargs)


def update_system_prompt(agent_id: str, prompt: str) -> None:
    """Convenient function to update system prompt"""
    manager = get_config_manager()
    manager.modify_system_prompt(agent_id, prompt)


def set_config_value(path: str, value: Any) -> None:
    """Convenient function to set any configuration value"""
    manager = get_config_manager()
    manager.set(path, value)


def get_config_value(path: str, default: Any = None) -> Any:
    """Convenient function to get any configuration value"""
    manager = get_config_manager()
    return manager.get(path, default)


if __name__ == "__main__":
    # Example usage
    manager = get_config_manager()
    
    # Print current configuration
    manager.print_config("agents")
    
    # Modify agent behavior
    manager.modify_behavior(
        "security_agent",
        temperature=0.3,
        timeout_seconds=600,
        max_retries=5
    )
    
    # Update system prompt
    manager.modify_system_prompt(
        "orchestrator",
        "You are a specialized orchestrator. Be more aggressive in task decomposition."
    )
    
    # Add custom agent
    manager.add_custom_agent("custom_agent", {
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "system_prompt": "Custom agent prompt"
    })
    
    # Add custom workflow
    manager.add_custom_workflow("custom_workflow", {
        "name": "Custom Workflow",
        "steps": [
            {"agent": "custom_agent", "task": "Do something"}
        ]
    })
    
    # Export configuration
    manager.export_config("config/custom_config.yaml")
    
    print("\n✅ Configuration system ready!")

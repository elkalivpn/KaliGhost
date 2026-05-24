"""
KaliGhost 3.0 Backend Modules

All modules are 100% customizable at runtime.
"""

from backend.config_manager_lite import (
    get_config_manager,
    configure_agent,
    update_system_prompt,
    set_config_value,
    get_config_value,
)

__all__ = [
    "get_config_manager",
    "configure_agent",
    "update_system_prompt",
    "set_config_value",
    "get_config_value",
]

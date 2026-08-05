"""
KaliGhost 4.0 ULTIMATE - Hybrid Dual-Core Architecture
=======================================================
Núcleo Fantasma: Operaciones ofensivas, ejecución en RAM, steganografía
Núcleo Legítimo: Fachada corporativa, camuflaje, gestión
"""

from .config_loader import ConfigLoader
from .security import SecurityManager
from .logger import GhostLogger

__version__ = "4.0-ULTIMATE"
__author__ = "KaliGhost Team"

__all__ = [
    "ConfigLoader",
    "SecurityManager", 
    "GhostLogger"
]

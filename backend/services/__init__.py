"""
Services Module Package
Core services for process, workspace, and security operations
"""

from backend.services.process_manager import ProcessManager
from backend.services.workspace_manager import WorkspaceManager

__all__ = ['ProcessManager', 'WorkspaceManager']

"""
Workspace Manager Module
Project and workspace management with encryption support
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class WorkspaceManager:
    """
    Manages project workspaces in KaliGhost IDE
    Handles creation, deletion, and encryption of project directories
    """
    
    def __init__(self, base_path: str = None):
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path.home() / '.kalighost' / 'workspaces'
        
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.projects_file = self.base_path / 'projects.json'
        self._load_projects_index()
    
    def _load_projects_index(self):
        """Load projects index from disk"""
        if self.projects_file.exists():
            with open(self.projects_file, 'r') as f:
                self.projects_index = json.load(f)
        else:
            self.projects_index = {}
    
    def _save_projects_index(self):
        """Save projects index to disk"""
        with open(self.projects_file, 'w') as f:
            json.dump(self.projects_index, f, indent=2)
    
    def create_project(self, name: str, encrypt: bool = False,
                       description: str = '') -> Dict:
        """
        Create a new project workspace
        
        Args:
            name: Project name
            encrypt: Enable encryption for this project
            description: Project description
            
        Returns:
            Project metadata dictionary
        """
        # Validate name
        if not name or not name.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Invalid project name")
        
        # Check if exists
        if name in self.projects_index:
            raise ValueError(f"Project '{name}' already exists")
        
        # Create directory
        project_path = self.base_path / name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create standard project structure
        subdirs = ['src', 'docs', 'config', 'tools', 'output', 'logs']
        for subdir in subdirs:
            (project_path / subdir).mkdir(exist_ok=True)
        
        # Create project metadata
        metadata = {
            'name': name,
            'path': str(project_path),
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'encrypted': encrypt,
            'description': description,
            'files': [],
            'tags': []
        }
        
        # Save metadata file in project
        meta_file = project_path / '.project.json'
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update index
        self.projects_index[name] = metadata
        self._save_projects_index()
        
        return metadata
    
    def open_project(self, identifier: str) -> Dict:
        """
        Open an existing project
        
        Args:
            identifier: Project name or path
            
        Returns:
            Project metadata
        """
        # Try by name first
        if identifier in self.projects_index:
            project = self.projects_index[identifier]
            project_path = Path(project['path'])
            
            if not project_path.exists():
                raise ValueError(f"Project path not found: {project_path}")
            
            # Update modified time
            project['modified'] = datetime.now().isoformat()
            self._save_projects_index()
            
            return project
        
        # Try by path
        path = Path(identifier)
        if path.exists() and (path / '.project.json').exists():
            with open(path / '.project.json', 'r') as f:
                metadata = json.load(f)
            
            name = metadata['name']
            self.projects_index[name] = metadata
            self._save_projects_index()
            
            return metadata
        
        raise ValueError(f"Project not found: {identifier}")
    
    def delete_project(self, name: str, force: bool = False) -> bool:
        """
        Delete a project
        
        Args:
            name: Project name
            force: Force deletion without confirmation
            
        Returns:
            Success status
        """
        if name not in self.projects_index:
            return False
        
        project = self.projects_index[name]
        project_path = Path(project['path'])
        
        # Remove directory
        if project_path.exists():
            shutil.rmtree(project_path, ignore_errors=True)
        
        # Remove from index
        del self.projects_index[name]
        self._save_projects_index()
        
        return True
    
    def list_projects(self) -> List[Dict]:
        """List all projects"""
        self._load_projects_index()
        return [
            {
                'name': p['name'],
                'path': p['path'],
                'created': p['created'],
                'modified': p['modified'],
                'encrypted': p['encrypted'],
                'description': p.get('description', '')
            }
            for p in self.projects_index.values()
        ]
    
    def update_project(self, name: str, **kwargs) -> Dict:
        """
        Update project metadata
        
        Args:
            name: Project name
            **kwargs: Fields to update
            
        Returns:
            Updated project metadata
        """
        if name not in self.projects_index:
            raise ValueError(f"Project not found: {name}")
        
        project = self.projects_index[name]
        
        # Update fields
        for key, value in kwargs.items():
            if key in ['description', 'tags']:
                project[key] = value
        
        project['modified'] = datetime.now().isoformat()
        
        # Save to disk
        project_path = Path(project['path'])
        meta_file = project_path / '.project.json'
        with open(meta_file, 'w') as f:
            json.dump(project, f, indent=2)
        
        # Update index
        self.projects_index[name] = project
        self._save_projects_index()
        
        return project
    
    def add_file_to_project(self, project_name: str, file_path: str,
                            category: str = 'general') -> bool:
        """Add a file reference to project"""
        if project_name not in self.projects_index:
            return False
        
        project = self.projects_index[project_name]
        file_entry = {
            'path': file_path,
            'category': category,
            'added': datetime.now().isoformat()
        }
        
        if 'files' not in project:
            project['files'] = []
        
        project['files'].append(file_entry)
        project['modified'] = datetime.now().isoformat()
        
        self._save_projects_index()
        return True
    
    def export_project(self, name: str, output_path: str = None) -> str:
        """
        Export project to archive
        
        Args:
            name: Project name
            output_path: Output path (optional)
            
        Returns:
            Path to exported archive
        """
        if name not in self.projects_index:
            raise ValueError(f"Project not found: {name}")
        
        project = self.projects_index[name]
        project_path = Path(project['path'])
        
        if not output_path:
            output_path = f"{name}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
        
        # Create tar.gz archive
        import tarfile
        
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(project_path, arcname=name)
        
        return output_path
    
    def get_project_stats(self, name: str) -> Dict:
        """Get project statistics"""
        if name not in self.projects_index:
            return {}
        
        project = self.projects_index[name]
        project_path = Path(project['path'])
        
        # Count files
        total_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk(project_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if not file.startswith('.'):
                    total_files += 1
                    file_path = Path(root) / file
                    total_size += file_path.stat().st_size
        
        return {
            'name': name,
            'total_files': total_files,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'created': project['created'],
            'modified': project['modified']
        }

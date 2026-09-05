"""
API Server Module
RESTful API for KaliGhost IDE backend
"""

import asyncio
import json
from typing import Dict, Any, Optional
from aiohttp import web
from datetime import datetime


class APIServer:
    """
    REST API Server for KaliGhost IDE
    Provides HTTP endpoints for all IDE functionality
    """
    
    def __init__(self, core):
        self.core = core
        self.app = web.Application()
        self.runner: Optional[web.AppRunner] = None
        self.port = 8080
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        self.app.router.add_get('/api/v1/status', self.get_status)
        self.app.router.add_get('/api/v1/health', self.health_check)
        
        # Agent endpoints
        self.app.router.add_get('/api/v1/agent/status', self.agent_status)
        self.app.router.add_post('/api/v1/agent/load', self.agent_load)
        self.app.router.add_post('/api/v1/agent/unload', self.agent_unload)
        self.app.router.add_post('/api/v1/agent/query', self.agent_query)
        
        # Project endpoints
        self.app.router.add_get('/api/v1/projects', self.list_projects)
        self.app.router.add_post('/api/v1/projects', self.create_project)
        self.app.router.add_get('/api/v1/projects/{name}', self.get_project)
        self.app.router.add_delete('/api/v1/projects/{name}', self.delete_project)
        
        # Sandbox endpoints
        self.app.router.add_post('/api/v1/sandbox/analyze', self.analyze_sample)
        
        # Purple team endpoints
        self.app.router.add_post('/api/v1/purple-team/scan', self.purple_team_scan)
        
        # System endpoints
        self.app.router.add_post('/api/v1/system/shutdown', self.shutdown)
    
    async def get_status(self, request: web.Request) -> web.Response:
        """Get system status"""
        status = self.core.get_status()
        return web.json_response({
            'success': True,
            'data': status
        })
    
    async def health_check(self, request: web.Request) -> web.Response:
        """Health check endpoint"""
        return web.json_response({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        })
    
    async def agent_status(self, request: web.Request) -> web.Response:
        """Get AI agent status"""
        return web.json_response({
            'success': True,
            'data': self.core.agent_status
        })
    
    async def agent_load(self, request: web.Request) -> web.Response:
        """Load AI agent"""
        try:
            data = await request.json()
            model = data.get('model', 'uncensored-v1')
            gpu = data.get('gpu', False)
            
            success = self.core.load_agent(model=model, gpu=gpu)
            
            return web.json_response({
                'success': success,
                'message': 'Agent loaded' if success else 'Failed to load agent'
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def agent_unload(self, request: web.Request) -> web.Response:
        """Unload AI agent"""
        self.core.unload_agent()
        return web.json_response({
            'success': True,
            'message': 'Agent unloaded'
        })
    
    async def agent_query(self, request: web.Request) -> web.Response:
        """Query AI agent"""
        try:
            data = await request.json()
            prompt = data.get('prompt', '')
            context = data.get('context', {})
            
            if not prompt:
                return web.json_response({
                    'success': False,
                    'error': 'Prompt required'
                }, status=400)
            
            response = self.core.query_agent(prompt, context)
            
            return web.json_response({
                'success': True,
                'data': {'response': response}
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def list_projects(self, request: web.Request) -> web.Response:
        """List all projects"""
        projects = self.core.workspace_mgr.list_projects()
        return web.json_response({
            'success': True,
            'data': projects
        })
    
    async def create_project(self, request: web.Request) -> web.Response:
        """Create new project"""
        try:
            data = await request.json()
            name = data.get('name')
            encrypt = data.get('encrypt', False)
            description = data.get('description', '')
            
            if not name:
                return web.json_response({
                    'success': False,
                    'error': 'Project name required'
                }, status=400)
            
            project = self.core.create_project(name, encrypt=encrypt)
            
            return web.json_response({
                'success': True,
                'data': project
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def get_project(self, request: web.Request) -> web.Response:
        """Get project details"""
        name = request.match_info['name']
        
        try:
            project = self.core.open_project(name)
            return web.json_response({
                'success': True,
                'data': project
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=404)
    
    async def delete_project(self, request: web.Request) -> web.Response:
        """Delete project"""
        name = request.match_info['name']
        
        success = self.core.workspace_mgr.delete_project(name)
        
        return web.json_response({
            'success': success,
            'message': 'Project deleted' if success else 'Failed to delete'
        })
    
    async def analyze_sample(self, request: web.Request) -> web.Response:
        """Analyze malware sample"""
        try:
            # Handle file upload
            reader = await request.multipart()
            field = await reader.next()
            
            if not field or field.name != 'sample':
                return web.json_response({
                    'success': False,
                    'error': 'No sample file provided'
                }, status=400)
            
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as f:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk:
                        break
                    f.write(chunk)
                temp_path = f.name
            
            # Analyze
            from backend.services.sandbox import MalwareSandbox
            sandbox = MalwareSandbox()
            results = sandbox.analyze(temp_path)
            sandbox.cleanup()
            
            # Cleanup temp file
            import os
            os.unlink(temp_path)
            
            return web.json_response({
                'success': True,
                'data': results
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def purple_team_scan(self, request: web.Request) -> web.Response:
        """Execute purple team operation"""
        try:
            data = await request.json()
            target = data.get('target')
            mode = data.get('mode', 'recon')
            stealth = data.get('stealth', False)
            
            if not target:
                return web.json_response({
                    'success': False,
                    'error': 'Target required'
                }, status=400)
            
            from backend.services.purple_team import PurpleTeamOps
            ops = PurpleTeamOps(stealth=stealth)
            
            if mode == 'full':
                results = ops.full_operation(target)
            elif mode == 'recon':
                results = ops.reconnaissance(target)
            elif mode == 'exploit':
                results = ops.exploitation(target)
            else:
                results = ops.post_exploitation(target)
            
            return web.json_response({
                'success': True,
                'data': results
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def shutdown(self, request: web.Request) -> web.Response:
        """Shutdown the IDE"""
        asyncio.create_task(self._delayed_shutdown())
        return web.json_response({
            'success': True,
            'message': 'Shutting down...'
        })
    
    async def _delayed_shutdown(self):
        """Delayed shutdown to allow response to be sent"""
        await asyncio.sleep(1)
        self.stop()
    
    def start(self):
        """Start the API server"""
        async def _start():
            self.runner = web.AppRunner(self.app)
            await self.runner.setup()
            site = web.TCPSite(self.runner, '0.0.0.0', self.port)
            await site.start()
            print(f"[*] API server started on port {self.port}")
        
        asyncio.run(_start())
    
    def stop(self):
        """Stop the API server"""
        if self.runner:
            async def _stop():
                await self.runner.cleanup()
            
            asyncio.run(_stop())
            print("[*] API server stopped")

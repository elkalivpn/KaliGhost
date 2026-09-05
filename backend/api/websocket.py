"""
WebSocket Server Module
Real-time bidirectional communication for IDE features
"""

import asyncio
import json
from typing import Dict, Set, Any, Optional
from aiohttp import web, WSMsgType
from datetime import datetime


class WebSocketServer:
    """
    WebSocket server for real-time communication
    Handles live updates, agent interactions, and collaborative features
    """
    
    def __init__(self, core):
        self.core = core
        self.app = web.Application()
        self.runner: Optional[web.AppRunner] = None
        self.port = 8081
        
        # Connected clients
        self.clients: Set[web.WebSocketResponse] = set()
        self.client_info: Dict[web.WebSocketResponse, Dict] = {}
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup WebSocket routes"""
        self.app.router.add_get('/ws', self.websocket_handler)
        self.app.router.add_get('/ws/agent', self.agent_websocket_handler)
        self.app.router.add_get('/ws/terminal/{session_id}', self.terminal_handler)
    
    async def websocket_handler(self, request: web.Request) -> web.WebSocketResponse:
        """Main WebSocket handler"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        # Add to clients
        self.clients.add(ws)
        self.client_info[ws] = {
            'type': 'main',
            'connected': datetime.now().isoformat(),
            'authenticated': False
        }
        
        # Send welcome message
        await ws.send_json({
            'type': 'welcome',
            'message': 'Connected to KaliGhost WebSocket',
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    await self._handle_message(ws, msg.data)
                elif msg.type == WSMsgType.BINARY:
                    await self._handle_binary(ws, msg.data)
                elif msg.type == WSMsgType.ERROR:
                    break
                    
        finally:
            self.clients.discard(ws)
            self.client_info.pop(ws, None)
        
        return ws
    
    async def agent_websocket_handler(self, request: web.Request) -> web.WebSocketResponse:
        """Dedicated WebSocket for AI agent communication"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.clients.add(ws)
        self.client_info[ws] = {
            'type': 'agent',
            'connected': datetime.now().isoformat()
        }
        
        await ws.send_json({
            'type': 'agent_ready',
            'status': self.core.agent_status
        })
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    await self._handle_agent_query(ws, msg.data)
                elif msg.type == WSMsgType.ERROR:
                    break
        finally:
            self.clients.discard(ws)
            self.client_info.pop(ws, None)
        
        return ws
    
    async def terminal_handler(self, request: web.Request) -> web.WebSocketResponse:
        """WebSocket handler for terminal sessions"""
        session_id = request.match_info['session_id']
        
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.clients.add(ws)
        self.client_info[ws] = {
            'type': 'terminal',
            'session_id': session_id,
            'connected': datetime.now().isoformat()
        }
        
        # Initialize terminal session
        await self._init_terminal_session(session_id, ws)
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    await self._handle_terminal_input(session_id, ws, msg.data)
                elif msg.type == WSMsgType.ERROR:
                    break
        finally:
            self.clients.discard(ws)
            self.client_info.pop(ws, None)
            await self._cleanup_terminal_session(session_id)
        
        return ws
    
    async def _handle_message(self, ws: web.WebSocketResponse, data: str):
        """Handle incoming text message"""
        try:
            message = json.loads(data)
            msg_type = message.get('type')
            
            if msg_type == 'ping':
                await ws.send_json({'type': 'pong', 'timestamp': datetime.now().isoformat()})
            
            elif msg_type == 'subscribe':
                channel = message.get('channel')
                await ws.send_json({
                    'type': 'subscribed',
                    'channel': channel
                })
            
            elif msg_type == 'command':
                command = message.get('command')
                # Execute command and stream results
                await self._execute_and_stream(ws, command)
            
        except json.JSONDecodeError:
            await ws.send_json({
                'type': 'error',
                'message': 'Invalid JSON'
            })
    
    async def _handle_binary(self, ws: web.WebSocketResponse, data: bytes):
        """Handle binary data (file transfers, etc.)"""
        # Implement file transfer logic
        pass
    
    async def _handle_agent_query(self, ws: web.WebSocketResponse, data: str):
        """Handle AI agent query via WebSocket"""
        try:
            message = json.loads(data)
            prompt = message.get('prompt', '')
            
            if not self.core.agent_status['loaded']:
                await ws.send_json({
                    'type': 'error',
                    'message': 'No agent loaded'
                })
                return
            
            # Stream response
            await ws.send_json({
                'type': 'thinking',
                'status': 'processing'
            })
            
            response = self.core.query_agent(prompt)
            
            await ws.send_json({
                'type': 'response',
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            await ws.send_json({
                'type': 'error',
                'message': str(e)
            })
    
    async def _init_terminal_session(self, session_id: str, ws: web.WebSocketResponse):
        """Initialize terminal session"""
        # Would create PTY or connect to container
        await ws.send_json({
            'type': 'terminal_init',
            'session_id': session_id,
            'status': 'ready'
        })
    
    async def _handle_terminal_input(self, session_id: str, ws: web.WebSocketResponse, 
                                      data: str):
        """Handle terminal input"""
        message = json.loads(data)
        input_data = message.get('input', '')
        
        # Would send to PTY and capture output
        # For now, echo back
        await ws.send_json({
            'type': 'output',
            'data': f"[echo] {input_data}"
        })
    
    async def _cleanup_terminal_session(self, session_id: str):
        """Cleanup terminal session"""
        # Close PTY, cleanup resources
        pass
    
    async def _execute_and_stream(self, ws: web.WebSocketResponse, command: str):
        """Execute command and stream output"""
        await ws.send_json({
            'type': 'executing',
            'command': command
        })
        
        # Would execute and stream in real implementation
        await ws.send_json({
            'type': 'output',
            'data': f"Command executed: {command}"
        })
    
    async def broadcast(self, message: Dict, exclude: Optional[web.WebSocketResponse] = None):
        """Broadcast message to all connected clients"""
        if not self.clients:
            return
        
        data = json.dumps(message)
        
        disconnected = []
        for client in self.clients:
            if client != exclude and not client.closed:
                try:
                    await client.send_str(data)
                except:
                    disconnected.append(client)
        
        # Clean up disconnected clients
        for client in disconnected:
            self.clients.discard(client)
            self.client_info.pop(client, None)
    
    async def send_to_channel(self, channel: str, message: Dict):
        """Send message to specific channel/subscribers"""
        # Implement channel-based messaging
        pass
    
    def start(self):
        """Start WebSocket server"""
        async def _start():
            self.runner = web.AppRunner(self.app)
            await self.runner.setup()
            site = web.TCPSite(self.runner, '0.0.0.0', self.port)
            await site.start()
            print(f"[*] WebSocket server started on port {self.port}")
        
        asyncio.run(_start())
    
    def stop(self):
        """Stop WebSocket server"""
        if self.runner:
            async def _stop():
                # Close all connections
                for client in list(self.clients):
                    await client.close()
                
                await self.runner.cleanup()
            
            asyncio.run(_stop())
            print("[*] WebSocket server stopped")
    
    def get_connected_count(self) -> int:
        """Get number of connected clients"""
        return len(self.clients)

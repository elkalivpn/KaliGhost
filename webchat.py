#!/usr/bin/env python3
"""
🐉 KaliGhost WebChat + 3D Dragon Interface
Unified web interface with real-time streaming and 3D visualization
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="KaliGhost WebChat")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()


# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """Main chat WebSocket endpoint"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            logger.info(f"💬 Received: {message.get('content', '')[:50]}")
            
            # Process with orchestrator
            from backend.orchestrator import get_orchestrator, AgentMode
            
            orchestrator = get_orchestrator()
            
            # Streaming response
            await websocket.send_json({
                "type": "status",
                "content": "🚀 Decomposing task...",
                "dragon_mode": "ACTIVE"
            })
            
            # Decompose task
            plan = await orchestrator.decompose_task(
                task=message.get('content'),
                thread_id=message.get('thread_id', 'webchat'),
                mode=AgentMode(message.get('mode', 'standard'))
            )
            
            # Stream plan details
            await websocket.send_json({
                "type": "plan",
                "plan_id": plan.id,
                "sub_tasks": len(plan.sub_tasks),
                "strategy": plan.decomposition_strategy
            })
            
            # Execute plan with real-time updates
            result = await orchestrator.execute_plan(plan)
            
            # Final response
            await websocket.send_json({
                "type": "complete",
                "status": result['status'],
                "execution_time_ms": result['execution_time_ms'],
                "dragon_mode": "SUCCESS",
                "results": result['results']
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("💔 Client disconnected")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        await websocket.send_json({
            "type": "error",
            "error": str(e),
            "dragon_mode": "ERROR"
        })


# ============================================================================
# HTML INTERFACE (WEBCHAT + 3D DRAGON)
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    """Main web interface with 3D dragon and chat"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🐉 KaliGhost 3.0</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.js"></script>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
                color: #00ff88;
                overflow: hidden;
                height: 100vh;
            }
            
            #container {
                display: flex;
                height: 100vh;
            }
            
            #canvas {
                flex: 1;
                background: radial-gradient(ellipse at center, #1a1a2e 0%, #0a0a0a 100%);
                position: relative;
            }
            
            #dragon-status {
                position: absolute;
                top: 20px;
                left: 20px;
                background: rgba(0, 255, 136, 0.1);
                border: 2px solid #00ff88;
                padding: 15px;
                border-radius: 5px;
                font-size: 12px;
            }
            
            .status-dot {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 1s infinite;
            }
            
            .status-idle { background-color: #00ff88; }
            .status-active { background-color: #ffaa00; animation: pulse-fast 0.5s infinite; }
            .status-error { background-color: #ff0055; }
            .status-success { background-color: #00ff88; }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            @keyframes pulse-fast {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            
            #chatbox {
                width: 400px;
                background: #0a0a0a;
                border-left: 2px solid #00ff88;
                display: flex;
                flex-direction: column;
                padding: 20px;
            }
            
            #messages {
                flex: 1;
                overflow-y: auto;
                margin-bottom: 15px;
                border: 1px solid #003311;
                padding: 10px;
                background: rgba(0, 0, 0, 0.5);
                border-radius: 3px;
            }
            
            .message {
                margin-bottom: 10px;
                padding: 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            
            .message-user {
                background: rgba(0, 255, 136, 0.1);
                border-left: 3px solid #00ff88;
                color: #00ff88;
            }
            
            .message-agent {
                background: rgba(0, 100, 255, 0.1);
                border-left: 3px solid #0064ff;
                color: #00ccff;
            }
            
            .message-system {
                background: rgba(255, 170, 0, 0.1);
                border-left: 3px solid #ffaa00;
                color: #ffaa00;
            }
            
            #input-area {
                display: flex;
                gap: 8px;
            }
            
            #message-input {
                flex: 1;
                background: rgba(0, 255, 136, 0.05);
                border: 1px solid #00ff88;
                color: #00ff88;
                padding: 8px;
                font-family: 'Courier New', monospace;
                border-radius: 3px;
                font-size: 12px;
            }
            
            #message-input::placeholder {
                color: #00663344;
            }
            
            #send-btn {
                background: linear-gradient(135deg, #00ff88 0%, #00cc66 100%);
                border: none;
                color: #000;
                padding: 8px 15px;
                cursor: pointer;
                border-radius: 3px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                transition: all 0.3s;
            }
            
            #send-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 0 10px #00ff88;
            }
            
            .loading {
                text-align: center;
                color: #ffaa00;
                font-size: 12px;
                margin: 5px 0;
            }
            
            .spinner {
                display: inline-block;
                width: 8px;
                height: 8px;
                margin: 0 3px;
                background: #ffaa00;
                border-radius: 50%;
                animation: spinner 1s infinite;
            }
            
            @keyframes spinner {
                0% { transform: scale(0); opacity: 1; }
                100% { transform: scale(1); opacity: 0; }
            }
        </style>
    </head>
    <body>
        <div id="container">
            <canvas id="canvas"></canvas>
            <div id="chatbox">
                <h2 style="margin-bottom: 15px; color: #00ff88;">🐉 KaliGhost Chat</h2>
                <div id="dragon-status">
                    <div><span class="status-dot status-idle"></span>Dragon Status: <span id="status-text">IDLE</span></div>
                    <div style="margin-top: 5px; font-size: 10px;">Mode: <span id="mode-text">READY</span></div>
                </div>
                <div id="messages"></div>
                <div id="input-area">
                    <input 
                        type="text" 
                        id="message-input" 
                        placeholder="Describe what you want to build..."
                        autocomplete="off"
                    >
                    <button id="send-btn">Send</button>
                </div>
            </div>
        </div>

        <script>
            // THREE.JS 3D DRAGON SETUP
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a0a0a);
            
            const canvas = document.getElementById('canvas');
            const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
            renderer.setSize(canvas.clientWidth, canvas.clientHeight);
            renderer.shadowMap.enabled = true;
            
            camera.position.set(0, 2, 5);
            camera.lookAt(0, 0, 0);
            
            // Lighting
            const light = new THREE.DirectionalLight(0x00ff88, 1);
            light.position.set(5, 5, 5);
            light.castShadow = true;
            scene.add(light);
            
            const ambientLight = new THREE.AmbientLight(0x0064ff, 0.5);
            scene.add(ambientLight);
            
            // CREATE DRAGON (Simplified 3D model)
            const dragonGroup = new THREE.Group();
            scene.add(dragonGroup);
            
            // Dragon body
            const bodyGeometry = new THREE.BoxGeometry(1.5, 1, 2);
            const bodyMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x00ff88,
                emissive: 0x004422,
                shininess: 100
            });
            const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
            body.castShadow = true;
            dragonGroup.add(body);
            
            // Dragon head
            const headGeometry = new THREE.SphereGeometry(0.5, 32, 32);
            const head = new THREE.Mesh(headGeometry, bodyMaterial);
            head.position.set(0, 0.3, -1);
            head.castShadow = true;
            dragonGroup.add(head);
            
            // Dragon eyes (glowing)
            const eyeGeometry = new THREE.SphereGeometry(0.15, 32, 32);
            const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
            
            const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
            leftEye.position.set(-0.2, 0.6, -1.3);
            dragonGroup.add(leftEye);
            
            const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
            rightEye.position.set(0.2, 0.6, -1.3);
            dragonGroup.add(rightEye);
            
            // Dragon tail
            const tailGeometry = new THREE.ConeGeometry(0.3, 2, 32);
            const tail = new THREE.Mesh(tailGeometry, bodyMaterial);
            tail.position.set(0, 0, 1.5);
            tail.rotation.z = Math.PI / 4;
            tail.castShadow = true;
            dragonGroup.add(tail);
            
            // WEBCHAT
            const messagesDiv = document.getElementById('messages');
            const inputField = document.getElementById('message-input');
            const sendBtn = document.getElementById('send-btn');
            const statusText = document.getElementById('status-text');
            const modeText = document.getElementById('mode-text');
            
            let ws = new WebSocket(`ws://${window.location.host}/ws/chat`);
            
            ws.onopen = () => {
                addMessage('System', 'Connected to KaliGhost 🐉', 'system');
            };
            
            ws.onmessage = (event) => {
                const response = JSON.parse(event.data);
                
                if (response.type === 'status') {
                    addMessage('Dragon', response.content, 'agent');
                    updateDragonStatus(response.dragon_mode);
                    animateDragon('thinking');
                } else if (response.type === 'plan') {
                    addMessage('Dragon', `📋 Planning: ${response.sub_tasks} sub-tasks (${response.strategy})`, 'agent');
                    updateDragonStatus('BUSY');
                    animateDragon('busy');
                } else if (response.type === 'complete') {
                    addMessage('Dragon', `✅ Task complete! (${response.execution_time_ms.toFixed(0)}ms)`, 'agent');
                    updateDragonStatus(response.dragon_mode);
                    animateDragon('success');
                } else if (response.type === 'error') {
                    addMessage('Dragon', `❌ Error: ${response.error}`, 'agent');
                    updateDragonStatus('ERROR');
                    animateDragon('error');
                }
            };
            
            ws.onerror = () => {
                addMessage('System', 'Connection error', 'system');
            };
            
            function addMessage(sender, content, type) {
                const msgDiv = document.createElement('div');
                msgDiv.className = `message message-${type}`;
                msgDiv.textContent = `${sender}: ${content}`;
                messagesDiv.appendChild(msgDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            function updateDragonStatus(mode) {
                statusText.textContent = mode;
                modeText.textContent = mode;
                const dot = document.querySelector('.status-dot');
                dot.className = `status-dot status-${mode.toLowerCase()}`;
            }
            
            function animateDragon(mode) {
                if (mode === 'thinking') {
                    body.rotation.y += 0.02;
                } else if (mode === 'busy') {
                    body.rotation.x += 0.01;
                    body.rotation.y += 0.03;
                } else if (mode === 'success') {
                    body.scale.set(1.2, 1.2, 1.2);
                    setTimeout(() => body.scale.set(1, 1, 1), 200);
                }
            }
            
            sendBtn.onclick = () => {
                const message = inputField.value.trim();
                if (!message) return;
                
                addMessage('You', message, 'user');
                
                ws.send(JSON.stringify({
                    content: message,
                    thread_id: 'webchat',
                    mode: 'standard'
                }));
                
                inputField.value = '';
                updateDragonStatus('ACTIVE');
            };
            
            inputField.onkeypress = (e) => {
                if (e.key === 'Enter') sendBtn.click();
            };
            
            // Animation loop
            function animate() {
                requestAnimationFrame(animate);
                
                // Slow dragon rotation when idle
                if (statusText.textContent === 'IDLE') {
                    dragonGroup.rotation.y += 0.005;
                }
                
                renderer.render(scene, camera);
            }
            animate();
            
            // Handle window resize
            window.addEventListener('resize', () => {
                camera.aspect = canvas.clientWidth / canvas.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(canvas.clientWidth, canvas.clientHeight);
            });
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

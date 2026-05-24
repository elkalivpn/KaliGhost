#!/usr/bin/env python3
"""
🐉 KaliGhost 3.0 Integration Layer
Unified gateway connecting orchestrator, memory, sandbox, and IM channels
FastAPI backend compatible with enhanced KaliGhost capabilities
"""

import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
from datetime import datetime
import logging

# Import our new modules
from orchestrator import (
    get_orchestrator, AgentMode, SubAgentTask,
    OrchestrationPlan
)
from memory_system import get_memory_system
from im_channels import (
    get_im_manager, IMMessage, IMResponse,
    TelegramChannel, SlackChannel, FeishuChannel, WeChatChannel
)
from enhanced_sandbox import (
    get_sandbox_manager, SandboxConfig, SandboxMode
)

logger = logging.getLogger(__name__)


# ============================================================================
# Pydantic Models (API Request/Response)
# ============================================================================

class ChatRequest(BaseModel):
    """Chat/task request"""
    message: str
    thread_id: str
    mode: str = "standard"  # flash, standard, pro, ultra
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Chat response"""
    thread_id: str
    response: str
    mode: str
    plan_id: Optional[str] = None
    sub_task_count: int = 0
    execution_time_ms: float


class MemoryRequest(BaseModel):
    """Memory operation request"""
    category: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class MemoryResponse(BaseModel):
    """Memory operation response"""
    id: str
    category: str
    content: str
    timestamp: str


class SandboxRequest(BaseModel):
    """Sandbox execution request"""
    code: str
    language: str = "python"
    mode: str = "docker"  # local, docker, kubernetes
    timeout_seconds: int = 60


class SandboxResponse(BaseModel):
    """Sandbox execution response"""
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float
    mode: str


# ============================================================================
# FastAPI Application Setup
# ============================================================================

app = FastAPI(
    title="KaliGhost Pro 3.0",
    description="Enhanced pentesting harness with multi-agent orchestration",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get service instances
orchestrator = get_orchestrator()
memory_system = get_memory_system()
sandbox_manager = get_sandbox_manager()
im_manager = get_im_manager()


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup():
    """Initialize services on startup"""
    logger.info("🐉 KaliGhost Pro 3.0 Backend Starting...")
    logger.info(f"✅ Orchestrator initialized")
    logger.info(f"✅ Memory system initialized at {memory_system.memory_dir}")
    logger.info(f"✅ Sandbox manager initialized (mode: {sandbox_manager.default_mode.value})")
    logger.info(f"✅ IM channel manager initialized")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    logger.info("🔌 Shutting down KaliGhost...")
    await sandbox_manager.cleanup_all()
    await im_manager.disconnect_all()
    logger.info("❌ KaliGhost shutdown complete")


# ============================================================================
# REST API Endpoints
# ============================================================================

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "orchestrator": "ready",
            "memory": "ready",
            "sandbox": "ready",
            "im_channels": "ready"
        }
    }


@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Main chat/task endpoint
    Handles single-agent and multi-agent modes
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message required")

    import time
    start = time.time()

    try:
        mode = AgentMode(request.mode)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid mode: {request.mode}")

    # Decompose task based on mode
    plan = await orchestrator.decompose_task(
        task=request.message,
        thread_id=request.thread_id,
        mode=mode
    )

    # Execute plan
    exec_result = await orchestrator.execute_plan(plan)

    duration_ms = (time.time() - start) * 1000

    # Synthesize response from sub-agent results
    response_text = f"Task completed with {plan.decomposition_strategy} strategy\n"
    response_text += f"Sub-tasks: {len(plan.sub_tasks)}\n"
    for task_id, result in exec_result['results'].items():
        if task_id != "error":
            response_text += f"  • {result.get('agent', 'unknown')}: {result.get('state', 'unknown')}\n"

    return ChatResponse(
        thread_id=request.thread_id,
        response=response_text,
        mode=mode.value,
        plan_id=plan.id,
        sub_task_count=len(plan.sub_tasks),
        execution_time_ms=duration_ms
    )


@app.get("/chat/stream/{thread_id}")
async def chat_stream(thread_id: str):
    """
    WebSocket endpoint for streaming responses
    (Implement WebSocket handling for real-time updates)
    """
    return {"message": "WebSocket streaming available at /ws/chat/{thread_id}"}


# ============================================================================
# Memory Endpoints
# ============================================================================

@app.post("/memory/add")
async def add_memory(request: MemoryRequest) -> MemoryResponse:
    """Add new memory entry"""
    memory_id = memory_system.add_memory(
        category=request.category,
        content=request.content,
        metadata=request.metadata
    )

    return MemoryResponse(
        id=memory_id,
        category=request.category,
        content=request.content,
        timestamp=datetime.now().isoformat()
    )


@app.get("/memory/search")
async def search_memories(
    query: str = Query(""),
    category: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100)
):
    """Search memories"""
    results = memory_system.search_memories(query, category=category, limit=limit)
    return {
        "query": query,
        "category": category,
        "results": [
            {
                "id": m.id,
                "category": m.category,
                "content": m.content,
                "relevance_score": m.relevance_score,
                "access_count": m.access_count
            }
            for m in results
        ]
    }


@app.get("/memory/profile")
async def get_user_profile():
    """Get synthesized user profile from memories"""
    profile = memory_system.get_user_profile()
    return profile


# ============================================================================
# Sandbox Endpoints
# ============================================================================

@app.post("/sandbox/execute")
async def execute_in_sandbox(request: SandboxRequest) -> SandboxResponse:
    """Execute code/command in sandbox"""
    try:
        mode = SandboxMode(request.mode)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid mode: {request.mode}")

    config = SandboxConfig(
        mode=mode,
        timeout_seconds=request.timeout_seconds,
        isolated_fs=True,
        network_access=False
    )

    if request.language == "python":
        result = await sandbox_manager.execute(
            "exec_" + datetime.now().isoformat(),
            code=request.code,
            language="python",
            config=config
        )
    else:
        result = await sandbox_manager.execute_command(
            "exec_" + datetime.now().isoformat(),
            cmd=request.code,
            config=config
        )

    return SandboxResponse(
        success=result.success,
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.exit_code,
        duration_seconds=result.duration_seconds,
        mode=result.execution_mode
    )


# ============================================================================
# Orchestration Endpoints
# ============================================================================

@app.get("/orchestration/stats")
async def get_orchestration_stats():
    """Get orchestrator statistics"""
    return orchestrator.get_execution_stats()


@app.get("/orchestration/plan/{plan_id}")
async def get_plan(plan_id: str):
    """Get details of a specific plan"""
    if plan_id not in orchestrator.plans:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan = orchestrator.plans[plan_id]
    return {
        "id": plan.id,
        "thread_id": plan.thread_id,
        "original_task": plan.original_task,
        "strategy": plan.decomposition_strategy,
        "status": plan.status,
        "sub_task_count": len(plan.sub_tasks)
    }


# ============================================================================
# IM Channel Endpoints
# ============================================================================

async def handle_im_message(message: IMMessage):
    """Unified handler for all IM messages"""
    logger.info(f"📨 Message from {message.channel}: {message.content[:50]}...")

    # Execute task via orchestrator
    plan = await orchestrator.decompose_task(
        task=message.content,
        thread_id=message.thread_id,
        mode=AgentMode.STANDARD
    )
    exec_result = await orchestrator.execute_plan(plan)

    # Format response
    response_text = "✅ Task processed"
    response = IMResponse(
        content=response_text,
        format="text"
    )

    # Send back to channel
    await im_manager.send_to_channel(
        channel_name=message.channel,
        response=response,
        user_id=message.user_id,
        thread_id=message.thread_id
    )


@app.post("/im/init")
async def initialize_im_channels(config: Dict[str, Any]):
    """Initialize IM channels from config"""
    if config.get("telegram", {}).get("enabled"):
        im_manager.register_channel(
            TelegramChannel("telegram", config["telegram"])
        )

    if config.get("slack", {}).get("enabled"):
        im_manager.register_channel(
            SlackChannel("slack", config["slack"])
        )

    if config.get("feishu", {}).get("enabled"):
        im_manager.register_channel(
            FeishuChannel("feishu", config["feishu"])
        )

    if config.get("wechat", {}).get("enabled"):
        im_manager.register_channel(
            WeChatChannel("wechat", config["wechat"])
        )

    im_manager.set_message_handler(handle_im_message)
    await im_manager.connect_all()

    return {
        "channels_initialized": len(im_manager.channels),
        "channels": list(im_manager.channels.keys())
    }


@app.get("/im/status")
async def get_im_status():
    """Get IM channel status"""
    return {
        "running": im_manager.running,
        "channels": [
            {
                "name": name,
                "connected": channel.is_connected
            }
            for name, channel in im_manager.channels.items()
        ]
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("""
╔════════════════════════════════════════════════════════════════╗
║    🐉 KaliGhost Pro 3.0 - Enhanced Pentesting Harness        ║
║         Multi-Agent Orchestration + Memory + Sandbox          ║
║    DeerFlow capabilities, KaliGhost DNA                       ║
╚════════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

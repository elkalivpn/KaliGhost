#!/usr/bin/env python3
"""
🐉 KaliGhost Pro Orchestrator 3.0
Native multi-agent orchestration engine (KaliGhost-built, DeerFlow-inspired)
Parallel sub-agent execution without LangGraph dependency
"""

import asyncio
import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)


class AgentMode(Enum):
    """KaliGhost agent execution modes"""
    FLASH = "flash"  # Fast execution, single agent
    STANDARD = "standard"  # Single agent, full capabilities
    PRO = "pro"  # Planning mode with sub-agent decomposition
    ULTRA = "ultra"  # Multi-agent parallel execution (DeerFlow-style)
    GHOST = "ghost"  # Autonomous + self-healing


class AgentState(Enum):
    """Sub-agent lifecycle states"""
    IDLE = "idle"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class SubAgentTask:
    """Represents a task for a sub-agent"""
    id: str
    parent_thread_id: str
    agent_name: str
    objective: str
    context: Dict[str, Any]
    tools_allowed: List[str]
    max_iterations: int = 10
    timeout_seconds: int = 300
    state: AgentState = AgentState.IDLE
    created_at: str = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class OrchestrationPlan:
    """Decomposed task plan for multi-agent execution"""
    id: str
    thread_id: str
    original_task: str
    decomposition_strategy: str  # "sequential", "parallel", "hierarchical"
    sub_tasks: List[SubAgentTask]
    dependencies: Dict[str, List[str]]  # task_id -> list of task_ids it depends on
    created_at: str = None
    status: str = "created"  # created, executing, completed, failed

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class SubAgentPool:
    """Manages available sub-agents for parallel execution"""

    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.agents: Dict[str, 'SubAgent'] = {}
        self.running_tasks: Dict[str, SubAgentTask] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()

    def register_agent(self, agent_name: str, capabilities: List[str], executor: Callable):
        """Register a new sub-agent"""
        self.agents[agent_name] = SubAgent(
            name=agent_name,
            capabilities=capabilities,
            executor=executor
        )
        logger.info(f"✅ Sub-agent registered: {agent_name} ({', '.join(capabilities)})")

    async def execute_task(self, task: SubAgentTask) -> SubAgentTask:
        """Execute a task with timeout and error handling"""
        agent = self.agents.get(task.agent_name)
        if not agent:
            task.state = AgentState.FAILED
            task.error = f"Agent '{task.agent_name}' not found"
            return task

        task.state = AgentState.RUNNING
        task.started_at = datetime.now().isoformat()
        self.running_tasks[task.id] = task

        try:
            result = await asyncio.wait_for(
                agent.executor(task),
                timeout=task.timeout_seconds
            )
            task.result = result
            task.state = AgentState.COMPLETED
            task.completed_at = datetime.now().isoformat()
            logger.info(f"✅ Task completed: {task.id} (agent: {task.agent_name})")
        except asyncio.TimeoutError:
            task.state = AgentState.FAILED
            task.error = f"Task timeout after {task.timeout_seconds}s"
            logger.error(f"❌ Task timeout: {task.id}")
        except Exception as e:
            task.state = AgentState.FAILED
            task.error = str(e)
            logger.error(f"❌ Task failed: {task.id} - {e}")
        finally:
            del self.running_tasks[task.id]

        return task

    async def execute_parallel(self, tasks: List[SubAgentTask]) -> List[SubAgentTask]:
        """Execute multiple tasks in parallel (respecting concurrency limit)"""
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def bounded_execute(task):
            async with semaphore:
                return await self.execute_task(task)

        results = await asyncio.gather(
            *[bounded_execute(task) for task in tasks],
            return_exceptions=False
        )
        return results

    async def execute_sequential(self, tasks: List[SubAgentTask]) -> List[SubAgentTask]:
        """Execute tasks sequentially (for dependent tasks)"""
        results = []
        for task in tasks:
            result = await self.execute_task(task)
            results.append(result)
            # Pass previous result as context to next task
            if len(tasks) > results.index(result) + 1:
                next_task = tasks[results.index(result) + 1]
                next_task.context['previous_result'] = result.result
        return results


@dataclass
class SubAgent:
    """Represents a specialized sub-agent"""
    name: str
    capabilities: List[str]
    executor: Callable


class KaliGhostOrchestrator:
    """
    Main orchestrator for multi-agent task decomposition and execution
    Replaces LangGraph with KaliGhost-native workflow engine
    """

    def __init__(self, max_concurrent_agents: int = 5):
        self.pool = SubAgentPool(max_concurrent=max_concurrent_agents)
        self.plans: Dict[str, OrchestrationPlan] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.llm_decomposer: Optional[Callable] = None

    def register_llm_decomposer(self, decomposer: Callable):
        """Register LLM function for task decomposition"""
        self.llm_decomposer = decomposer
        logger.info("✅ LLM decomposer registered")

    def register_sub_agent(self, agent_name: str, capabilities: List[str], executor: Callable):
        """Register a sub-agent with the pool"""
        self.pool.register_agent(agent_name, capabilities, executor)

    async def decompose_task(
        self,
        task: str,
        thread_id: str,
        mode: AgentMode = AgentMode.PRO
    ) -> OrchestrationPlan:
        """
        Decompose a complex task into sub-tasks
        Uses LLM if available, else heuristic decomposition
        """
        plan_id = str(uuid.uuid4())

        if mode == AgentMode.FLASH or mode == AgentMode.STANDARD:
            # No decomposition for single-agent modes
            single_task = SubAgentTask(
                id=str(uuid.uuid4()),
                parent_thread_id=thread_id,
                agent_name="lead_agent",
                objective=task,
                context={"mode": mode.value},
                tools_allowed=["all"]
            )
            plan = OrchestrationPlan(
                id=plan_id,
                thread_id=thread_id,
                original_task=task,
                decomposition_strategy="none",
                sub_tasks=[single_task],
                dependencies={}
            )
        else:
            # Multi-agent decomposition
            if self.llm_decomposer:
                sub_tasks = await self.llm_decomposer(task, thread_id)
            else:
                # Heuristic decomposition
                sub_tasks = self._heuristic_decompose(task, thread_id)

            # Detect dependencies
            dependencies = self._detect_dependencies(sub_tasks)

            strategy = "parallel" if not dependencies else "hierarchical"

            plan = OrchestrationPlan(
                id=plan_id,
                thread_id=thread_id,
                original_task=task,
                decomposition_strategy=strategy,
                sub_tasks=sub_tasks,
                dependencies=dependencies
            )

        self.plans[plan.id] = plan
        logger.info(
            f"📋 Task decomposed into {len(plan.sub_tasks)} sub-tasks "
            f"(strategy: {plan.decomposition_strategy})"
        )
        return plan

    def _heuristic_decompose(self, task: str, thread_id: str) -> List[SubAgentTask]:
        """Simple heuristic task decomposition"""
        # Example: pentesting tasks
        keywords = {
            "research": ["recon_agent", "osint_agent"],
            "exploit": ["exploit_agent", "payload_agent"],
            "scan": ["scanner_agent", "analyzer_agent"],
            "report": ["report_agent"],
        }

        sub_tasks = []
        for keyword, agents in keywords.items():
            if keyword.lower() in task.lower():
                for agent_name in agents:
                    sub_tasks.append(
                        SubAgentTask(
                            id=str(uuid.uuid4()),
                            parent_thread_id=thread_id,
                            agent_name=agent_name,
                            objective=f"{keyword.capitalize()}: {task}",
                            context={"parent_task": task},
                            tools_allowed=["all"]
                        )
                    )
        return sub_tasks if sub_tasks else [
            SubAgentTask(
                id=str(uuid.uuid4()),
                parent_thread_id=thread_id,
                agent_name="general_agent",
                objective=task,
                context={},
                tools_allowed=["all"]
            )
        ]

    def _detect_dependencies(self, tasks: List[SubAgentTask]) -> Dict[str, List[str]]:
        """Detect task dependencies based on keywords"""
        dependencies = {}
        for i, task in enumerate(tasks):
            dependencies[task.id] = []
            # Simple heuristic: if task mentions output of previous task
            for j in range(i):
                if "previous" in task.objective.lower() or "result" in task.objective.lower():
                    dependencies[task.id].append(tasks[j].id)
        return dependencies

    async def execute_plan(self, plan: OrchestrationPlan) -> Dict[str, Any]:
        """Execute an orchestration plan"""
        plan.status = "executing"
        logger.info(f"🚀 Executing plan {plan.id} ({plan.decomposition_strategy} strategy)")

        results = {}
        try:
            if plan.decomposition_strategy == "parallel":
                # Execute all tasks in parallel
                results_list = await self.pool.execute_parallel(plan.sub_tasks)
            elif plan.decomposition_strategy == "hierarchical":
                # Execute with dependency ordering
                results_list = await self._execute_with_dependencies(plan)
            else:
                # Single task
                results_list = await self.pool.execute_task(plan.sub_tasks[0])
                if not isinstance(results_list, list):
                    results_list = [results_list]

            for task in results_list:
                results[task.id] = {
                    "agent": task.agent_name,
                    "state": task.state.value,
                    "result": task.result,
                    "error": task.error,
                    "duration_ms": (
                        (datetime.fromisoformat(task.completed_at) -
                         datetime.fromisoformat(task.started_at)).total_seconds() * 1000
                        if task.completed_at and task.started_at
                        else None
                    )
                }

            plan.status = "completed"
            logger.info(f"✅ Plan {plan.id} completed")

        except Exception as e:
            plan.status = "failed"
            logger.error(f"❌ Plan execution failed: {e}")
            results["error"] = str(e)

        self.execution_history.append({
            "plan_id": plan.id,
            "timestamp": datetime.now().isoformat(),
            "status": plan.status,
            "results": results
        })

        return {
            "plan_id": plan.id,
            "status": plan.status,
            "results": results,
            "sub_task_count": len(plan.sub_tasks)
        }

    async def _execute_with_dependencies(self, plan: OrchestrationPlan) -> List[SubAgentTask]:
        """Execute tasks respecting dependencies"""
        completed = {}
        results = []

        while len(completed) < len(plan.sub_tasks):
            # Find tasks that can run now (dependencies met)
            ready_tasks = [
                t for t in plan.sub_tasks
                if t.id not in completed and all(
                    dep_id in completed for dep_id in plan.dependencies.get(t.id, [])
                )
            ]

            if not ready_tasks:
                break  # Deadlock or circular dependency

            task_results = await self.pool.execute_parallel(ready_tasks)
            for task in task_results:
                completed[task.id] = task
                results.append(task)

        return results

    def get_execution_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        total_plans = len(self.plans)
        completed_plans = sum(1 for p in self.plans.values() if p.status == "completed")
        total_tasks = sum(len(p.sub_tasks) for p in self.plans.values())

        return {
            "total_plans": total_plans,
            "completed_plans": completed_plans,
            "total_sub_tasks": total_tasks,
            "concurrent_capacity": self.pool.max_concurrent,
            "execution_history_count": len(self.execution_history)
        }


# Singleton instance
_orchestrator: Optional[KaliGhostOrchestrator] = None


def get_orchestrator() -> KaliGhostOrchestrator:
    """Get or create singleton orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = KaliGhostOrchestrator()
    return _orchestrator

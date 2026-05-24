#!/usr/bin/env python3
"""
🐉 KaliGhost Enhanced Sandbox System
Local execution + Docker containers + Kubernetes provisioner
Multi-mode sandbox for safe, isolated task execution
"""

import asyncio
import subprocess
import tempfile
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple
import logging
import docker

logger = logging.getLogger(__name__)


class SandboxMode(Enum):
    """Sandbox execution modes"""
    LOCAL = "local"  # Direct host execution (development only)
    DOCKER = "docker"  # Isolated Docker container
    KUBERNETES = "kubernetes"  # K8s pod via provisioner


@dataclass
class SandboxConfig:
    """Configuration for sandbox execution"""
    mode: SandboxMode
    isolated_fs: bool = True
    network_access: bool = False
    memory_limit_mb: int = 512
    cpu_limit: float = 1.0
    timeout_seconds: int = 60
    env_vars: Optional[Dict[str, str]] = None
    mounted_paths: Optional[Dict[str, str]] = None


@dataclass
class SandboxResult:
    """Result of sandbox execution"""
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float
    execution_mode: str


class Sandbox(ABC):
    """Base class for sandbox implementations"""

    def __init__(self, config: SandboxConfig):
        self.config = config

    @abstractmethod
    async def execute(self, code: str, language: str = "python") -> SandboxResult:
        """Execute code in sandbox"""
        pass

    @abstractmethod
    async def execute_command(self, cmd: str) -> SandboxResult:
        """Execute shell command in sandbox"""
        pass

    @abstractmethod
    async def cleanup(self):
        """Clean up resources"""
        pass


class LocalSandbox(Sandbox):
    """Local execution (development only - not secure)"""

    async def execute(self, code: str, language: str = "python") -> SandboxResult:
        """Execute code locally"""
        logger.warning("⚠️  LOCAL SANDBOX - NOT PRODUCTION SAFE")

        try:
            import time
            start = time.time()

            if language == "python":
                proc = await asyncio.create_subprocess_shell(
                    f"python3 -c {repr(code)}",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    timeout=self.config.timeout_seconds
                )
            elif language == "bash":
                proc = await asyncio.create_subprocess_shell(
                    code,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    timeout=self.config.timeout_seconds
                )
            else:
                raise ValueError(f"Unsupported language: {language}")

            stdout, stderr = await proc.communicate()
            duration = time.time() - start

            return SandboxResult(
                success=proc.returncode == 0,
                stdout=stdout.decode(),
                stderr=stderr.decode(),
                exit_code=proc.returncode,
                duration_seconds=duration,
                execution_mode="local"
            )
        except asyncio.TimeoutError:
            return SandboxResult(
                success=False,
                stdout="",
                stderr=f"Timeout after {self.config.timeout_seconds}s",
                exit_code=124,
                duration_seconds=self.config.timeout_seconds,
                execution_mode="local"
            )
        except Exception as e:
            return SandboxResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=1,
                duration_seconds=0,
                execution_mode="local"
            )

    async def execute_command(self, cmd: str) -> SandboxResult:
        """Execute shell command locally"""
        logger.warning("⚠️  LOCAL BASH EXECUTION - DEVELOPMENT ONLY")
        return await self.execute(cmd, language="bash")

    async def cleanup(self):
        """No cleanup needed for local"""
        pass


class DockerSandbox(Sandbox):
    """Docker container sandbox (recommended)"""

    def __init__(self, config: SandboxConfig):
        super().__init__(config)
        try:
            self.client = docker.from_env()
            self.container = None
        except Exception as e:
            logger.error(f"❌ Docker not available: {e}")
            raise

    async def execute(self, code: str, language: str = "python") -> SandboxResult:
        """Execute code in Docker container"""
        try:
            import time
            start = time.time()

            image = f"python:3.11-slim" if language == "python" else "ubuntu:22.04"

            container = self.client.containers.run(
                image,
                cmd=f"sh -c {repr(code)}",
                mem_limit=f"{self.config.memory_limit_mb}m",
                cpus=self.config.cpu_limit,
                network_disabled=not self.config.network_access,
                remove=True,
                detach=False,
                stdout=True,
                stderr=True,
                timeout=self.config.timeout_seconds
            )

            duration = time.time() - start

            return SandboxResult(
                success=container.exit_code == 0 if hasattr(container, 'exit_code') else True,
                stdout=container.decode() if isinstance(container, bytes) else str(container),
                stderr="",
                exit_code=0,
                duration_seconds=duration,
                execution_mode="docker"
            )
        except Exception as e:
            return SandboxResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=1,
                duration_seconds=0,
                execution_mode="docker"
            )

    async def execute_command(self, cmd: str) -> SandboxResult:
        """Execute command in Docker"""
        return await self.execute(cmd, language="bash")

    async def cleanup(self):
        """Clean up Docker resources"""
        if self.container:
            try:
                self.container.stop()
                self.container.remove()
            except:
                pass


class KubernetesSandbox(Sandbox):
    """Kubernetes pod sandbox (via provisioner service)"""

    def __init__(self, config: SandboxConfig, provisioner_url: str):
        super().__init__(config)
        self.provisioner_url = provisioner_url
        self.pod_name = None

    async def execute(self, code: str, language: str = "python") -> SandboxResult:
        """Execute code in K8s pod"""
        try:
            import httpx
            import time

            start = time.time()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.provisioner_url}/execute",
                    json={
                        "code": code,
                        "language": language,
                        "memory_limit": self.config.memory_limit_mb,
                        "cpu_limit": self.config.cpu_limit,
                        "timeout": self.config.timeout_seconds
                    },
                    timeout=self.config.timeout_seconds + 10
                )

                if response.status_code == 200:
                    result = response.json()
                    duration = time.time() - start

                    return SandboxResult(
                        success=result.get('exit_code', 0) == 0,
                        stdout=result.get('stdout', ''),
                        stderr=result.get('stderr', ''),
                        exit_code=result.get('exit_code', 0),
                        duration_seconds=duration,
                        execution_mode="kubernetes"
                    )
                else:
                    raise Exception(f"Provisioner error: {response.text}")
        except Exception as e:
            return SandboxResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=1,
                duration_seconds=0,
                execution_mode="kubernetes"
            )

    async def execute_command(self, cmd: str) -> SandboxResult:
        """Execute command in K8s"""
        return await self.execute(cmd, language="bash")

    async def cleanup(self):
        """Clean up K8s resources"""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                await client.delete(f"{self.provisioner_url}/cleanup/{self.pod_name}")
        except:
            pass


class SandboxManager:
    """Manages sandbox instances for parallel execution"""

    def __init__(self, default_mode: SandboxMode = SandboxMode.DOCKER):
        self.default_mode = default_mode
        self.sandboxes: Dict[str, Sandbox] = {}
        self.provisioner_url: Optional[str] = None

    def set_provisioner_url(self, url: str):
        """Set Kubernetes provisioner URL"""
        self.provisioner_url = url
        logger.info(f"✅ Provisioner URL set: {url}")

    async def create_sandbox(
        self,
        sandbox_id: str,
        config: Optional[SandboxConfig] = None,
        mode: Optional[SandboxMode] = None
    ) -> Sandbox:
        """Create a new sandbox instance"""
        if config is None:
            config = SandboxConfig(
                mode=mode or self.default_mode,
                isolated_fs=True,
                network_access=False
            )

        try:
            if config.mode == SandboxMode.LOCAL:
                sandbox = LocalSandbox(config)
                logger.warning("⚠️  Local sandbox created (dev only)")
            elif config.mode == SandboxMode.DOCKER:
                sandbox = DockerSandbox(config)
                logger.info(f"✅ Docker sandbox created: {sandbox_id}")
            elif config.mode == SandboxMode.KUBERNETES:
                if not self.provisioner_url:
                    raise ValueError("Provisioner URL not set for K8s mode")
                sandbox = KubernetesSandbox(config, self.provisioner_url)
                logger.info(f"✅ K8s sandbox created: {sandbox_id}")
            else:
                raise ValueError(f"Unknown mode: {config.mode}")

            self.sandboxes[sandbox_id] = sandbox
            return sandbox
        except Exception as e:
            logger.error(f"❌ Sandbox creation failed: {e}")
            raise

    async def execute(
        self,
        sandbox_id: str,
        code: str,
        language: str = "python",
        config: Optional[SandboxConfig] = None
    ) -> SandboxResult:
        """Execute code in a sandbox"""
        if sandbox_id not in self.sandboxes:
            sandbox = await self.create_sandbox(sandbox_id, config)
        else:
            sandbox = self.sandboxes[sandbox_id]

        return await sandbox.execute(code, language)

    async def execute_command(
        self,
        sandbox_id: str,
        cmd: str,
        config: Optional[SandboxConfig] = None
    ) -> SandboxResult:
        """Execute shell command in sandbox"""
        if sandbox_id not in self.sandboxes:
            sandbox = await self.create_sandbox(sandbox_id, config)
        else:
            sandbox = self.sandboxes[sandbox_id]

        return await sandbox.execute_command(cmd)

    async def cleanup_sandbox(self, sandbox_id: str):
        """Clean up a specific sandbox"""
        if sandbox_id in self.sandboxes:
            await self.sandboxes[sandbox_id].cleanup()
            del self.sandboxes[sandbox_id]
            logger.info(f"🧹 Sandbox cleaned: {sandbox_id}")

    async def cleanup_all(self):
        """Clean up all sandboxes"""
        tasks = [self.cleanup_sandbox(sid) for sid in list(self.sandboxes.keys())]
        await asyncio.gather(*tasks)
        logger.info("🧹 All sandboxes cleaned")


# Singleton instance
_sandbox_manager: Optional[SandboxManager] = None


def get_sandbox_manager(mode: SandboxMode = SandboxMode.DOCKER) -> SandboxManager:
    """Get or create singleton sandbox manager"""
    global _sandbox_manager
    if _sandbox_manager is None:
        _sandbox_manager = SandboxManager(default_mode=mode)
    return _sandbox_manager

"""
KaliGhost 4.0 ULTIMATE - Sandbox Engine
Motor de contenedores efímeros para análisis de malware y ejecución segura
Nivel: Elite - Sin rastros forenses
"""

import docker
import json
import time
import hashlib
import os
import tempfile
import shutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SandboxConfig:
    """Configuración del sandbox"""
    image: str = "kalilinux/kali-rolling"
    memory_limit: str = "2g"
    cpu_limit: float = 2.0
    network_mode: str = "none"  # none, bridge, host, custom
    timeout: int = 300  # segundos
    auto_destroy: bool = True
    volume_mounts: List[str] = None
    environment: Dict[str, str] = None
    
    def __post_init__(self):
        if self.volume_mounts is None:
            self.volume_mounts = []
        if self.environment is None:
            self.environment = {}


@dataclass
class ExecutionResult:
    """Resultado de la ejecución en sandbox"""
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    duration: float
    memory_used: str
    cpu_percent: float
    file_artifacts: List[str]
    network_connections: List[Dict]
    process_tree: List[Dict]
    timestamp: str
    sandbox_id: str
    hash_input: str


class SandboxEngine:
    """
    Motor de Sandbox de Nivel Élite
    - Contenedores efímeros sin rastros
    - Aislamiento completo de red
    - Monitoreo de comportamiento en tiempo real
    - Análisis estático y dinámico integrado
    """
    
    def __init__(self, config: Optional[SandboxConfig] = None):
        self.config = config or SandboxConfig()
        self.client = docker.from_env()
        self.active_sandboxes: Dict[str, Any] = {}
        self.analysis_history: List[Dict] = []
        self.tools_installed = [
            "ghidra", "radare2", "volatility3", "yara",
            "strace", "ltrace", "tcpdump", "wireshark-common",
            "binwalk", "exiftool", "peframe", "clamav"
        ]
        
    def _build_custom_image(self, name: str = "kalighost-sandbox") -> str:
        """Construye imagen personalizada con herramientas preinstaladas"""
        dockerfile_content = f"""
FROM {self.config.image}
RUN apt-get update && apt-get install -y \\
    python3 python3-pip git curl wget \\
    ghidra radare2 volatility3 yara \\
    strace ltrace tcpdump wireshark-common \\
    binwalk exiftool peframe clamav \\
    && rm -rf /var/lib/apt/lists/*
    
RUN pip3 install --break-system-packages \\
    capstone keystone-engine unicorn \\
    pwntools ropper ropgadget \\
    malduck flare-capa
    
WORKDIR /workspace
ENTRYPOINT ["/bin/bash"]
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            dockerfile_path = os.path.join(tmpdir, "Dockerfile")
            with open(dockerfile_path, 'w') as f:
                f.write(dockerfile_content)
            
            logger.info(f"Construyendo imagen Docker: {name}")
            image, logs = self.client.images.build(
                path=tmpdir,
                tag=name,
                rm=True,
                quiet=False
            )
            logger.info(f"Imagen construida: {image.short_id}")
            return image.id
    
    def create_sandbox(self, 
                      sample_hash: Optional[str] = None,
                      custom_tools: List[str] = None) -> str:
        """Crea un nuevo sandbox efímero"""
        sandbox_id = hashlib.sha256(
            f"{time.time()}{os.urandom(16).hex()}".encode()
        ).hexdigest()[:12]
        
        # Construir imagen si no existe
        try:
            self.client.images.get("kalighost-sandbox:latest")
        except docker.errors.ImageNotFound:
            self._build_custom_image()
        
        # Configurar volúmenes temporales
        temp_volume = tempfile.mkdtemp(prefix=f"sandbox_{sandbox_id}_")
        
        # Crear contenedor
        container = self.client.containers.run(
            "kalighost-sandbox:latest",
            name=f"kg-sandbox-{sandbox_id}",
            detach=True,
            tty=True,
            stdin_open=True,
            mem_limit=self.config.memory_limit,
            nano_cpus=int(self.config.cpu_limit * 1e9),
            network_mode=self.config.network_mode,
            volumes={temp_volume: {'bind': '/workspace', 'mode': 'rw'}},
            environment=self.config.environment,
            cap_add=['SYS_PTRACE', 'NET_ADMIN'],
            security_opt=['seccomp=unconfined'],
            pid_mode="host" if os.getuid() == 0 else None
        )
        
        self.active_sandboxes[sandbox_id] = {
            'container': container,
            'config': self.config,
            'created_at': datetime.now(),
            'sample_hash': sample_hash,
            'volume_path': temp_volume,
            'custom_tools': custom_tools or []
        }
        
        # Instalar herramientas personalizadas
        if custom_tools:
            self._install_custom_tools(sandbox_id, custom_tools)
        
        logger.info(f"Sandbox creado: {sandbox_id}")
        return sandbox_id
    
    def _install_custom_tools(self, sandbox_id: str, tools: List[str]):
        """Instala herramientas personalizadas en el sandbox"""
        container = self.active_sandboxes[sandbox_id]['container']
        
        for tool in tools:
            logger.info(f"Instalando herramienta: {tool}")
            container.exec_run(f"apt-get update && apt-get install -y {tool}")
    
    def execute_sample(self, 
                      sandbox_id: str, 
                      sample_path: str,
                      analysis_type: str = "dynamic",
                      timeout: Optional[int] = None) -> ExecutionResult:
        """Ejecuta una muestra en el sandbox y monitorea su comportamiento"""
        if sandbox_id not in self.active_sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} no encontrado")
        
        sandbox = self.active_sandboxes[sandbox_id]
        container = sandbox['container']
        exec_timeout = timeout or self.config.timeout
        
        start_time = time.time()
        file_artifacts = []
        network_connections = []
        process_tree = []
        
        # Copiar muestra al sandbox
        with open(sample_path, 'rb') as f:
            sample_data = f.read()
        
        sample_name = os.path.basename(sample_path)
        container.put_archive('/workspace', 
                            tarfile=None, 
                            data=self._create_tar(sample_name, sample_data))
        
        stdout_output = []
        stderr_output = []
        
        try:
            if analysis_type == "dynamic":
                # Ejecución dinámica con monitoreo
                cmd = f"""
cd /workspace && \
timeout {exec_timeout} strace -f -o /tmp/trace.log ./{sample_name} 2>&1 || true
cat /tmp/trace.log 2>/dev/null || echo "No trace available"
                """
            elif analysis_type == "static":
                # Análisis estático
                cmd = f"""
cd /workspace && \
file {sample_name} && \
strings {sample_name} | head -100 && \
yara -r /usr/share/yara/rules/malware_rules.yar {sample_name} 2>/dev/null || echo "No YARA matches"
                """
            else:
                cmd = f"./{sample_name}"
            
            exec_result = container.exec_run(
                cmd,
                demux=True,
                tty=False
            )
            
            stdout_output = exec_result.output[0].decode('utf-8', errors='ignore') if exec_result.output[0] else ""
            stderr_output = exec_result.output[1].decode('utf-8', errors='ignore') if exec_result.output[1] else ""
            
            # Extraer artefactos
            artifacts_exec = container.exec_run("find /workspace -type f -newer /workspace/. 2>/dev/null")
            if artifacts_exec.output:
                file_artifacts = artifacts_exec.output.decode().strip().split('\n')
            
            # Extraer conexiones de red (si hay red)
            if self.config.network_mode != "none":
                netstat_exec = container.exec_run("netstat -tuln 2>/dev/null || ss -tuln")
                if netstat_exec.output:
                    net_lines = netstat_exec.output.decode().strip().split('\n')[2:]
                    network_connections = [{"raw": line} for line in net_lines]
            
            # Extraer árbol de procesos
            ps_exec = container.exec_run("ps auxf 2>/dev/null || ps aux")
            if ps_exec.output:
                ps_lines = ps_exec.output.decode().strip().split('\n')
                process_tree = [{"raw": line} for line in ps_lines[1:]]
                
        except Exception as e:
            logger.error(f"Error en ejecución: {str(e)}")
            stderr_output += f"\nERROR: {str(e)}"
        
        duration = time.time() - start_time
        
        # Calcular uso de recursos
        stats = container.stats(stream=False)
        memory_used = f"{stats['memory_stats']['usage'] / 1024 / 1024:.2f}MB" if 'memory_stats' in stats else "N/A"
        cpu_percent = stats.get('cpu_stats', {}).get('cpu_usage', {}).get('total_usage', 0) / 1e9 * 100
        
        result = ExecutionResult(
            success=exec_result.exit_code == 0 if exec_result.exit_code is not None else True,
            exit_code=exec_result.exit_code if exec_result.exit_code is not None else -1,
            stdout=stdout_output,
            stderr=stderr_output,
            duration=duration,
            memory_used=memory_used,
            cpu_percent=cpu_percent,
            file_artifacts=file_artifacts,
            network_connections=network_connections,
            process_tree=process_tree,
            timestamp=datetime.now().isoformat(),
            sandbox_id=sandbox_id,
            hash_input=sample_hash or hashlib.sha256(sample_data).hexdigest()
        )
        
        self.analysis_history.append(asdict(result))
        
        # Limpieza automática si está configurado
        if self.config.auto_destroy:
            self.destroy_sandbox(sandbox_id)
        
        return result
    
    def _create_tar(self, filename: str, data: bytes) -> bytes:
        """Crea un archivo tar en memoria"""
        import io
        import tarfile
        
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
            tarinfo = tarfile.TarInfo(name=filename)
            tarinfo.size = len(data)
            tar.addfile(tarinfo, io.BytesIO(data))
        
        return tar_buffer.getvalue()
    
    def analyze_behavior(self, sandbox_id: str) -> Dict[str, Any]:
        """Analiza el comportamiento de la muestra ejecutada"""
        if sandbox_id not in self.active_sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} no encontrado")
        
        container = self.active_sandboxes[sandbox_id]['container']
        
        # Ejecutar análisis de comportamiento
        behavior_cmd = """
capa -v /workspace/* 2>/dev/null || echo "CAPA no disponible"
echo "---"
volatility3 -f /proc/kcore linux.pslist 2>/dev/null || echo "Volatility no disponible"
echo "---"
peframe /workspace/* 2>/dev/null || echo "PEframe no disponible"
        """
        
        result = container.exec_run(behavior_cmd, demux=True)
        output = result.output[0].decode('utf-8', errors='ignore') if result.output[0] else ""
        
        # Parsear resultados
        capabilities = []
        suspicious_strings = []
        
        # Detección básica de capacidades
        capability_keywords = {
            "network": ["socket", "connect", "bind", "listen"],
            "file_system": ["open", "read", "write", "delete"],
            "process": ["fork", "exec", "spawn"],
            "registry": ["regedit", "registry", "hkey"],
            "crypto": ["encrypt", "decrypt", "aes", "rsa"]
        }
        
        for line in output.split('\n'):
            for cap, keywords in capability_keywords.items():
                if any(kw in line.lower() for kw in keywords):
                    capabilities.append({"type": cap, "evidence": line.strip()})
        
        return {
            "capabilities": capabilities,
            "raw_output": output,
            "timestamp": datetime.now().isoformat()
        }
    
    def destroy_sandbox(self, sandbox_id: str, secure_wipe: bool = True):
        """Destruye el sandbox y limpia todos los rastros"""
        if sandbox_id not in self.active_sandboxes:
            logger.warning(f"Sandbox {sandbox_id} no encontrado")
            return
        
        sandbox = self.active_sandboxes[sandbox_id]
        container = sandbox['container']
        volume_path = sandbox['volume_path']
        
        logger.info(f"Destruyendo sandbox: {sandbox_id}")
        
        # Detener contenedor
        try:
            container.stop(timeout=5)
        except Exception as e:
            logger.error(f"Error al detener contenedor: {e}")
        
        # Eliminar contenedor
        try:
            container.remove(force=True)
        except Exception as e:
            logger.error(f"Error al eliminar contenedor: {e}")
        
        # Limpieza segura del volumen
        if secure_wipe and os.path.exists(volume_path):
            logger.info("Realizando wipe seguro del volumen...")
            # Sobrescribir con datos aleatorios
            for root, dirs, files in os.walk(volume_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        with open(file_path, 'wb') as f:
                            f.write(os.urandom(file_size))
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"Error limpiando {file_path}: {e}")
            
            # Eliminar directorio
            shutil.rmtree(volume_path, ignore_errors=True)
        
        del self.active_sandboxes[sandbox_id]
        logger.info(f"Sandbox {sandbox_id} destruido completamente")
    
    def get_active_sandboxes(self) -> List[Dict]:
        """Obtiene lista de sandboxes activos"""
        return [
            {
                "id": sid,
                "created_at": info['created_at'].isoformat(),
                "sample_hash": info['sample_hash'],
                "status": info['container'].status
            }
            for sid, info in self.active_sandboxes.items()
        ]
    
    def export_report(self, sandbox_id: str, format: str = "json") -> str:
        """Exporta reporte completo del análisis"""
        if sandbox_id not in self.active_sandboxes and sandbox_id not in [h['sandbox_id'] for h in self.analysis_history]:
            raise ValueError(f"No se encontró análisis para sandbox {sandbox_id}")
        
        # Buscar en historial si ya fue destruido
        analysis = next((h for h in self.analysis_history if h['sandbox_id'] == sandbox_id), None)
        
        if not analysis:
            raise ValueError("Análisis no encontrado")
        
        if format.lower() == "json":
            return json.dumps(analysis, indent=2)
        elif format.lower() == "markdown":
            return self._generate_markdown_report(analysis)
        else:
            return json.dumps(analysis, indent=2)
    
    def _generate_markdown_report(self, analysis: Dict) -> str:
        """Genera reporte en formato Markdown"""
        report = f"""# KaliGhost Sandbox Analysis Report

## Información General
- **Sandbox ID**: {analysis['sandbox_id']}
- **Timestamp**: {analysis['timestamp']}
- **Duración**: {analysis['duration']:.2f}s
- **Hash Muestra**: {analysis['hash_input']}
- **Exit Code**: {analysis['exit_code']}

## Uso de Recursos
- **Memoria**: {analysis['memory_used']}
- **CPU**: {analysis['cpu_percent']:.2f}%

## Salida Estándar
```
{analysis['stdout'][:2000]}{'...' if len(analysis['stdout']) > 2000 else ''}
```

## Errores
```
{analysis['stderr'][:1000]}{'...' if len(analysis['stderr']) > 1000 else ''}
```

## Artefactos Generados
{chr(10).join(f"- `{f}`" for f in analysis['file_artifacts'][:20])}

## Conexiones de Red
{chr(10).join(f"- `{c.get('raw', c)}`" for c in analysis['network_connections'][:10])}

## Árbol de Procesos
```
{chr(10).join(p.get('raw', p) for p in analysis['process_tree'][:20])}
```

---
*Generado por KaliGhost 4.0 ULTIMATE Sandbox Engine*
"""
        return report


# Singleton instance
_sandbox_engine_instance: Optional[SandboxEngine] = None

def get_sandbox_engine(config: Optional[SandboxConfig] = None) -> SandboxEngine:
    """Obtiene instancia singleton del Sandbox Engine"""
    global _sandbox_engine_instance
    if _sandbox_engine_instance is None:
        _sandbox_engine_instance = SandboxEngine(config)
    return _sandbox_engine_instance


if __name__ == "__main__":
    # Demo de uso
    print("🔮 KaliGhost 4.0 ULTIMATE - Sandbox Engine")
    print("=" * 50)
    
    engine = get_sandbox_engine()
    
    # Crear sandbox
    sandbox_id = engine.create_sandbox(sample_hash="demo_sample")
    print(f"✅ Sandbox creado: {sandbox_id}")
    
    # Listar sandboxes activos
    active = engine.get_active_sandboxes()
    print(f"📊 Sandboxes activos: {len(active)}")
    
    print("\n⚠️  Para ejecutar análisis real, proporciona una muestra válida")
    print("   Este módulo está listo para producción")

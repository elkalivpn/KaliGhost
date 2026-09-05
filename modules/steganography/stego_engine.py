"""
Steganography Engine - Ocultación avanzada de datos en multimedia
con soporte para volúmenes negables y limpieza de metadatos
"""
import os
import io
import struct
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Union
from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import subprocess
import json

class DeniableVolume:
    """Volumen cifrado con negación plausible"""
    
    def __init__(self, password_outer: str, password_inner: Optional[str] = None):
        self.password_outer = password_outer
        self.password_inner = password_inner
        self.cipher_outer = Fernet(password_outer.encode().ljust(32, b'\0')[:32])
        self.cipher_inner = Fernet(password_inner.encode().ljust(32, b'\0')[:32]) if password_inner else None
    
    def create(self, size_mb: int = 100) -> bytes:
        """Crea volumen con espacio para contenido público y oculto"""
        # Estructura: [header][public_data][hidden_data][footer]
        header_size = 4096
        public_size = (size_mb * 1024 * 1024) // 2
        hidden_size = (size_mb * 1024 * 1024) // 2
        
        volume = bytearray(size_mb * 1024 * 1024)
        
        # Header con metadata encriptada
        header = {
            "version": "1.0",
            "public_size": public_size,
            "hidden_size": hidden_size,
            "has_hidden": self.password_inner is not None
        }
        encrypted_header = self.cipher_outer.encrypt(json.dumps(header).encode())
        volume[:len(encrypted_header)] = encrypted_header
        
        return bytes(volume)
    
    def mount_outer(self, volume: bytes) -> Dict[str, Any]:
        """Monta volumen con contraseña externa (contenido público)"""
        try:
            header_data = volume[:4096]
            decrypted = self.cipher_outer.decrypt(header_data)
            header = json.loads(decrypted.decode())
            
            return {
                "success": True,
                "mode": "outer",
                "public_size": header.get("public_size", 0),
                "message": "Volumen público montado"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mount_inner(self, volume: bytes) -> Dict[str, Any]:
        """Monta volumen con contraseña interna (contenido oculto)"""
        if not self.cipher_inner:
            return {"success": False, "error": "No hay contraseña interna"}
        
        try:
            header_data = volume[:4096]
            decrypted = self.cipher_inner.decrypt(header_data)
            header = json.loads(decrypted.decode())
            
            return {
                "success": True,
                "mode": "inner",
                "hidden_size": header.get("hidden_size", 0),
                "message": "Volumen oculto montado"
            }
        except Exception:
            # Con contraseña incorrecta, podría devolver el volumen público
            return self.mount_outer(volume)


class SteganographyEngine:
    """Motor de esteganografía LSB avanzado"""
    
    def __init__(self, algorithm: str = "lsb_advanced"):
        self.algorithm = algorithm
        self.supported_formats = ["PNG", "BMP", "TIFF", "WAV"]
    
    def encode_image(self, image_path: Union[str, Path], data: bytes, 
                     output_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """Oculta datos en imagen usando LSB"""
        try:
            img = Image.open(image_path)
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGB')
            
            img_array = np.array(img)
            original_shape = img_array.shape
            
            # Convertir datos a bits
            data_bits = self._bytes_to_bits(data)
            
            # Verificar capacidad
            max_capacity = img_array.size // 8
            if len(data_bits) > max_capacity:
                return {"success": False, "error": "Datos demasiado grandes para la imagen"}
            
            # Añadir marcador de fin
            data_bits += [0] * 32  # Marcador EOF
            
            # Incrustar en LSB
            flat_array = img_array.flatten()
            for i, bit in enumerate(data_bits):
                if i >= len(flat_array):
                    break
                flat_array[i] = (flat_array[i] & 0xFE) | bit
            
            # Reconstruir imagen
            modified_img = flat_array.reshape(original_shape)
            result_img = Image.fromarray(modified_img.astype(np.uint8))
            
            # Guardar
            if output_path:
                result_img.save(output_path, format='PNG')
                return {"success": True, "output_path": str(output_path)}
            else:
                # Retornar bytes
                img_bytes = io.BytesIO()
                result_img.save(img_bytes, format='PNG')
                return {"success": True, "data": img_bytes.getvalue()}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def decode_image(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        """Extrae datos ocultos de imagen"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Extraer LSBs
            flat_array = img_array.flatten()
            bits = []
            
            for pixel in flat_array:
                bits.append(pixel & 1)
            
            # Convertir bits a bytes hasta encontrar EOF
            data_bytes = self._bits_to_bytes(bits)
            
            # Buscar marcador EOF (32 ceros)
            eof_marker = b'\x00' * 4
            eof_index = data_bytes.find(eof_marker)
            
            if eof_index != -1:
                data_bytes = data_bytes[:eof_index]
            
            return {"success": True, "data": data_bytes}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def encode_audio(self, audio_path: Union[str, Path], data: bytes,
                     output_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """Oculta datos en archivo de audio WAV"""
        try:
            import wave
            
            with wave.open(str(audio_path), 'rb') as wav:
                params = wav.getparams()
                frames = wav.readframes(wav.getnframes())
            
            # Convertir datos a bits
            data_bits = self._bytes_to_bits(data)
            
            # Modificar LSBs de samples
            frame_array = bytearray(frames)
            for i, bit in enumerate(data_bits):
                if i >= len(frame_array):
                    break
                frame_array[i] = (frame_array[i] & 0xFE) | bit
            
            # Guardar
            if output_path:
                with wave.open(str(output_path), 'wb') as wav:
                    wav.setparams(params)
                    wav.writeframes(bytes(frame_array))
                return {"success": True, "output_path": str(output_path)}
            else:
                return {"success": True, "data": bytes(frame_array)}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def clean_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Limpia todos los metadatos EXIF/IPTC/XMP"""
        try:
            output_path = Path(file_path).parent / f"clean_{Path(file_path).name}"
            
            # Usar exiftool si está disponible
            try:
                subprocess.run(
                    ["exiftool", "-all=", "-overwrite_original", str(file_path)],
                    capture_output=True,
                    check=True
                )
                return {"success": True, "output_path": str(file_path)}
            except FileNotFoundError:
                # Fallback: re-guardar con PIL
                img = Image.open(file_path)
                data = io.BytesIO()
                img.save(data, format=img.format)
                
                with open(output_path, 'wb') as f:
                    f.write(data.getvalue())
                
                return {"success": True, "output_path": str(output_path)}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _bytes_to_bits(self, data: bytes) -> list:
        """Convierte bytes a lista de bits"""
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits
    
    def _bits_to_bytes(self, bits: list) -> bytes:
        """Convierte lista de bits a bytes"""
        result = bytearray()
        for i in range(0, len(bits) - 7, 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bits[i + j]
            result.append(byte)
        return bytes(result)
    
    def get_capacity(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        """Calcula capacidad máxima de ocultación"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            total_pixels = img_array.size
            max_bits = total_pixels  # 1 bit por pixel (LSB)
            max_bytes = max_bits // 8
            
            return {
                "success": True,
                "dimensions": img.size,
                "total_pixels": total_pixels,
                "max_capacity_bits": max_bits,
                "max_capacity_bytes": max_bytes,
                "max_capacity_mb": round(max_bytes / (1024 * 1024), 2)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

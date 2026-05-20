#!/usr/bin/env python3
"""
Interfaz mejorada para Hermes con solución al problema de entrada de texto
"""

import sys
import os
import time
import threading
from typing import Optional
import readline

class ImprovedTextInputHandler:
    """Manejador mejorado de entrada de texto para resolver problemas de renderizado"""
    
    def __init__(self):
        self.input_buffer = ""
        self.cursor_position = 0
        self.history = []
        self.max_history = 100
        
    def clear_screen(self):
        """Limpia la pantalla de manera segura"""
        print("\033[2J\033[H", end="", flush=True)
        
    def safe_print(self, text: str, end: str = "\n"):
        """Imprime texto de manera segura evitando problemas de renderizado"""
        try:
            print(text, end=end, flush=True)
        except Exception:
            # Si hay problemas de impresión, usar sys.stdout
            sys.stdout.write(text + end)
            sys.stdout.flush()
            
    def process_input(self, input_data: str) -> Optional[str]:
        """Procesa la entrada de texto correctamente"""
        if not input_data:
            return None
            
        # Eliminar caracteres de control problemáticos
        cleaned_input = ''.join(char for char in input_data if ord(char) >= 32 or char in '\n\r\t')
        
        # Actualizar buffer de entrada
        self.input_buffer += cleaned_input
        self.cursor_position = len(self.input_buffer)
        
        # Mostrar el buffer completo
        self.show_buffer()
        
        return self.input_buffer
        
    def show_buffer(self):
        """Muestra todo el buffer actual de entrada"""
        # Limpiar línea actual y volver al inicio
        sys.stdout.write(f"\r{' ' * 100}\r")
        sys.stdout.write(f"> {self.input_buffer}")
        sys.stdout.flush()
        
    def get_input(self) -> str:
        """Obtiene entrada de texto de manera robusta"""
        try:
            # Configurar readline para mejores interacciones
            readline.parse_and_bind("tab: complete")
            readline.set_completion_display_matches_hook(None)
            
            # Mostrar prompt inicial
            print("> ", end="", flush=True)
            
            # Obtener entrada de forma continua sin perder caracteres
            while True:
                try:
                    # Usar sys.stdin.read() para capturar todo el input
                    char = sys.stdin.read(1)
                    if char == '\n':
                        print()  # Nueva línea tras enter
                        break
                    elif char == '\b' or char == '\x7f':  # Backspace
                        if len(self.input_buffer) > 0:
                            self.input_buffer = self.input_buffer[:-1]
                            self.cursor_position = len(self.input_buffer)
                            # Refrescar la pantalla
                            self.show_buffer()
                    else:
                        self.input_buffer += char
                        self.cursor_position = len(self.input_buffer)
                        self.show_buffer()
                        
                except KeyboardInterrupt:
                    print("\nInterrupción por teclado")
                    return ""
                except Exception:
                    # En caso de error de entrada, seguir esperando
                    continue
                    
        except Exception as e:
            print(f"Error en get_input: {e}")
            return ""
            
        # Devolver el texto completo
        result = self.input_buffer
        self.input_buffer = ""  # Limpiar buffer
        return result

class ModernTerminalInterface:
    """Interfaz moderna del terminal"""
    
    def __init__(self):
        self.text_handler = ImprovedTextInputHandler()
        self.running = True
        
    def display_welcome(self):
        """Muestra el mensaje de bienvenida moderno"""
        welcome_msg = """
╔════════════════════════════════════════════════════════════════════════════╗
║                   🚀 YrYs-Agent - Interfaz Moderna                       ║
║                      ¡Bienvenido al sistema autónomo!                    ║
╚════════════════════════════════════════════════════════════════════════════╝

🔧 Sistema optimizado para uso eficiente de tokens
📈 Monitoreo continuo de eficiencia
⚡ Operación segura y proactiva

Comenzamos con el modo autónomo...
        """
        print(welcome_msg)
        
    def display_status(self, status: str = "Listo"):
        """Muestra indicadores de estado visualmente"""
        status_emojis = {
            "Listo": "✅",
            "Procesando": "🔄",
            "Error": "❌",
            "Esperando": "⏳",
            "Éxito": "🎉"
        }
        
        emoji = status_emojis.get(status, "❓")
        print(f"  {emoji} Estado: {status}")
        
    def handle_user_input(self):
        """Maneja la entrada del usuario con feedback visual"""
        print("\n📝 Ingresa tu comando (escribe 'salir' para terminar):")
        while self.running:
            try:
                # Mostrar prompt con feedback
                self.text_handler.show_buffer()
                
                # Obtener entrada
                user_input = self.text_handler.get_input()
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("👋 Cerrando sistema...")
                    self.running = False
                    break
                    
                if user_input.strip():
                    # Procesar la entrada
                    print(f"\n📥 Recibido: '{user_input}'")
                    self.process_command(user_input)
                    
            except Exception as e:
                print(f"🔧 Error al procesar entrada: {e}")
                self.text_handler.input_buffer = ""
                self.text_handler.show_buffer()
                
    def process_command(self, command: str):
        """Procesa comandos con feedback visual"""
        self.display_status("Procesando")
        
        # Simulación de procesamiento
        time.sleep(0.5)
        
        # Mostrar resultado
        result_msg = f"✅ Comando '{command}' procesado exitosamente"
        print(f"  {result_msg}")
        self.display_status("Listo")

def main():
    """Punto de entrada principal"""
    try:
        # Crear sistema de interfaz moderna
        interface = ModernTerminalInterface()
        
        # Mostrar bienvenida
        interface.display_welcome()
        
        # Iniciar manejo de entrada
        interface.handle_user_input()
        
        print("Sistema cerrado correctamente")
        
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error fatal: {e}")

if __name__ == "__main__":
    main()
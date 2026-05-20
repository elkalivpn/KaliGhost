#!/usr/bin/env python3
"""Visualizador avanzado de logs de agentes autónomos"""

import os
import re
import sys
import json
import time
import curses
import threading
from datetime import datetime
from collections import deque
from pathlib import Path

class LogVisualizer:
    def __init__(self, log_directory="~/KaliGhost/yrays-agent/logs"):
        self.log_directory = Path(os.path.expanduser(log_directory))
        self.log_files = [
            "proactive_monitor.log",
            "orchestrator.log",
            "yrays.log"
        ]
        self.log_data = {log_file: deque(maxlen=100) for log_file in self.log_files}
        self.running = False
        self.screen = None
        
    def parse_log_line(self, line):
        """Parsear una línea de log para extraer información"""
        # Patrón para logs con timestamp
        timestamp_pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),.*?\[(\w+)\] - (.*)$'
        match = re.match(timestamp_pattern, line.strip())
        
        if match:
            timestamp, level, message = match.groups()
            return {
                'timestamp': timestamp,
                'level': level,
                'message': message
            }
        else:
            # Formato alternativo
            return {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'level': 'INFO',
                'message': line.strip()
            }
            
    def read_logs(self):
        """Leer archivos de log y actualizar datos"""
        while self.running:
            for log_file in self.log_files:
                file_path = self.log_directory / log_file
                if file_path.exists():
                    try:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()[-50:]  # Últimas 50 líneas
                            parsed_lines = [self.parse_log_line(line) for line in lines if line.strip()]
                            self.log_data[log_file] = deque(parsed_lines, maxlen=100)
                    except Exception as e:
                        error_entry = {
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'level': 'ERROR',
                            'message': f'Error leyendo {log_file}: {str(e)}'
                        }
                        self.log_data[log_file].append(error_entry)
                        
            time.sleep(1)
            
    def get_colored_level(self, level):
        """Obtener color para nivel de log"""
        colors = {
            'DEBUG': curses.color_pair(4),    # Azul
            'INFO': curses.color_pair(2),     # Verde
            'WARNING': curses.color_pair(3),  # Amarillo
            'ERROR': curses.color_pair(1),    # Rojo
            'CRITICAL': curses.color_pair(1) | curses.A_BOLD  # Rojo brillante
        }
        return colors.get(level.upper(), curses.color_pair(0))
        
    def draw_screen(self):
        """Dibujar pantalla con datos de logs"""
        if not self.screen:
            return
            
        self.screen.clear()
        
        # Encabezado
        height, width = self.screen.getmaxyx()
        self.screen.addstr(0, 0, "=" * (width-1))
        self.screen.addstr(0, 2, f" VISUALIZADOR DE LOGS - KALIGHOST - {datetime.now().strftime('%H:%M:%S')} ")
        
        # Altura por sección de log
        section_height = (height - 4) // len(self.log_files)
        
        # Mostrar logs por archivo
        start_row = 2
        for i, (log_file, entries) in enumerate(self.log_data.items()):
            if start_row >= height - 2:
                break
                
            # Título de sección
            self.screen.addstr(start_row, 0, f"[{log_file}]", curses.A_BOLD)
            start_row += 1
            
            # Líneas de log
            for j, entry in enumerate(list(entries)[-section_height+2:]):
                if start_row >= height - 2:
                    break
                    
                try:
                    # Formatear línea
                    timestamp = entry['timestamp'][-8:]  # Solo HH:MM:SS
                    level = entry['level']
                    message = entry['message'][:width-30]  # Truncar si es muy largo
                    
                    # Dibujar línea con colores
                    self.screen.addstr(start_row, 0, f"{timestamp} ", curses.color_pair(5))
                    self.screen.addstr(start_row, 9, f"[{level:>7}] ", self.get_colored_level(level))
                    self.screen.addstr(start_row, 19, message)
                    
                    start_row += 1
                except curses.error:
                    # Pantalla demasiado pequeña
                    break
                    
            start_row += 1
            
        # Pie de página
        self.screen.addstr(height-1, 0, "q: Salir | r: Refrescar | Ctrl+C: Detener", curses.color_pair(6))
        
        self.screen.refresh()
        
    def run(self, screen):
        """Ejecutar visualizador"""
        self.screen = screen
        
        # Verificar si tenemos una terminal adecuada
        if not hasattr(screen, 'getmaxyx'):
            print("No se puede inicializar curses. Ejecuta este script en una terminal compatible.")
            return
            
        # Configurar colores
        try:
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)     # ERROR
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # INFO
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # WARNING
            curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)    # DEBUG
            curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Timestamp
            curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Footer
        except curses.error:
            # Si no podemos configurar colores, continuar sin ellos
            pass
        
        # Iniciar hilo de lectura de logs
        self.running = True
        log_thread = threading.Thread(target=self.read_logs, daemon=True)
        log_thread.start()
        
        # Bucle principal
        while self.running:
            self.draw_screen()
            
            # Leer entrada
            try:
                key = self.screen.getch()
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('r') or key == ord('R'):
                    # Refrescar manualmente
                    pass
            except KeyboardInterrupt:
                break
                
        self.running = False

def main():
    """Función principal"""
    # Verificar directorio de logs
    log_dir = Path(os.path.expanduser("~/KaliGhost/yrays-agent/logs"))
    if not log_dir.exists():
        print(f"Directorio de logs no encontrado: {log_dir}")
        print("Asegúrate de que los agentes estén corriendo")
        sys.exit(1)
        
    # Verificar si estamos en una terminal interactiva
    if not sys.stdin.isatty():
        print("Este script requiere una terminal interactiva con soporte de curses.")
        sys.exit(1)
        
    # Iniciar visualizador
    visualizer = LogVisualizer()
    try:
        curses.wrapper(visualizer.run)
    except curses.error as e:
        print(f"Error de curses: {e}")
        print("Este script requiere una terminal compatible con curses.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
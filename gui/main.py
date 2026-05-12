"""
GUI Principal de KaliGhost
Interfaz en PySide6 con estilo cyberpunk 3D
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# --- PySide6 ---
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                  QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame,
                                  QSplitter, QStatusBar, QMenuBar, QMenu)
from PySide6.QtCore import Qt, Signal, Slot, QObject, QTimer
from PySide6.QtGui import QFont, QColor, QPalette, QIcon, QAction, QMovie

# --- Rutas ---
KALIGHOST_DIR = Path(__file__).parent.parent
AGENT_DIR = KALIGHOST_DIR / "YrYs-Agent"
GUI_DIR = KALIGHOST_DIR / "gui"

# --- Estilos Cyberpunk ---
CYBERPUNK_STYLE = """
QMainWindow {
    background-color: #0a0a0a;
    color: #00ff88;
    font-family: 'Courier New', monospace;
}

QTextEdit, QLineEdit {
    background-color: #111111;
    color: #00ff88;
    border: 2px solid #00ff88;
    border-radius: 5px;
    padding: 8px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
}

QTextEdit {
    selection-background-color: #005f40;
}

QPushButton {
    background-color: #001f17;
    color: #00ff88;
    border: 2px solid #00ff88;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
    font-family: 'Courier New', monospace;
}

QPushButton:hover {
    background-color: #003324;
    border: 2px solid #00ffaa;
}

QPushButton:pressed {
    background-color: #00110e;
}

QLabel {
    color: #00ff88;
    font-family: 'Courier New', monospace;
    font-size: 16px;
}

QSplitter::handle {
    background-color: #00ff88;
    width: 2px;
}

QScrollArea, QFrame {
    border: 1px solid #003324;
    border-radius: 5px;
}

QStatusBar {
    background-color: #001f17;
    color: #00ff88;
    border-top: 1px solid #00ff88;
}
"""

class Stream(QObject):
    """Emite texto a la GUI desde stdout/stderr"""
    text_written = Signal(str)
    
    def write(self, text):
        self.text_written.emit(str(text))
    
    def flush(self):
        pass

class AgentInterface(QWidget):
    """
    Widget principal de interacción con YrYs-Agent
    """
    def __init__(self):
        super().__init__()
        self.agent_process = None
        self.setup_ui()
        self.setup_agent()
        self.setup_styles()
    
    def setup_ui(self):
        """Configura la interfaz principal"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # --- Header ---
        header_layout = QHBoxLayout()
        
        self.logo_label = QLabel("👾 YrYs-Agent")
        self.logo_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        self.status_label = QLabel("🟢 Listo")
        self.status_label.setStyleSheet("font-size: 14px; color: #00ff88;")
        
        header_layout.addWidget(self.logo_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        
        # --- Área de mensajes ---
        self.messages_area = QTextEdit()
        self.messages_area.setReadOnly(True)
        self.messages_area.setStyleSheet("border: none;")
        
        # Scroll area para mensajes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.messages_area)
        scroll.setStyleSheet("border: none;")
        
        # --- Entrada de usuario ---
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe una orden para YrYs-Agent...")
        self.input_field.returnPressed.connect(self.send_command)
        
        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_command)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        # --- Añadir al layout principal ---
        layout.addLayout(header_layout)
        layout.addWidget(scroll)
        layout.addLayout(input_layout)
    
    def setup_agent(self):
        """Configura la conexión con YrYs-Agent"""
        # Redirigir stdout/stderr
        sys.stdout = Stream(text_written=self.append_message)
        sys.stderr = Stream(text_written=self.append_message)
        
    @Slot(str)
    def append_message(self, text):
        """Añade mensaje al área de texto"""
        self.messages_area.append(text)
        # Auto-scroll
        scrollbar = self.messages_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_command(self):
        """Envía un comando al agente"""
        command = self.input_field.text().strip()
        if not command:
            return
        
        # Mostrar comando
        self.append_message(f"\n\033[1m[Usuario]\033[0m {command}\n")
        self.input_field.clear()
        
        # Ejecutar agente en segundo plano
        if self.agent_process is None or self.agent_process.poll() is not None:
            try:
                self.agent_process = subprocess.Popen(
                    ["python3", str(AGENT_DIR / "main.py")],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=str(AGENT_DIR)
                )
            except Exception as e:
                self.append_message(f"Error al iniciar el agente: {e}\n")
                return
        
        # Enviar comando
        self.agent_process.stdin.write(command + "\n")
        self.agent_process.stdin.flush()
        
        # Leer respuesta
        # Esto es solo un mock, en producción usaríamos una interfaz real
        self.append_message("Agente procesando... (mock)\n")
        QTimer.singleShot(1000, lambda: self.append_message("Mock: Tarea completada.\n"))
    
    def setup_styles(self):
        """Aplica estilos cyberpunk"""
        self.setStyleSheet(CYBERPUNK_STYLE)


class MainWindow(QMainWindow):
    """Ventana principal de KaliGhost"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KaliGhost - Sistema de Pentesting Autónomo")
        self.setGeometry(100, 100, 1000, 700)
        
        # Aplicar estilos
        self.setStyleSheet(CYBERPUNK_STYLE)
        
        # Crear widget central
        central_widget = AgentInterface()
        self.setCentralWidget(central_widget)
        
        # Crear menú
        self.create_menu()
        
        # Crear status bar
        self.statusBar().showMessage("KaliGhost listo. Agente IA autónomo cargado.")
    
    def create_menu(self):
        """Crea el menú de la aplicación"""
        menu_bar = self.menuBar()
        
        # Archivo
        file_menu = menu_bar.addMenu("Archivo")
        
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Herramientas
        tools_menu = menu_bar.addMenu("Herramientas")
        
        onboarding_action = QAction("Iniciar Onboarding", self)
        onboarding_action.triggered.connect(self.start_onboarding)
        tools_menu.addAction(onboarding_action)
        
        # Ayuda
        help_menu = menu_bar.addMenu("Ayuda")
        
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)
    
    def start_onboarding(self):
        """Inicia el asistente de configuración"""
        try:
            subprocess.run(["bash", str(KALIGHOST_DIR / "start_onboarding.sh")], check=True)
        except Exception as e:
            print(f"Error al iniciar onboarding: {e}")
    
    def about(self):
        """Muestra información sobre KaliGhost"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(self, "Acerca de KaliGhost", 
                         "KaliGhost v1.0.0\n\n" +
                         "Sistema de pentesting autónomo con IA integrada.\n" +
                         "Desarrollado por elKalivpn.\n\n" +
                         "YrYs-Agent: Asistente de seguridad autónomo en tiempo real.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
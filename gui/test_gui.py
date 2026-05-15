#!/usr/bin/env python3
"""
Script de prueba simple para verificar que la GUI funciona
"""

import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

def main():
    app = QApplication(sys.argv)
    
    # Crear ventana simple
    window = QWidget()
    window.setWindowTitle("Test KaliGhost GUI")
    window.resize(400, 200)
    
    # Crear layout y etiqueta
    layout = QVBoxLayout()
    label = QLabel("¡KaliGhost GUI está funcionando correctamente!")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 16px; color: #22AA55; font-weight: bold;")
    
    layout.addWidget(label)
    window.setLayout(layout)
    
    # Mostrar ventana
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
KaliGhost Professional GUI Demonstration
Showcases the advanced features of the professional cyberpunk interface
"""

import sys
import time
from pathlib import Path

# Add the gui directory to Python path
sys.path.append(str(Path(__file__).parent))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit, QGroupBox,
    QSplitter, QFrame
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import QTimer, Qt

class DemoWindow(QMainWindow):
    """Demonstration window showcasing professional GUI features"""
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.simulateActivity()
    
    def setupUI(self):
        """Setup demonstration UI"""
        self.setWindowTitle("KaliGhost Professional GUI Demo")
        self.setGeometry(200, 200, 1000, 700)
        
        # Professional styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0F0F1E;
            }
            QLabel {
                color: #DADADA;
            }
            QGroupBox {
                color: #22AA55;
                border: 1px solid #22AA55;
                margin-top: 1ex;
                font-weight: bold;
            }
            QPushButton {
                background-color: #22AA55;
                color: black;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #33BB66;
            }
            QTextEdit {
                background-color: #0A0A0A;
                color: #00FF00;
                border: 1px solid #22AA55;
                font-family: 'Monaco', 'Courier New';
            }
            QProgressBar {
                border: 1px solid #22AA55;
                border-radius: 3px;
                text-align: center;
                color: white;
                background-color: #181818;
            }
            QProgressBar::chunk {
                background-color: #22AA55;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🔥 KALIGHOST PROFESSIONAL GUI DEMONSTRATION")
        title_font = QFont("Arial", 16, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #22AA55; padding: 15px;")
        main_layout.addWidget(title)
        
        # Splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Features showcase
        left_panel = self.createFeaturesPanel()
        splitter.addWidget(left_panel)
        
        # Right panel - Live demo
        right_panel = self.createDemoPanel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([400, 600])
        main_layout.addWidget(splitter)
        
        # Bottom panel - Console
        console_panel = self.createConsolePanel()
        main_layout.addWidget(console_panel)
    
    def createFeaturesPanel(self):
        """Create features showcase panel"""
        panel = QGroupBox("✨ PROFESSIONAL FEATURES SHOWCASE")
        layout = QVBoxLayout()
        
        features = [
            "🐉 Advanced 3D Cyber Dragon with Real-time Animation",
            "🎨 Cyberpunk Theme with Professional Color Scheme",
            "⚡ Hardware-Accelerated Rendering with OpenGL",
            "📊 Real-time System Monitoring and Performance Metrics",
            "🛠️ Integrated Pentesting Tool Access",
            "🧠 YrYs Agent Status and Control Interface",
            "🔓 Security Mode Visualization (Ghost/Active)",
            "📈 Dynamic Data Visualization and Charts",
            "🔊 Audio Feedback and Sound Effects",
            "🎮 Interactive Controls and Widgets"
        ]
        
        for feature in features:
            label = QLabel(feature)
            label.setStyleSheet("color: #DADADA; padding: 5px;")
            layout.addWidget(label)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ START DEMO")
        self.start_btn.clicked.connect(self.startDemo)
        
        self.stop_btn = QPushButton("⏹ STOP DEMO")
        self.stop_btn.clicked.connect(self.stopDemo)
        self.stop_btn.setEnabled(False)
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)
        
        panel.setLayout(layout)
        return panel
    
    def createDemoPanel(self):
        """Create live demonstration panel"""
        panel = QGroupBox("🎮 LIVE DEMONSTRATION")
        layout = QVBoxLayout()
        
        # System stats simulation
        stats_layout = QHBoxLayout()
        
        # CPU Usage
        cpu_group = QGroupBox("🖥️ CPU USAGE")
        cpu_layout = QVBoxLayout()
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setValue(0)
        cpu_layout.addWidget(self.cpu_bar)
        cpu_group.setLayout(cpu_layout)
        stats_layout.addWidget(cpu_group)
        
        # Memory Usage
        mem_group = QGroupBox("💾 MEMORY USAGE")
        mem_layout = QVBoxLayout()
        self.mem_bar = QProgressBar()
        self.mem_bar.setRange(0, 100)
        self.mem_bar.setValue(0)
        mem_layout.addWidget(self.mem_bar)
        mem_group.setLayout(mem_layout)
        stats_layout.addWidget(mem_group)
        
        layout.addLayout(stats_layout)
        
        # Status indicators
        status_layout = QHBoxLayout()
        
        self.agent_status = QLabel("🔴 YrYs Agent: INACTIVE")
        self.agent_status.setStyleSheet("color: #FF5555; font-weight: bold;")
        
        self.dragon_status = QLabel("🟡 Dragon: INITIALIZING")
        self.dragon_status.setStyleSheet("color: #FFAA00; font-weight: bold;")
        
        self.security_status = QLabel("🟢 Security: NOMINAL")
        self.security_status.setStyleSheet("color: #22AA55; font-weight: bold;")
        
        status_layout.addWidget(self.agent_status)
        status_layout.addWidget(self.dragon_status)
        status_layout.addWidget(self.security_status)
        layout.addLayout(status_layout)
        
        panel.setLayout(layout)
        return panel
    
    def createConsolePanel(self):
        """Create console demonstration panel"""
        panel = QGroupBox("📟 OPERATION CONSOLE")
        layout = QVBoxLayout()
        
        self.console = QTextEdit()
        self.console.setMaximumHeight(150)
        self.console.append("[ демо ] KaliGhost Professional GUI Demo Started")
        self.console.append("[ инфо ] Initializing cyberpunk interface components")
        self.console.append("[ статус ] All systems nominal, ready for demonstration")
        
        layout.addWidget(self.console)
        panel.setLayout(layout)
        return panel
    
    def simulateActivity(self):
        """Simulate system activity for demonstration"""
        self.demo_timer = QTimer()
        self.demo_timer.timeout.connect(self.updateDemo)
        self.demo_counter = 0
    
    def startDemo(self):
        """Start demonstration"""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.demo_timer.start(500)  # Update twice per second
        
        self.console.append("[ запуск ] Starting professional demonstration sequence")
        self.console.append("[ активация ] Enabling advanced cyberpunk features")
        
        # Update status
        self.agent_status.setText("🟢 YrYs Agent: ACTIVE")
        self.agent_status.setStyleSheet("color: #22AA55; font-weight: bold;")
        
        self.dragon_status.setText("🟢 Dragon: RENDERING")
        self.dragon_status.setStyleSheet("color: #22AA55; font-weight: bold;")
    
    def stopDemo(self):
        """Stop demonstration"""
        self.demo_timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self.console.append("[ остановка ] Demonstration sequence terminated")
        self.console.append("[ завершено ] Professional GUI demo completed")
        
        # Reset status
        self.agent_status.setText("🔴 YrYs Agent: INACTIVE")
        self.agent_status.setStyleSheet("color: #FF5555; font-weight: bold;")
        
        self.dragon_status.setText("🟡 Dragon: PAUSED")
        self.dragon_status.setStyleSheet("color: #FFAA00; font-weight: bold;")
    
    def updateDemo(self):
        """Update demonstration"""
        self.demo_counter += 1
        
        # Simulate changing values
        import random
        cpu_val = 30 + random.randint(0, 40)
        mem_val = 40 + random.randint(0, 30)
        
        self.cpu_bar.setValue(cpu_val)
        self.mem_bar.setValue(mem_val)
        
        # Add periodic messages
        if self.demo_counter % 4 == 0:
            messages = [
                "[ рендеринг ] 3D dragon animation frame rendered",
                "[ оптимизация ] Cyberpunk effects optimized",
                "[ сеть ] Network monitoring active",
                "[ анализ ] Security protocols validated",
                "[ производительность ] Frame rate: 60 FPS",
                "[ система ] All professional features operational"
            ]
            self.console.append(random.choice(messages))

def main():
    """Main demonstration function"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show demo window
    demo_window = DemoWindow()
    demo_window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
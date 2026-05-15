#!/usr/bin/env python3
"""
KaliGhost GUI with 3D Animated Dragon
Using PySide6 and OpenGL for 3D rendering
"""

import sys
import math
import random
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QMenuBar, QStatusBar, QToolBar,
    QDockWidget, QTextEdit, QGroupBox, QGridLayout, QFrame
)
from PySide6.QtGui import (
    QIcon, QPixmap, QFont, QPalette, QColor, QAction, QPainter,
    QPen, QBrush, QVector3D
)
from PySide6.QtCore import QTimer, Qt, Slot, Signal, QObject
from PySide6.QtOpenGLWidgets import QOpenGLWidget

# Try to import OpenGL functions - handle different versions
try:
    from PySide6.QtOpenGL import QOpenGLFunctions
    OPENGL_FUNCTIONS_AVAILABLE = True
except ImportError:
    # In older versions, functions might be in QtGui or not available
    try:
        from PySide6.QtGui import QOpenGLFunctions
        OPENGL_FUNCTIONS_AVAILABLE = True
    except ImportError:
        OPENGL_FUNCTIONS_AVAILABLE = False

# Try to import OpenGL - handle case where it's not installed
try:
    import OpenGL.GL as gl
    from OpenGL.GL import *
    from OpenGL.GLU import *
    OPENGL_AVAILABLE = True
except ImportError:
    OPENGL_AVAILABLE = False
    print("Warning: OpenGL no disponible. La visualización 3D estará desactivada.")

class Dragon2DWidget(QWidget):
    """Widget de respaldo que muestra un dragón 2D cuando OpenGL no está disponible"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Dragón 2D de Kali Linux")
        
        # Parámetros de animación
        self.rotation = 0
        self.animation_speed = 1.0
        
        # Temporizador para animación
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)  # Más lento para 2D
    
    def paintEvent(self, event):
        """Dibujar el dragón 2D"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo oscuro
        painter.fillRect(self.rect(), QColor(24, 24, 24))
        
        # Guardar estado del painter
        painter.save()
        
        # Mover al centro
        center = self.rect().center()
        painter.translate(center)
        
        # Rotar según animación
        painter.rotate(self.rotation)
        
        # Dibujar dragón 2D estilizado
        self.draw_2d_dragon(painter)
        
        # Restaurar estado del painter
        painter.restore()
        
        # Dibujar texto informativo
        painter.setPen(QColor(34, 170, 85))  # Verde Kali
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        if not OPENGL_AVAILABLE:
            painter.drawText(self.rect(), Qt.AlignBottom | Qt.AlignHCenter, 
                           "OpenGL no disponible - mostrando versión 2D\nInstale PyOpenGL para la experiencia 3D completa")
    
    def draw_2d_dragon(self, painter):
        """Dibujar una representación 2D estilizada del dragón"""
        # Configurar color verde característico de Kali
        painter.setPen(QPen(QColor(34, 170, 85), 3))
        painter.setBrush(QBrush(QColor(34, 170, 85, 100)))
        
        # Cuerpo principal (elipse)
        body_rect = QRect(-100, -30, 200, 60)
        painter.drawEllipse(body_rect)
        
        # Cabeza
        painter.setBrush(QBrush(QColor(34, 170, 85, 150)))
        head_rect = QRect(80, -25, 50, 50)
        painter.drawEllipse(head_rect)
        
        # Ojos brillantes
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        painter.drawEllipse(95, -15, 8, 8)  # Ojo izquierdo
        painter.drawEllipse(115, -15, 8, 8)  # Ojo derecho
        
        # Alas (animadas)
        wing_offset = math.sin(self.rotation * 0.2) * 10
        painter.setPen(QPen(QColor(0, 200, 100), 2))
        painter.setBrush(QBrush(QColor(0, 200, 100, 80)))
        
        # Ala izquierda
        left_wing = QPolygon([
            QPoint(-50, -40),
            QPoint(-100, -80 + wing_offset),
            QPoint(-70, -60),
            QPoint(-50, -40)
        ])
        painter.drawPolygon(left_wing)
        
        # Ala derecha
        right_wing = QPolygon([
            QPoint(-50, 40),
            QPoint(-100, 80 - wing_offset),
            QPoint(-70, 60),
            QPoint(-50, 40)
        ])
        painter.drawPolygon(right_wing)
        
        # Cola
        painter.setPen(QPen(QColor(34, 170, 85), 3))
        tail_path = QPainterPath()
        tail_path.moveTo(-100, 0)
        tail_path.cubicTo(-130, -20, -150, 20, -170, 0)
        painter.drawPath(tail_path)
        
        # Patas
        painter.setPen(QPen(QColor(20, 120, 60), 4))
        # Patas delanteras
        painter.drawLine(50, 30, 60, 60)
        painter.drawLine(50, -30, 60, -60)
        # Patas traseras
        painter.drawLine(-50, 30, -40, 60)
        painter.drawLine(-50, -30, -40, -60)
    
    def animate(self):
        """Animar el dragón 2D"""
        self.rotation += 2 * self.animation_speed
        self.update()

# Create dummy classes for when OpenGL is not available
if not OPENGL_AVAILABLE:
    class QOpenGLWidget(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Dragón 2D de Kali Linux - OpenGL no disponible")
            
        def initializeGL(self):
            pass
            
        def resizeGL(self, width, height):
            pass
            
        def paintGL(self):
            # Replace with 2D widget when OpenGL is not available
            pass

class Dragon3DRenderer(QOpenGLWidget):
    """Widget para renderizar el dragón 3D de Kali Linux"""

class Dragon3DRenderer(QOpenGLWidget):
    """Widget para renderizar el dragón 3D de Kali Linux"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Dragón 3D de Kali Linux")
        
        # Parámetros de animación
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.scale = 1.0
        self.animation_speed = 1.0
        
        # Temporizador para animación
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS
        
        # Colores característicos de Kali Linux
        self.kali_green = (0.13, 0.67, 0.33)  # #22AA55
        self.kali_dark = (0.09, 0.09, 0.09)   # #181818
        self.kali_light = (0.85, 0.85, 0.85)  # #DADADA
        
        # Parámetros del dragón
        self.dragon_parts = []
        self.initialize_dragon()
        
        # Check if OpenGL is available, if not, create 2D version
        if not OPENGL_AVAILABLE:
            self.timer.stop()
            # Replace with 2D widget functionality
            self.rotation = 0
    
    def initialize_dragon(self):
        """Inicializar las partes del dragón"""
        # Crear partes básicas del dragón
        self.dragon_parts = [
            {"type": "body", "position": [0, 0, 0], "size": [2, 1, 1]},
            {"type": "head", "position": [1.5, 0.3, 0], "size": [0.8, 0.8, 0.8]},
            {"type": "tail", "position": [-1.2, 0, 0], "size": [1.5, 0.3, 0.3]},
            {"type": "wing_left", "position": [0, 0.5, 0.8], "size": [1, 0.1, 1.2]},
            {"type": "wing_right", "position": [0, 0.5, -0.8], "size": [1, 0.1, 1.2]},
            {"type": "leg_front_left", "position": [0.8, -0.8, 0.4], "size": [0.2, 0.8, 0.2]},
            {"type": "leg_front_right", "position": [0.8, -0.8, -0.4], "size": [0.2, 0.8, 0.2]},
            {"type": "leg_back_left", "position": [-0.8, -0.8, 0.4], "size": [0.2, 0.8, 0.2]},
            {"type": "leg_back_right", "position": [-0.8, -0.8, -0.4], "size": [0.2, 0.8, 0.2]},
        ]
    
    def initializeGL(self):
        """Inicializar OpenGL"""
        if not OPENGL_AVAILABLE:
            return
            
        # Only try to initialize OpenGL functions if they're available
        if OPENGL_FUNCTIONS_AVAILABLE:
            try:
                self.initializeOpenGLFunctions()
            except:
                pass
                
        glClearColor(*self.kali_dark, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    def resizeGL(self, width, height):
        """Redimensionar la vista OpenGL"""
        if not OPENGL_AVAILABLE:
            return
            
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / height if height > 0 else 1
        gluPerspective(45, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        """Renderizar la escena"""
        if not OPENGL_AVAILABLE:
            # Use QPainter for 2D rendering when OpenGL is not available
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Fondo oscuro
            painter.fillRect(self.rect(), QColor(24, 24, 24))
            
            # Guardar estado del painter
            painter.save()
            
            # Mover al centro
            center = self.rect().center()
            painter.translate(center)
            
            # Rotar según animación
            painter.rotate(self.rotation)
            
            # Dibujar dragón 2D estilizado
            self.draw_2d_dragon_simple(painter)
            
            # Restaurar estado del painter
            painter.restore()
            
            # Dibujar texto informativo
            painter.setPen(QColor(34, 170, 85))  # Verde Kali
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignBottom | Qt.AlignHCenter, 
                           "OpenGL no disponible - mostrando versión 2D\nInstale PyOpenGL para la experiencia 3D completa")
            return
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Configurar la cámara
        glTranslatef(0, 0, -8)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glRotatef(self.rotation_z, 0, 0, 1)
        glScalef(self.scale, self.scale, self.scale)
        
        # Luz ambiental
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1.0])
        
        # Renderizar cada parte del dragón
        for part in self.dragon_parts:
            self.render_dragon_part(part)
        
        # Añadir efecto de brillo especial
        self.render_special_effects()
    
    def draw_2d_dragon_simple(self, painter):
        """Dibujar una representación 2D simplificada del dragón para el widget OpenGL"""
        # Configurar color verde característico de Kali
        painter.setPen(QPen(QColor(34, 170, 85), 3))
        painter.setBrush(QBrush(QColor(34, 170, 85, 100)))
        
        # Cuerpo principal (elipse)
        body_rect = QRect(-100, -30, 200, 60)
        painter.drawEllipse(body_rect)
        
        # Cabeza
        painter.setBrush(QBrush(QColor(34, 170, 85, 150)))
        head_rect = QRect(80, -25, 50, 50)
        painter.drawEllipse(head_rect)
        
        # Ojos brillantes
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        painter.drawEllipse(95, -15, 8, 8)  # Ojo izquierdo
        painter.drawEllipse(115, -15, 8, 8)  # Ojo derecho
        
        # Alas (animadas)
        wing_offset = math.sin(self.rotation * 0.2) * 10
        painter.setPen(QPen(QColor(0, 200, 100), 2))
        painter.setBrush(QBrush(QColor(0, 200, 100, 80)))
        
        # Ala izquierda
        left_wing = QPolygon([
            QPoint(-50, -40),
            QPoint(-100, -80 + wing_offset),
            QPoint(-70, -60),
            QPoint(-50, -40)
        ])
        painter.drawPolygon(left_wing)
        
        # Ala derecha
        right_wing = QPolygon([
            QPoint(-50, 40),
            QPoint(-100, 80 - wing_offset),
            QPoint(-70, 60),
            QPoint(-50, 40)
        ])
        painter.drawPolygon(right_wing)
        
        # Cola
        painter.setPen(QPen(QColor(34, 170, 85), 3))
        tail_path = QPainterPath()
        tail_path.moveTo(-100, 0)
        tail_path.cubicTo(-130, -20, -150, 20, -170, 0)
        painter.drawPath(tail_path)
        
        # Patas
        painter.setPen(QPen(QColor(20, 120, 60), 4))
        # Patas delanteras
        painter.drawLine(50, 30, 60, 60)
        painter.drawLine(50, -30, 60, -60)
        # Patas traseras
        painter.drawLine(-50, 30, -40, 60)
        painter.drawLine(-50, -30, -40, -60)
    
    def render_dragon_part(self, part):
        """Renderizar una parte del dragón"""
        if not OPENGL_AVAILABLE:
            return
            
        glPushMatrix()
        
        # Posición de la parte
        position = part["position"]
        glTranslatef(position[0], position[1], position[2])
        
        # Tamaño de la parte
        size = part["size"]
        
        # Color según el tipo de parte
        if part["type"] == "head":
            glColor3f(*self.kali_green)
        elif "wing" in part["type"]:
            glColor3f(0.0, 0.8, 0.4)  # Verde brillante para alas
        elif "leg" in part["type"]:
            glColor3f(0.2, 0.5, 0.2)  # Verde oscuro para patas
        else:
            glColor3f(*self.kali_green)
        
        # Animación de alas (movimiento)
        if "wing" in part["type"]:
            wing_angle = math.sin(self.rotation_y * 0.1) * 30
            if "left" in part["type"]:
                glRotatef(wing_angle, 0, 1, 0)
            else:
                glRotatef(-wing_angle, 0, 1, 0)
        
        # Crear la geometría de la parte
        self.draw_cube(size[0], size[1], size[2])
        
        glPopMatrix()
    
    def draw_cube(self, width, height, depth):
        """Dibujar un cubo como parte del dragón"""
        if not OPENGL_AVAILABLE:
            return
            
        w, h, d = width/2, height/2, depth/2
        
        glBegin(GL_QUADS)
        # Frente
        glVertex3f(-w, -h, d)
        glVertex3f(w, -h, d)
        glVertex3f(w, h, d)
        glVertex3f(-w, h, d)
        
        # Atrás
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(w, -h, -d)
        
        # Arriba
        glVertex3f(-w, h, -d)
        glVertex3f(-w, h, d)
        glVertex3f(w, h, d)
        glVertex3f(w, h, -d)
        
        # Abajo
        glVertex3f(-w, -h, -d)
        glVertex3f(w, -h, -d)
        glVertex3f(w, -h, d)
        glVertex3f(-w, -h, d)
        
        # Derecha
        glVertex3f(w, -h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(w, h, d)
        glVertex3f(w, -h, d)
        
        # Izquierda
        glVertex3f(-w, -h, -d)
        glVertex3f(-w, -h, d)
        glVertex3f(-w, h, d)
        glVertex3f(-w, h, -d)
        glEnd()
    
    def render_special_effects(self):
        """Renderizar efectos especiales del dragón"""
        if not OPENGL_AVAILABLE:
            return
            
        # Efecto de energía en los ojos
        glPushMatrix()
        glTranslatef(1.8, 0.4, 0.2)  # Ojo izquierdo
        glColor3f(0.0, 1.0, 0.0)  # Verde brillante
        self.draw_sphere(0.1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(1.8, 0.4, -0.2)  # Ojo derecho
        glColor3f(0.0, 1.0, 0.0)  # Verde brillante
        self.draw_sphere(0.1)
        glPopMatrix()
        
        # Partículas de energía
        self.render_energy_particles()
    
    def draw_sphere(self, radius):
        """Dibujar una esfera simple"""
        if not OPENGL_AVAILABLE:
            return
            
        quad = gluNewQuadric()
        gluSphere(quad, radius, 10, 10)
        gluDeleteQuadric(quad)
    
    def render_energy_particles(self):
        """Renderizar partículas de energía"""
        if not OPENGL_AVAILABLE:
            return
            
        for i in range(20):
            angle = (self.rotation_y + i * 18) % 360
            radius = 2.5 + math.sin(self.rotation_y * 0.05 + i) * 0.5
            x = math.cos(math.radians(angle)) * radius
            y = math.sin(math.radians(i * 18)) * 0.5
            z = math.sin(math.radians(angle)) * radius
            
            glPushMatrix()
            glTranslatef(x, y, z)
            # Color pulsante
            pulse = (math.sin(self.rotation_y * 0.1 + i) + 1) / 2
            glColor3f(0.0, pulse, 0.0)
            self.draw_sphere(0.05)
            glPopMatrix()
    
    @Slot()
    def animate(self):
        """Animar el dragón"""
        if not OPENGL_AVAILABLE:
            # Animate 2D version
            self.rotation += 2 * self.animation_speed
            self.update()
            return
            
        self.rotation_y += 1 * self.animation_speed
        self.rotation_x = math.sin(self.rotation_y * 0.02) * 10
        self.rotation_z = math.cos(self.rotation_y * 0.03) * 5
        self.update()
    
    def set_animation_speed(self, speed):
        """Configurar velocidad de animación"""
        self.animation_speed = speed / 10.0
    
    def set_scale(self, scale):
        """Configurar escala del dragón"""
        if OPENGL_AVAILABLE:
            self.scale = scale / 50.0 + 0.5
        # For 2D, we could adjust the size of the drawing, but for simplicity we'll just ignore

class KaliGhostMainWindow(QMainWindow):
    """Ventana principal de KaliGhost con dragón 3D"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        self.setWindowTitle("KaliGhost - Sistema de Pentesting Avanzado")
        self.setGeometry(100, 100, 1200, 800)
        
        # Configurar estilo cyberpunk
        self.setup_style()
        
        # Crear widgets centrales
        self.create_central_widget()
        
        # Crear barra de menú
        self.create_menu_bar()
        
        # Crear barra de herramientas
        self.create_toolbar()
        
        # Crear barra de estado
        self.create_status_bar()
        
        # Crear paneles dock
        self.create_dock_widgets()
    
    def setup_style(self):
        """Configurar estilo cyberpunk"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(24, 24, 24))  # #181818
        palette.setColor(QPalette.WindowText, QColor(218, 218, 218))  # #DADADA
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
        palette.setColor(QPalette.ToolTipBase, QColor(218, 218, 218))
        palette.setColor(QPalette.ToolTipText, QColor(24, 24, 24))
        palette.setColor(QPalette.Text, QColor(218, 218, 218))
        palette.setColor(QPalette.Button, QColor(35, 35, 35))
        palette.setColor(QPalette.ButtonText, QColor(34, 170, 85))  # #22AA55
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(34, 170, 85))
        palette.setColor(QPalette.Highlight, QColor(34, 170, 85))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(palette)
        
        # Fuente personalizada
        font = QFont("Monaco", 10)
        self.setFont(font)
    
    def create_central_widget(self):
        """Crear widget central con el dragón 3D"""
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel("KALIGHOST - DRAGÓN 3D")
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #22AA55; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Renderer del dragón 3D
        self.dragon_renderer = Dragon3DRenderer()
        
        # Controles
        controls_layout = self.create_controls()
        
        # Agregar widgets al layout
        layout.addWidget(title_label)
        layout.addWidget(self.dragon_renderer)
        layout.addLayout(controls_layout)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def create_controls(self):
        """Crear controles para la animación del dragón"""
        controls_layout = QHBoxLayout()
        
        # Grupo de controles de animación
        animation_group = QGroupBox("Controles de Animación")
        animation_layout = QVBoxLayout()
        
        # Slider de velocidad
        speed_label = QLabel("Velocidad:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(0, 20)
        self.speed_slider.setValue(10)
        self.speed_slider.valueChanged.connect(self.change_speed)
        
        # Slider de escala
        scale_label = QLabel("Tamaño:")
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(0, 100)
        self.scale_slider.setValue(50)
        self.scale_slider.valueChanged.connect(self.change_scale)
        
        # Botones de control
        button_layout = QHBoxLayout()
        pause_button = QPushButton("⏸️ Pausar")
        pause_button.clicked.connect(self.toggle_pause)
        
        reset_button = QPushButton("🔄 Reiniciar")
        reset_button.clicked.connect(self.reset_animation)
        
        button_layout.addWidget(pause_button)
        button_layout.addWidget(reset_button)
        
        # Agregar controles al layout
        animation_layout.addWidget(speed_label)
        animation_layout.addWidget(self.speed_slider)
        animation_layout.addWidget(scale_label)
        animation_layout.addWidget(self.scale_slider)
        animation_layout.addLayout(button_layout)
        
        animation_group.setLayout(animation_layout)
        controls_layout.addWidget(animation_group)
        
        # Grupo de información del sistema
        info_group = QGroupBox("Información del Sistema")
        info_layout = QVBoxLayout()
        
        info_label = QLabel(
            "Agente YrYs: ✅ Activo\n"
            "Herramientas: ✅ Cargadas\n"
            "Modo Fantasma: ⚠️ Desactivado\n"
            "Particiones: ✅ Montadas"
        )
        info_label.setStyleSheet("color: #DADADA; font-family: Monaco;")
        info_layout.addWidget(info_label)
        
        info_group.setLayout(info_layout)
        controls_layout.addWidget(info_group)
        
        return controls_layout
    
    def create_menu_bar(self):
        """Crear barra de menú"""
        menu_bar = self.menuBar()
        
        # Menú Archivo
        file_menu = menu_bar.addMenu("Archivo")
        
        new_action = QAction("Nuevo Proyecto", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)
        
        open_action = QAction("Abrir Proyecto", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Herramientas
        tools_menu = menu_bar.addMenu("Herramientas")
        
        nmap_action = QAction("Nmap Scanner", self)
        tools_menu.addAction(nmap_action)
        
        metasploit_action = QAction("Metasploit Framework", self)
        tools_menu.addAction(metasploit_action)
        
        tools_menu.addSeparator()
        
        fuzzing_action = QAction("Fuzzing Tools", self)
        tools_menu.addAction(fuzzing_action)
        
        # Menú Ayuda
        help_menu = menu_bar.addMenu("Ayuda")
        
        docs_action = QAction("Documentación", self)
        help_menu.addAction(docs_action)
        
        about_action = QAction("Acerca de KaliGhost", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Crear barra de herramientas"""
        toolbar = self.addToolBar("Herramientas Principales")
        
        # Botones de herramientas
        scan_action = QAction("🔍 Escanear", self)
        toolbar.addAction(scan_action)
        
        exploit_action = QAction("⚔️ Explotar", self)
        toolbar.addAction(exploit_action)
        
        analyze_action = QAction("📊 Analizar", self)
        toolbar.addAction(analyze_action)
        
        report_action = QAction("📋 Reportar", self)
        toolbar.addAction(report_action)
    
    def create_status_bar(self):
        """Crear barra de estado"""
        self.statusBar().showMessage("KaliGhost listo - Dragón 3D animado cargado")
    
    def create_dock_widgets(self):
        """Crear paneles dock"""
        # Panel de consola
        console_dock = QDockWidget("Consola del Sistema", self)
        console_widget = QTextEdit()
        console_widget.setReadOnly(True)
        console_widget.append("[$] Bienvenido a KaliGhost")
        console_widget.append("[$] Sistema iniciado correctamente")
        console_widget.append("[$] Agente YrYs activo y escuchando")
        console_widget.append("[$] Dragón 3D cargado y animado")
        console_dock.setWidget(console_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)
        
        # Panel de tareas
        tasks_dock = QDockWidget("Tareas Activas", self)
        tasks_widget = QTextEdit()
        tasks_widget.setReadOnly(True)
        tasks_widget.append("✓ Análisis de red en progreso...")
        tasks_widget.append("✓ Monitoreo de servicios activo")
        tasks_widget.append("✓ Backup automático programado")
        tasks_dock.setWidget(tasks_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, tasks_dock)
    
    @Slot(int)
    def change_speed(self, value):
        """Cambiar velocidad de animación"""
        self.dragon_renderer.set_animation_speed(value)
        self.statusBar().showMessage(f"Velocidad ajustada a {value/10.0}x")
    
    @Slot(int)
    def change_scale(self, value):
        """Cambiar escala del dragón"""
        self.dragon_renderer.set_scale(value)
        self.statusBar().showMessage(f"Tamaño ajustado a {value}%")
    
    @Slot()
    def toggle_pause(self):
        """Alternar pausa de animación"""
        if self.dragon_renderer.timer.isActive():
            self.dragon_renderer.timer.stop()
            self.statusBar().showMessage("_Animación pausada")
        else:
            self.dragon_renderer.timer.start(16)
            self.statusBar().showMessage("Animación reanudada")
    
    @Slot()
    def reset_animation(self):
        """Reiniciar animación"""
        self.dragon_renderer.rotation_x = 0
        self.dragon_renderer.rotation_y = 0
        self.dragon_renderer.rotation_z = 0
        self.speed_slider.setValue(10)
        self.scale_slider.setValue(50)
        self.statusBar().showMessage("Animación reiniciada")
    
    @Slot()
    def show_about(self):
        """Mostrar información sobre KaliGhost"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "Acerca de KaliGhost",
            "<h2>KaliGhost v1.0</h2>"
            "<p>Sistema avanzado de pentesting con IA</p>"
            "<p><b>Características:</b></p>"
            "<ul>"
            "<li>Agente YrYs con IA nativa</li>"
            "<li>GUI cyberpunk con dragón 3D animado</li>"
            "<li>Más de 60 herramientas de pentesting integradas</li>"
            "<li>Modo Fantasma (similar a Tails OS)</li>"
            "<li>Automatización completa de workflows</li>"
            "</ul>"
            "<p style='color: #22AA55;'>Desarrollado por el equipo KaliGhost</p>"
        )

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Configurar icono de la aplicación (si existe)
    icon_path = Path(__file__).parent / "assets" / "kalighost_icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Crear y mostrar ventana principal
    window = KaliGhostMainWindow()
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
# YrYs Pro - Agente de Ciberseguridad Autónomo

## 🚀 Descripción

YrYs Pro es una evolución avanzada del agente autónomo de pentesting YrYs-Agent, equipado con capacidades mejoradas de auto-aprendizaje, razonamiento multimodal, planificación autónoma y ejecución segura.

## 🎯 Características Principales

### 🔍 Auto-Aprendizaje RAG
- Aprende continuamente de nuevas fuentes de información
- Recupera y combina conocimiento para mejorar respuestas
- Mantiene base de conocimiento actualizada automáticamente

### 🧠 Razonamiento Multimodal
- Procesa texto, imágenes y código simultáneamente
- Interpreta capturas de pantalla y diagramas técnicos
- Combina múltiples tipos de entrada para mejor comprensión

### 📋 Planificación Autónoma
- Genera planes complejos de pentesting sin intervención humana
- Se adapta dinámicamente basado en resultados parciales
- Optimiza uso de recursos y tiempo de ejecución

### 🛡️ Ejecución Segura
- Validación exhaustiva de comandos antes de ejecutar
- Entornos aislados para operaciones sensibles
- Monitoreo en tiempo real y controles de acceso robustos

## 📁 Estructura del Proyecto

```
YrYs-Pro/
├── docs/                     # Documentación técnica
│   ├── technical_spec.md     # Especificaciones técnicas completas
│   └── architecture.md       # Diagramas y arquitectura
├── src/                      # Código fuente
│   ├── core/                 # Componentes principales
│   ├── agents/               # Implementación de agentes
│   ├── rag/                  # Sistema RAG
│   ├── planning/             # Motor de planificación
│   ├── execution/            # Capa de ejecución segura
│   └── utils/                # Utilidades auxiliares
├── config/                   # Archivos de configuración
├── tests/                    # Pruebas unitarias e integración
└── scripts/                  # Scripts de instalación y utilidades
```

## 🛠️ Requisitos del Sistema

- **Sistema Operativo**: Linux (Ubuntu/Kali Linux)
- **Python**: 3.9+
- **Memoria RAM**: 16GB mínimos (32GB recomendados)
- **Almacenamiento**: 100GB libres
- **Docker**: Para ejecución segura en contenedores

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/kalighost/yr-ys-pro.git
cd yr-ys-pro

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar agente
python src/main.py --mode auto
```

## 📖 Documentación

Para información detallada técnica, consulte las [Especificaciones Técnicas Completas](./docs/technical_spec.md).

## 🤝 Contribuciones

Contribuciones bienvenidas. Por favor revise nuestra guía de contribución.

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.
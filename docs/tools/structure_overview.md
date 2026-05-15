# 📁 Estructura Completa de Documentación de Herramientas - KaliGhost

## 📂 Directorio Principal: `/docs/tools/`

### 📄 Archivos de Documentación Individual
- `nmap_guide.md` - Guía completa de Nmap (8000+ líneas)
- `metasploit_guide.md` - Documentación exhaustiva de Metasploit (15000+ líneas)
- `FUZZING_TOOLS.md` - Documentación detallada de herramientas de fuzzing
- `COMPLETE_PENTEST_TOOLS_GUIDE.md` - Guía integral de todas las herramientas

### 📋 Archivos de Índice y Navegación
- `INDEX.md` - Índice detallado de toda la documentación
- `README.md` - Punto de entrada y descripción general
- `TOC.md` - Tabla de contenidos estructurada

### 📁 Subdirectorios Especializados

#### 📂 `/docs/tools/web/`
Herramientas especializadas en aplicaciones web:
- `web_app_scanning.md` - Escaneo de aplicaciones web
- `api_testing_guide.md` - Testing de APIs REST/SOAP
- `mobile_app_testing.md` - Testing de aplicaciones móviles
- `web_proxy_manual.md` - Uso avanzado de proxies web

#### 📂 `/docs/tools/network/`
Herramientas de red y sistemas:
- `network_scanning.md` - Escaneo avanzado de redes
- `wireless_testing.md` - Testing de redes inalámbricas
- `bluetooth_security.md` - Seguridad Bluetooth
- `iot_device_testing.md` - Testing de dispositivos IoT

#### 📂 `/docs/tools/exploitation/`
Herramientas de explotación:
- `binary_exploitation.md` - Explotación de binarios
- `reverse_engineering.md` - Ingeniería inversa
- `malware_analysis.md` - Análisis de malware
- `privilege_escalation.md` - Escalación de privilegios

#### 📂 `/docs/tools/forensics/`
Herramientas forenses:
- `digital_forensics.md` - Forensia digital
- `memory_analysis.md` - Análisis de memoria
- `disk_imaging.md` - Creación de imágenes de disco
- `log_analysis.md` - Análisis de logs

#### 📂 `/docs/tools/social_engineering/`
Herramientas de ingeniería social:
- `phishing_frameworks.md` - Frameworks de phishing
- `pretexting_guide.md` - Guía de pretexting
- `physical_security.md` - Seguridad física
- `human_psychology.md` - Psicología humana en seguridad

## 📊 Estadísticas de la Documentación

### 📈 Cobertura de Herramientas
| Categoría | Herramientas Documentadas | Profundidad |
|-----------|--------------------------|-------------|
| Escaneo de Red | 15 | ★★★★☆ |
| Web Application | 12 | ★★★★★ |
| Explotación | 8 | ★★★★☆ |
| Análisis Forense | 10 | ★★★☆☆ |
| Cracking | 6 | ★★★★☆ |
| Wireless | 7 | ★★★☆☆ |
| Social Engineering | 5 | ★★☆☆☆ |
| **Total** | **63** | **★★★★☆** |

### 📚 Formatos de Documentación
- **Markdown**: 95% de documentos
- **PDF**: Guías de referencia rápida
- **HTML**: Documentación interactiva
- **Video Tutoriales**: Demos en proceso

### 🔄 Actualizaciones y Mantenimiento
- **Frecuencia**: Actualización mensual
- **Responsables**: Equipo de Desarrollo de KaliGhost
- **Revisión**: Comunidad de seguridad
- **Feedback**: Sistema de issues en GitHub

## 🔍 Sistema de Búsqueda

### 🎯 Búsqueda por Herramienta
```bash
# Buscar documentación específica
find /docs/tools/ -name "*.md" -exec grep -l "nmap\|Nmap\|NMAP" {} \;

# Buscar por categoría
find /docs/tools/*/ -name "*.md" -path "*/web/*"

# Buscar ejemplos de comandos
grep -r "^\s*\`.*\`$" /docs/tools/ | head -10
```

### 🔍 Índice de Búsqueda Rápida
- **[Nmap Index](./nmap_index.html)** - Búsqueda rápida en documentación de Nmap
- **[Metasploit Search](./metasploit_search.html)** - Motor de búsqueda en docs de Metasploit
- **[Web Tools Finder](./web_tools_finder.html)** - Localizador de herramientas web

## 🤝 Integración con Otros Recursos

### 📚 Documentación Externa Enlazada
- **[Nmap Official Docs](https://nmap.org/book/man.html)** - Manual oficial de Nmap
- **[Metasploit Unleashed](https://www.offensive-security.com/metasploit-unleashed/)** - Curso oficial gratuito
- **[OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)** - Guía de testing web
- **[Portswigger Web Academy](https://portswigger.net/web-security)** - Academia de seguridad web

### 🎥 Recursos Multimedia
- **YouTube Channels**: Enlaces a canales educativos
- **Conference Talks**: Charlas técnicas relevantes
- **Podcasts**: Podcasts de seguridad recomendados
- **Webinars**: Sesiones en vivo grabadas

## 🛠️ Herramientas de Mantenimiento

### 📝 Scripts de Validación
- `validate_links.py` - Verificación de enlaces rotos
- `check_formatting.py` - Validación de formato Markdown
- `update_toc.py` - Actualización automática de índices
- `spell_check.py` - Corrección ortográfica

### 🔄 Procesos de Actualización
1. **Revisión Mensual**: Auditoría de contenido
2. **Testing de Comandos**: Validación en entorno KaliGhost
3. **Feedback de Usuarios**: Incorporación de sugerencias
4. **Actualización de Versiones**: Sincronización con releases

---

📅 **Última actualización**: 2026-05-15  
📍 **Mantenimiento**: Equipo de Documentación de KaliGhost  
🔐 **Acceso**: Documentación interna del proyecto

⚠️ **Nota**: Esta estructura se actualiza continuamente. Consulte regularmente para nuevas adiciones.
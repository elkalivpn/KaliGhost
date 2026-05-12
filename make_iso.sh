#!/bin/bash
# Script para crear la imagen ISO de KaliGhost

set -e

# --- Variables ---
ISO_NAME="KaliGhost-$(date +%Y%m%d).iso"
WORK_DIR="/tmp/kalighost-build"
BUILD_DIR="$WORK_DIR/live"
ISO_DIR="/Users/mrhardcore/Desktop"
ARCH="amd64"

# --- Limpiar entorno ---
if [ -d "$WORK_DIR" ]; then
    echo "🧹 Limpiando directorio de trabajo anterior..."
    rm -rf "$WORK_DIR"
fi

# --- Crear estructura ---
echo "📁 Crear estructura de directorios..."
mkdir -p "$BUILD_DIR"
mkdir -p "$ISO_DIR"

# --- Copiar el sistema ---
# En producción, aquí se clonaría una base Kali minimal
# y se copiaría todo nuestro sistema encima

echo "📦 Copiando KaliGhost al directorio de build..."
cp -r /Users/mrhardcore/KaliGhost/* "$BUILD_DIR/"

# --- Permisos ---
echo "🔧 Ajustando permisos..."
# Skipping chown on macOS
chmod -R 755 "$BUILD_DIR"

# --- Crear ISO con hdiutil (macOS) ---
echo "💿 Creando imagen ISO: $ISO_NAME"
echo "   Salida: $ISO_DIR/$ISO_NAME"

# Crear ISO directamente
hdiutil makehybrid \
    -iso \
    -joliet \
    -o "$ISO_DIR/$ISO_NAME" \
    "$BUILD_DIR"

# --- Verificar ---
echo "🔍 Verificando ISO..."
if [ -f "$ISO_DIR/$ISO_NAME" ]; then
    echo "  📦 Peso: $(du -h "$ISO_DIR/$ISO_NAME" | cut -f1)"
    echo "  ✅ Imagen ISO creada exitosamente"
    echo "    Ubicación: $ISO_DIR/$ISO_NAME"
else
    echo "  ❌ Error: No se creó la ISO"
    exit 1
fi

# --- Limpieza final ---
echo "🧹 Limpiando directorio temporal..."
sudo rm -rf "$WORK_DIR"

echo "🎉 KaliGhost ISO lista para distribución!"
echo "   Nombre: $ISO_NAME"
echo "   Ubicación: $ISO_DIR/$ISO_NAME"
echo "   Tamaño: $(du -h "$ISO_DIR/$ISO_NAME" | cut -f1)"
echo "\n➡️  Puedes probarla con:"
echo "   qemu-system-x86_64 -cdrom $ISO_DIR/$ISO_NAME -boot d -m 2048"

echo "\n💡 Recuerda:"
echo "   - El modo GHOST borra todo al apagar"
echo "   - El modo DISK persiste configuraciones"
echo "   - YrYs-Agent empieza con autoconfianza al 100%"

echo "\n🚀 ¡Felicidades por tu lanzamiento!"
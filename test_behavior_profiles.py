#!/usr/bin/env python3
"""
Script para probar el sistema de perfiles de comportamiento de YrYs-Agent
"""

import sys
import os
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_behavior_profiles():
    """Prueba el sistema de perfiles de comportamiento"""
    try:
        # Importar el sistema de perfiles
        from behavior_profiles import get_profile_manager, BehaviorMode
        
        # Obtener el gestor de perfiles
        profile_manager = get_profile_manager()
        print("✅ Gestor de perfiles creado correctamente")
        
        # Listar perfiles disponibles
        profiles = profile_manager.list_profiles()
        print(f"\n📚 Perfiles disponibles ({len(profiles)}):")
        for profile in profiles:
            status = "✓ ACTIVO" if profile["is_active"] else "○ INACTIVO"
            print(f"  • {profile['name']} ({profile['mode']}) - {status}")
            print(f"    {profile['description']}")
        
        # Activar perfil equilibrado
        if profile_manager.activate_profile("Equilibrado"):
            print("\n✅ Perfil 'Equilibrado' activado")
            
            # Obtener perfil activo
            active_profile = profile_manager.get_active_profile()
            if active_profile:
                print(f"\n🔧 Configuración del perfil activo '{active_profile.name}':")
                for key, value in active_profile.settings.items():
                    print(f"  {key}: {value}")
                
                # Obtener configuraciones específicas
                scan_intensity = profile_manager.get_profile_setting("scan_intensity", "normal")
                max_parallel = profile_manager.get_profile_setting("max_parallel_scans", 1)
                tool_timeout = profile_manager.get_profile_setting("tool_timeout", 300)
                
                print(f"\n🎯 Valores clave del perfil:")
                print(f"  • Intensidad de escaneo: {scan_intensity}")
                print(f"  • Escaneos paralelos máximos: {max_parallel}")
                print(f"  • Timeout de herramientas: {tool_timeout} segundos")
        
        # Crear perfil personalizado
        try:
            custom_profile = profile_manager.create_profile(
                "Personalizado", 
                BehaviorMode.CUSTOM, 
                "Perfil con configuración personalizada para pruebas"
            )
            
            # Modificar algunas configuraciones
            custom_profile.update_setting("scan_intensity", "high")
            custom_profile.update_setting("max_parallel_scans", 5)
            custom_profile.update_setting("alert_sensitivity", "high")
            
            print(f"\n🆕 Perfil personalizado creado: {custom_profile.name}")
            print(f"  Descripción: {custom_profile.description}")
            print(f"  Modo: {custom_profile.mode.value}")
            
            # Activar perfil personalizado
            if profile_manager.activate_profile("Personalizado"):
                print(f"✅ Perfil '{custom_profile.name}' activado")
                
                # Verificar configuración
                intensity = profile_manager.get_profile_setting("scan_intensity")
                parallel = profile_manager.get_profile_setting("max_parallel_scans")
                sensitivity = profile_manager.get_profile_setting("alert_sensitivity")
                
                print(f"  Configuración activa:")
                print(f"    Intensidad: {intensity}")
                print(f"    Paralelismo: {parallel}")
                print(f"    Sensibilidad: {sensitivity}")
            
        except ValueError as e:
            print(f"\n⚠️ Nota: {e}")
        
        # Listar perfiles actualizados
        profiles = profile_manager.list_profiles()
        print(f"\n📋 Estado final de perfiles:")
        for profile in profiles:
            status = "✓ ACTIVO" if profile["is_active"] else "○ INACTIVO"
            print(f"  • {profile['name']} - {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 Probando sistema de perfiles de comportamiento...")
    success = test_behavior_profiles()
    if success:
        print("\n🎉 Prueba completada correctamente")
        sys.exit(0)
    else:
        print("\n💥 La prueba falló")
        sys.exit(1)
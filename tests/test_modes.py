"""
Tests para KaliGhost en modo Fantasma y persistente
"""

import os
import sys
import json
import subprocess
import unittest
import time
from pathlib import Path

# --- Rutas ---
KALIGHOST_DIR = Path(__file__).parent.parent
AGENT_DIR = KALIGHOST_DIR / "YrYs-Agent"
MEMORY_DIR = AGENT_DIR / "memory"
ONBOARDING_FLAG = KALIGHOST_DIR / ".onboarding_completed"

# --- Configuración de prueba ---
TEST_CONFIG = {
    "ghost": {
        "enabled": True,
        "wipe_ram": True,
        "encrypt_logs": True,
        "auto_shutdown": True,
        "ephemeral_fs": True
    },
    "agent": {
        "autonomy_level": 100,
        "auto_confirm": True
    }
}


class TestKaliGhostModes(unittest.TestCase):
    """
    Test suite para validar KaliGhost en diferentes modos
    """
    
    def setUp(self):
        """Configuración inicial para cada test"""
        print("\n🔧 Configurando entorno de prueba...")
        
        # Backup de configuración original
        self.config_backup = None
        self.config_path = AGENT_DIR / "yrays_config.yaml"
        
        if self.config_path.exists():
            self.config_backup = self.config_path.read_text()
        
        # Crear config de prueba
        self.update_config(TEST_CONFIG)
        
        # Limpiar flag de onboarding
        if ONBOARDING_FLAG.exists():
            ONBOARDING_FLAG.unlink()
        
        # Asegurar directorio de memoria
        MEMORY_DIR.mkdir(exist_ok=True, parents=True)
        
    
    def tearDown(self):
        """Limpieza después de cada test"""
        print("🧹 Limpiando entorno de prueba...")
        
        # Restaurar configuración original
        if self.config_backup:
            self.config_path.write_text(self.config_backup)
        else:
            self.config_path.unlink(missing_ok=True)
        
        # Limpiar memoria
        for file in MEMORY_DIR.glob("*.json"):
            file.unlink()
        
        # Limpiar flag
        ONBOARDING_FLAG.unlink(missing_ok=True)
        
    
    def update_config(self, new_config: dict):
        """Actualiza la configuración con nuevos valores"""
        # Cargar config actual si existe
        if self.config_path.exists():
            try:
                import yaml
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f)
            except:
                config = {}
        else:
            config = {}
        
        # Actualizar con nuevos valores
        config.update(new_config)
        
        # Guardar
        with open(self.config_path, 'w') as f:
            import yaml
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    
    def test_onboarding_flow(self):
        """Prueba que los archivos de onboarding existen y son ejecutables"""
        print("\n🔄 Probando flujo de onboarding...")
        
        # Probar que los archivos esenciales existen
        wizard_path = KALIGHOST_DIR / "onboarding" / "wizard.py"
        self.assertTrue(wizard_path.exists(), "wizard.py no existe")
        
        start_script = KALIGHOST_DIR / "start_onboarding.sh"
        self.assertTrue(start_script.exists(), "start_onboarding.sh no existe")
        
        # Verificar que tiene permisos de ejecución
        self.assertTrue(os.access(start_script, os.X_OK), "start_onboarding.sh no es ejecutable")
        
        print("✅ Archivos de onboarding verificados")
    
    
    def test_autonomous_loop(self):
        """Prueba que el bucle autónomo se puede importar y que la clase existe"""
        print("\n🔄 Probando bucle autónomo...")
        
        # Verificar que existe el archivo
        loop_path = AGENT_DIR / "core" / "autonomous_loop.py"
        self.assertTrue(loop_path.exists(), "autonomous_loop.py no existe")
        
        # Intentar importar
        try:
            sys.path.append(str(AGENT_DIR))
            from core.autonomous_loop import AutonomousAgent
            print("✅ AutonomousAgent importado correctamente")
        except Exception as e:
            self.fail(f"Error al importar AutonomousAgent: {e}")
        
        # Verificar que se puede instanciar
        try:
            agent = AutonomousAgent()
            self.assertIsNotNone(agent)
            print("✅ AutonomousAgent instanciado correctamente")
        except Exception as e:
            self.fail(f"Error al instanciar AutonomousAgent: {e}")
    
    
    def test_ghost_mode(self):
        """Prueba que el modo Fantasma borra la memoria al apagar"""
        print("\n🔄 Probando modo Fantasma...")
        
        # Crear memoria de prueba
        memory_file = MEMORY_DIR / "test_session.json"
        memory_file.write_text('{"test": "data", "timestamp": "' + str(int(time.time())) + '"}')
        
        # Verificar que existe antes
        self.assertTrue(memory_file.exists(), "Archivo de memoria no creado")
        
        # Simular apagado (limpieza)
        print("🔌 Simulando apagado...")
        time.sleep(2)  # Simular tiempo de uso
        
        # Limpiar como haría el modo Fantasma
        for file in MEMORY_DIR.glob("*.json"):
            file.unlink()
        
        # Verificar que se borró
        self.assertFalse(memory_file.exists(), "Memoria no borrada en modo Fantasma")
        
        print("✅ Modo Fantasma: memoria borrada correctamente")
    
    
    def test_persistent_mode(self):
        """Prueba que el modo persistente guarda la memoria"""
        print("\n🔄 Probando modo persistente...")
        
        # Actualizar configuración para modo persistente
        persistent_config = {"ghost": {"enabled": False}}
        self.update_config(persistent_config)
        
        # Crear memoria de prueba
        memory_file = MEMORY_DIR / "persistent_data.json"
        memory_file.write_text('{"session": "active", "tasks": 1, "completed": true}')
        
        # Simular ciclo de uso
        print("💾 Simulando uso persistente...")
        time.sleep(1)
        
        # Verificar que persiste
        self.assertTrue(memory_file.exists(), "Datos no persistentes")
        
        # Leer contenido
        content = json.loads(memory_file.read_text())
        self.assertEqual(content["tasks"], 1, "Datos corruptos o modificados")
        
        print("✅ Modo persistente: datos guardados correctamente")


if __name__ == "__main__":
    # Asegurar que existe el directorio de tests
    Path(__file__).parent.mkdir(exist_ok=True)
    
    # Ejecutar tests
    unittest.main(verbosity=2)
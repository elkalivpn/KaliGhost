"""
Onboarding Wizard — KaliGhost
Primer contacto del usuario con YrYs-Agent
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import subprocess

# --- Rutas ---
KALIGHOST_DIR = Path(__file__).parent.parent
AGENT_DIR = KALIGHOST_DIR / "YrYs-Agent"
CONFIG_PATH = AGENT_DIR / "yrays_config.yaml"
ONBOARDING_DONE_FLAG = KALIGHOST_DIR / ".onboarding_completed"

# --- Estilos CLI ---
class Style:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def colored(text, color):
        return f"{color}{text}{Style.ENDC}"

# --- Menú de Onboarding ---
class OnboardingWizard:
    def __init__(self):
        self.user_data = {}
        self.config = {}

    def print_header(self):
        print(Style.colored("\n🚀 BIENVENIDO A KALIGHOST\n", Style.CYAN))
        print(Style.colored("========================\n", Style.CYAN))
        print("Este asistente configurará YrYs-Agent para ti.\n")

    def step_welcome(self):
        self.print_header()
        print("KaliGhost es un sistema de pentesting autónomo con IA integrada.\n")
        print("YrYs-Agent puede ejecutar herramientas de seguridad y tomar decisiones por ti.\n")
        input("Presiona Enter para continuar...\n")

    def step_mode_selection(self):
        print(Style.colored("\n📌 ¿Qué modo deseas usar?\n", Style.HEADER))
        print("1) [GHOST]  Ephemeral - Cero rastro (como Tails OS)")
        print("2) [DISK]   Persistente - Guarda configuraciones y datos")
        
        while True:
            choice = input("\nSelecciona (1/2): ")
            if choice == '1':
                self.user_data['mode'] = 'ghost'
                print("Modo elegido: \033[91mGHOST MODE\033[0m (cero rastro)\n")
                break
            elif choice == '2':
                self.user_data['mode'] = 'disk'
                print("Modo elegido: \033[92mDISK MODE\033[0m (persistencia)\n")
                break
            else:
                print("Opción no válida.\n")

    def step_autonomy_level(self):
        print(Style.colored("\n🧠 ¿Qué nivel de autonomía deseas?\n", Style.HEADER))
        print("1) [SEMIAUTO]  Solo ejecuta cuando yo lo diga")
        print("2) [AUTO]      Toma decisiones por sí mismo (recomendado)")
        
        while True:
            choice = input("\nSelecciona (1/2): ")
            if choice == '1':
                self.user_data['autonomy'] = 'semiauto'
                print("Autonomía: \033[93mSEMIAUTO\033[0m (requiere confirmación)\n")
                break
            elif choice == '2':
                self.user_data['autonomy'] = 'auto'
                print("Autonomía: \033[92mAUTO\033[0m (100% autónomo)\n")
                break
            else:
                print("Opción no válida.\n")

    def step_create_proton_account(self):
        print(Style.colored("\n🔐 ¿Quieres crear una cuenta en Proton Mail? (recomendado)\n", Style.HEADER))
        print("Proton Pass guardará de forma segura tus credenciales y las del agente.")
        print("Proton Drive será el respaldo encriptado de la memoria del agente.\n")
        
        while True:
            choice = input("¿Crear cuenta gratuita en Proton? (s/n): ").lower()
            if choice in ['s', 'y', 'si', 'yes']:
                self.user_data['create_proton'] = True
                print("\033[92mSí\033[0m, crearemos una cuenta Proton para ti.\n")
                break
            elif choice in ['n', 'no']:
                self.user_data['create_proton'] = False
                print("\033[91mNo\033[0m, puedes configurarlo después.\n")
                break
            else:
                print("Por favor, responde 's' o 'n'.\n")

    def step_setup_proton_credentials(self):
        if not self.user_data.get('create_proton'):
            return
        
        print(Style.colored("\n📧 CREANDO CUENTA EN PROTON MAIL...\n", Style.YELLOW))
        print("Abriendo navegador para registro...\n")
        
        # Abrir URL de registro
        register_url = "https://account.proton.me/mail/signup?plan=free"
        try:
            subprocess.run(['open', register_url], check=True)
        except:
            try:
                subprocess.run(['xdg-open', register_url], check=True)
            except:
                print(f"Abre manualmente: {register_url}\n")
        
        print("Sigue los pasos para crear una cuenta gratuita en Proton.\n")
        input("Presiona Enter cuando hayas terminado...\n")
        
        # Pedir credenciales
        email = input("📧 Email de tu cuenta Proton: ")
        password = input("🔑 Contraseña de Proton: ")
        
        # Guardar en entorno del agente
        env_path = AGENT_DIR / ".env"
        with open(env_path, 'w') as f:
            f.write(f"PROTON_AGENT_EMAIL={email}\n")
            f.write(f"PROTON_PASSWORD={password}\n")
            f.write(f"PROTON_VAULT_NAME=KaliGhost-Agent\n")
        
        print(f"\033[92m✅ Credenciales guardadas en {env_path}\n\033[0m")

    def step_configure_agent(self):
        print(Style.colored("\n⚙️ CONFIGURANDO YrYs-Agent...\n", Style.HEADER))
        
        # Cargar configuración base
        with open(CONFIG_PATH, 'r') as f:
            lines = f.readlines()
        
        config_text = ''.join(lines)
        
        # Aplicar cambios según selecciones
        autonomy_level = 100 if self.user_data['autonomy'] == 'auto' else 50
        auto_confirm = 'true' if self.user_data['autonomy'] == 'auto' else 'false'
        ghost_enabled = 'true' if self.user_data['mode'] == 'ghost' else 'false'
        
        # Reemplazos exactos con líneas completas
        config_text = config_text.replace("    autonomy_level: 100", f"    autonomy_level: {autonomy_level}")
        config_text = config_text.replace("    auto_confirm: true", f"    auto_confirm: {auto_confirm}")
        config_text = config_text.replace("    enabled: true", f"    enabled: {ghost_enabled}", 1)  # Solo el primero
        
        # Guardar configuración final
        with open(CONFIG_PATH, 'w') as f:
            f.write(config_text)
        
        print("\033[92m✅ Configuración del agente actualizada\n\033[0m")

    def step_final_message(self):
        print(Style.colored("\n🎉 CONFIGURACIÓN COMPLETA\n", Style.GREEN))
        print("YrYs-Agent está listo para usar.\n")
        
        if self.user_data['autonomy'] == 'auto':
            print("💡 En modo AUTO, el agente puede tomar decisiones por sí mismo.")
            print("Pídele algo como: \033[1mEscanea la red local y encuentra vulnerabilidades.\033[0m\n")
        else:
            print("💡 En modo SEMIAUTO, el agente te pedirá confirmación antes de actuar.\n")
        
        print("Para iniciar el agente:\n")
        print("  cd KaliGhost && python3 YrYs-Agent/main.py\n")
        
        # Crear flag de onboarding completado
        ONBOARDING_DONE_FLAG.touch()
        
        print("\033[94m¡Gracias por usar KaliGhost! El futuro del pentesting autónomo.\033[0m\n")

    def run(self):
        try:
            self.step_welcome()
            self.step_mode_selection()
            self.step_autonomy_level()
            self.step_create_proton_account()
            self.step_setup_proton_credentials()
            self.step_configure_agent()
            self.step_final_message()
        except KeyboardInterrupt:
            print("\n\n\033[91mConfiguración cancelada por el usuario.\033[0m")
            sys.exit(1)

if __name__ == '__main__':
    wizard = OnboardingWizard()
    wizard.run()
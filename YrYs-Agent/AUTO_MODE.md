#!/usr/bin/env python3
# AWS AUTO-BOOTSTRAP - CREA INFRA COMPLETA AUTO

import os
import sys
import json
import subprocess
import time
from pathlib import Path

class AwsAutonomousEngine:
    def __init__(self, pem_key_path, role_arn):
        self.pem_path = pem_key_path
        self.role_arn = role_arn
        self.session_info = None
        self.ec2_instance_id = None
        self.s3_bucket = None
        
        # Secure PEM permissions
        os.chmod(pem_key_path, 0o600)
        
    def assume_role(self):
        """Assume AWS role and get temporary credentials"""
        print("🔄 Assumiendo AWS Role...")
        cmd = f"aws sts assume-role --role-arn {self.role_arn} --role-session-name YrYsAutoMode"
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                creds = json.loads(result.stdout)['Credentials']
                os.environ['AWS_ACCESS_KEY_ID'] = creds['AccessKeyId']
                os.environ['AWS_SECRET_ACCESS_KEY'] = creds['SecretAccessKey']
                os.environ['AWS_SESSION_TOKEN'] = creds['SessionToken']
                self.session_info = creds
                print("✅ AWS Role assumido correctamente")
                return True
            else:
                print(f"❌ Error assumiendo role: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def create_ec2_scanner_instance(self):
        """Crea instancia EC2 para scanning autónomo"""
        print("🔄 Creando instancia EC2 Kali Linux...")
        
        # User data script para auto-instalar herramientas
        user_data = """#!/bin/bash
# Update and install Kali tools
apt-get update -y
apt-get install -y kali-linux-headless nmap metasploit-framework sqlmap hydra john \
                    nikto wpscan dirb gobuster nuclei zaproxy burpsuite wireshark tshark \
                    awscli python3-pip docker.io
                    
# Install Python tools
pip3 install boto3 paramiko scrapy requests beautifulsoup4

# Create YrYs agent directory
mkdir -p /opt/yr_ys
cd /opt/yr_ys

# Clone agent repo
git clone https://github.com/kalighost/yr_ys_agent.git . || echo "Repo not cloned"

# Create auto-start service
cat > /etc/systemd/system/yr_ys.service << EOF
[Unit]
Description=YrYs Autonomous Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/yr_ys
ExecStart=/usr/bin/python3 /opt/yr_ys/agent.py --mode auto
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl enable yr_ys.service
systemctl start yr_ys.service

echo "✅ YrYs Agent instalado y ejecutándose"
"""
        
        # Base64 encode user data
        import base64
        user_data_b64 = base64.b64encode(user_data.encode()).decode()
        
        # Comando para crear instancia
        cmd = f"""aws ec2 run-instances \
            --image-id ami-0c7c4e3a6c7b8a2a8 \
            --instance-type t3.medium \
            --key-name kalighost \
            --security-group-ids sg-0123456789abcdef \
            --subnet-id subnet-0123456789abcdef \
            --user-data '{user_data_b64}' \
            --tag-specifications 'ResourceType=instance,Tags=[{{Key=Name,Value=yr_ys_scanner}}]' \
            --count 1"""
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                instance_data = json.loads(result.stdout)
                self.ec2_instance_id = instance_data['Instances'][0]['InstanceId']
                print(f"✅ Instancia EC2 creada: {self.ec2_instance_id}")
                return self.ec2_instance_id
            else:
                print(f"❌ Error creando instancia: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Exception: {e}")
            return None
    
    def configure_ssh_access(self, public_ip):
        """Configura acceso SSH con la key PEM"""
        print(f"🔄 Configurando SSH a {public_ip}...")
        
        # Crear configuración SSH en ~/.ssh/config
        ssh_config = f"""
Host yr_ys_scanner
    HostName {public_ip}
    User ubuntu
    IdentityFile {self.pem_path}
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
"""
        
        ssh_config_path = Path.home() / ".ssh" / "config"
        with open(ssh_config_path, 'a') as f:
            f.write(ssh_config)
        
        # Probar conexión
        test_cmd = f"ssh -i {self.pem_path} -o ConnectTimeout=10 ubuntu@{public_ip} 'echo ✅ SSH OK'"
        result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ SSH configurado correctamente a {public_ip}")
            return True
        else:
            print(f"❌ SSH test falló: {result.stderr}")
            return False
    
    def deploy_agent_to_ec2(self, public_ip):
        """Despliega YrYs Agent a la instancia EC2"""
        print(f"🔄 Desplegando YrYs Agent a {public_ip}...")
        
        # Copiar archivos del agente
        agent_files = [
            "yrays_config.yaml",
            "CORE_PRINCIPLES.md",
            "AUTO_MODE.md",
            "agent.py"
        ]
        
        for file in agent_files:
            local_path = Path(f"/Users/mrhardcore/KaliGhost/YrYs-Agent/{file}")
            if local_path.exists():
                cmd = f"scp -i {self.pem_path} -o ConnectTimeout=30 {local_path} ubuntu@{public_ip}:/opt/yr_ys/"
                subprocess.run(cmd, shell=True)
                print(f"  📦 {file} copiado")
        
        # Instalar dependencias remotas
        install_cmd = f"""ssh -i {self.pem_path} ubuntu@{public_ip} '
cd /opt/yr_ys &&
sudo apt-get update -y &&
sudo apt-get install -y python3-pip &&
pip3 install -r requirements.txt 2>/dev/null || pip3 install boto3 paramiko requests &&
sudo chmod +x *.py
'"""
        
        subprocess.run(install_cmd, shell=True)
        print("✅ Agent desplegado e instalado")
    
    def create_s3_for_results(self):
        """Crea bucket S3 para almacenar resultados"""
        import uuid
        bucket_name = f"yr-ys-results-{uuid.uuid4().hex[:8]}"
        
        print(f"🔄 Creando bucket S3: {bucket_name}")
        
        cmd = f"aws s3api create-bucket --bucket {bucket_name} --region us-east-1"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            self.s3_bucket = bucket_name
            print(f"✅ Bucket S3 creado: {bucket_name}")
            
            # Subir archivo de configuración
            config_cmd = f"aws s3 cp /Users/mrhardcore/KaliGhost/YrYs-Agent/yrays_config.yaml s3://{bucket_name}/config/"
            subprocess.run(config_cmd, shell=True, capture_output=True)
            
            return bucket_name
        else:
            print(f"❌ Error creando bucket: {result.stderr}")
            return None
    
    def launch_full_stack(self):
        """Lanza stack completo AWS para operaciones autónomas"""
        print("🚀 LANZANDO STACK AWS COMPLETO...")
        
        # 1. Assume role
        if not self.assume_role():
            return False
        
        # 2. Create S3 bucket
        s3_bucket = self.create_s3_for_results()
        if not s3_bucket:
            print("⚠️ Continuando sin S3 bucket...")
        
        # 3. Create EC2 instance
        instance_id = self.create_ec2_scanner_instance()
        if not instance_id:
            print("❌ No se pudo crear instancia EC2")
            return False
        
        # 4. Wait for instance to be running and get public IP
        print("⏳ Esperando que instancia esté running...")
        time.sleep(60)  # Wait for instance
        
        # Get public IP
        ip_cmd = f"aws ec2 describe-instances --instance-ids {instance_id} --query 'Reservations[0].Instances[0].PublicIpAddress' --output text"
        result = subprocess.run(ip_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            public_ip = result.stdout.strip()
            print(f"✅ Instancia IP pública: {public_ip}")
            
            # 5. Configure SSH
            if self.configure_ssh_access(public_ip):
                # 6. Deploy agent
                self.deploy_agent_to_ec2(public_ip)
                
                # 7. Start autonomous mode
                start_cmd = f"""ssh -i {self.pem_path} ubuntu@{public_ip} '
cd /opt/yr_ys &&
nohup python3 agent.py --mode auto --s3-bucket {s3_bucket} > agent.log 2>&1 &
echo $! > agent.pid
echo "🌀 YrYs Agent ejecutándose en modo auto"
'"""
                subprocess.run(start_cmd, shell=True)
                
                print("=" * 60)
                print("🎉 STACK COMPLETO DESPLEGADO")
                print(f"📡 EC2 Instance: {instance_id}")
                print(f"🌐 Public IP: {public_ip}")
                print(f"📦 S3 Bucket: {s3_bucket}")
                print(f"🔑 SSH: ssh yr_ys_scanner")
                print("=" * 60)
                
                return {
                    'instance_id': instance_id,
                    'public_ip': public_ip,
                    's3_bucket': s3_bucket,
                    'ssh_alias': 'yr_ys_scanner'
                }
        
        print("❌ No se pudo obtener IP pública")
        return False

if __name__ == "__main__":
    # Configuración automática
    pem_path = "/Users/mrhardcore/Downloads/kalighost.pem"
    role_arn = "arn:aws:iam::233896339713:role/service-role/DevOpsAgentRole-WebappAdmin-vt2y0ajh"
    
    engine = AwsAutonomousEngine(pem_path, role_arn)
    stack_info = engine.launch_full_stack()
    
    if stack_info:
        print("\n✅ YRYS AGENT READY FOR AUTO MODE")
        print(f"El agente está ejecutándose en {stack_info['public_ip']}")
        print("Puedes monitorear con: ssh yr_ys_scanner 'tail -f /opt/yr_ys/agent.log'")
    else:
        print("\n❌ FALLÓ EL AUTO-DEPLOY")
        print("Revisa credenciales y permisos")
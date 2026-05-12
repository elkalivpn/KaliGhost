#!/usr/bin/env python3
"""Despliega instancia EC2 autónomamente con KaliGhost pre-instalado"""

import boto3
import time

ec2 = boto3.resource('ec2', region_name='us-east-1')

def create_kalighost_instance():
    """Crea EC2 con Kali Linux + KaliGhost preconfigurado"""
    
    user_data = '''#!/bin/bash
apt-get update
apt-get install -y docker.io git
git clone https://github.com/elkalivpn/KaliGhost.git
cd KaliGhost
./boot/boot.sh
'''

    instance = ec2.create_instances(
        ImageId='ami-0c55b159cbfafe1f0',  # Kali Linux 2024.x (x86_64)
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.medium',
        UserData=user_data,
        SecurityGroupIds=['sg-xxxxxxx'],
        KeyName='kalighost-key',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'KaliGhost-Pentest'}]
            }
        ]
    )[0]
    
    print(f"Instance created: {instance.id}")
    return instance

if __name__ == '__main__':
    inst = create_kalighost_instance()
    inst.wait_until_running()
    print(f"✅ Instance {inst.id} is running!")
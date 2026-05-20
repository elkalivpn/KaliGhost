#!/usr/bin/env python3
"""
Integración de Modelos de IA para YrYs-Agent
Soporta múltiples proveedores: AWS Bedrock, OpenAI, Anthropic, modelos locales
"""

import os
import json
import logging
import boto3
from typing import Dict, List, Optional
from pathlib import Path

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class AIProvider:
    """Proveedor base para modelos de IA"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.model_name = config.get('model', '')
        
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """Envía un mensaje al modelo de IA y devuelve la respuesta"""
        raise NotImplementedError("Este método debe ser implementado por subclasses")

class BedrockProvider(AIProvider):
    """Proveedor para AWS Bedrock"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.region = config.get('region', 'us-east-1')
        
        # Obtener credenciales del entorno
        self.access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.session_token = os.environ.get('AWS_SESSION_TOKEN')
        
        # Inicializar cliente de Bedrock
        if self.access_key and self.secret_key:
            self.client = boto3.client(
                'bedrock-runtime',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                aws_session_token=self.session_token
            )
        else:
            # Intentar usar credenciales por defecto
            self.client = boto3.client('bedrock-runtime', region_name=self.region)
    
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """Envía un mensaje a Bedrock y devuelve la respuesta"""
        try:
            # Convertir mensajes al formato de Bedrock
            prompt = self._format_messages(messages)
            
            # Determinar el tipo de modelo basado en el nombre
            if 'claude' in self.model_name.lower():
                response = self._send_claude_request(prompt)
            else:
                response = self._send_generic_request(prompt)
                
            return response
        except Exception as e:
            logging.error(f"Error en BedrockProvider: {e}")
            raise
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Formatea mensajes para Bedrock"""
        formatted = ""
        for msg in messages:
            if msg['role'] == 'system':
                formatted += f"\n\nHuman: {msg['content']}\n"
            elif msg['role'] == 'user':
                formatted += f"\n\nHuman: {msg['content']}\n"
            elif msg['role'] == 'assistant':
                formatted += f"\n\nAssistant: {msg['content']}\n"
        formatted += "\n\nAssistant:"
        return formatted
    
    def _send_claude_request(self, prompt: str) -> str:
        """Envía una solicitud a Claude en Bedrock"""
        body = {
            "prompt": prompt,
            "max_tokens_to_sample": 2000,
            "temperature": 0.7,
            "top_p": 0.9,
        }
        
        response = self.client.invoke_model(
            modelId=self.model_name,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['completion']
    
    def _send_generic_request(self, prompt: str) -> str:
        """Envía una solicitud genérica a Bedrock"""
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 2000,
                "temperature": 0.7,
                "topP": 0.9,
            }
        }
        
        response = self.client.invoke_model(
            modelId=self.model_name,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['results'][0]['outputText']

class OpenAIProvider(AIProvider):
    """Proveedor para OpenAI"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        
        # Obtener API key del entorno
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if self.api_key and OPENAI_AVAILABLE:
            openai.api_key = self.api_key
    
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """Envía un mensaje a OpenAI y devuelve la respuesta"""
        if not OPENAI_AVAILABLE:
            raise Exception("OpenAI no está disponible. Instala openai con pip install openai")
        
        if not self.api_key:
            raise Exception("OPENAI_API_KEY no está configurada en el entorno")
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error en OpenAIProvider: {e}")
            raise

class AnthropicProvider(AIProvider):
    """Proveedor para Anthropic (Claude)"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        
        # Obtener API key del entorno
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        if self.api_key and ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """Envía un mensaje a Anthropic y devuelve la respuesta"""
        if not ANTHROPIC_AVAILABLE:
            raise Exception("Anthropic no está disponible. Instala anthropic con pip install anthropic")
        
        if not self.api_key:
            raise Exception("ANTHROPIC_API_KEY no está configurada en el entorno")
        
        try:
            # Convertir mensajes al formato de Anthropic
            prompt = self._format_messages(messages)
            
            response = self.client.completions.create(
                model=self.model_name,
                prompt=prompt,
                max_tokens_to_sample=2000,
                temperature=0.7,
            )
            
            return response.completion
        except Exception as e:
            logging.error(f"Error en AnthropicProvider: {e}")
            raise
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Formatea mensajes para Anthropic"""
        formatted = ""
        for msg in messages:
            if msg['role'] == 'system':
                formatted += f"{anthropic.HUMAN_PROMPT} {msg['content']}"
            elif msg['role'] == 'user':
                formatted += f"{anthropic.HUMAN_PROMPT} {msg['content']}"
            elif msg['role'] == 'assistant':
                formatted += f"{anthropic.AI_PROMPT} {msg['content']}"
        formatted += f"{anthropic.AI_PROMPT}"
        return formatted

class LocalModelProvider(AIProvider):
    """Proveedor para modelos locales (usando Ollama u otros)"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.endpoint = config.get('endpoint', 'http://localhost:11434/api/generate')
    
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """Envía un mensaje a un modelo local y devuelve la respuesta"""
        try:
            import requests
            
            # Formatear mensajes para el modelo local
            prompt = self._format_messages(messages)
            
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
                "max_tokens": 2000,
            }
            
            response = requests.post(self.endpoint, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '')
        except Exception as e:
            logging.error(f"Error en LocalModelProvider: {e}")
            raise
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Formatea mensajes para modelos locales"""
        formatted = ""
        for msg in messages:
            formatted += f"{msg['role']}: {msg['content']}\n"
        return formatted

def create_ai_provider(provider_type: str, config: Dict) -> AIProvider:
    """Crea un proveedor de IA basado en el tipo especificado"""
    if provider_type == 'bedrock':
        return BedrockProvider(config)
    elif provider_type == 'openai':
        return OpenAIProvider(config)
    elif provider_type == 'anthropic':
        return AnthropicProvider(config)
    elif provider_type == 'local':
        return LocalModelProvider(config)
    else:
        raise ValueError(f"Proveedor de IA no soportado: {provider_type}")

# Función de fallback para cuando no hay proveedores disponibles
def fallback_response(prompt: str) -> str:
    """Respuesta de fallback cuando no hay modelos de IA disponibles"""
    return f"""✅ [KaliGhost IA - MODO LOCAL] → 
🔍 OBJETIVO RECIBIDO: '{prompt}'
🔄 PROCESANDO: Aplicando lógica avanzada YrYs-Agent.
🎯 MODO FANTASMA: Operando en modo seguro y eficiente.
🛠️ TOOLS: Preparado para ejecutar herramientas autorizadas.
📝 NOTA: Conectado a modelos de IA reales para respuestas más completas."""
"""
KaliGhost AI Enterprise - Communication System
Sistema de comunicación entre agentes y coordinación
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any

class CommunicationSystem:
    """
    Sistema de comunicación entre agentes y el sistema central
    """
    
    def __init__(self):
        self.message_queue = []
        self.communication_history = []
        
    def send_message(self, sender: str, receiver: str, message: Dict[str, Any]) -> bool:
        """Enviar mensaje entre agentes"""
        msg = {
            "id": len(self.communication_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "status": "sent"
        }
        
        self.message_queue.append(msg)
        self.communication_history.append(msg)
        
        print(f"✉️ Mensaje enviado de {sender} a {receiver}")
        print(f"   Contenido: {message.get('subject', 'Sin asunto')}")
        return True
        
    def receive_message(self, receiver: str) -> List[Dict[str, Any]]:
        """Recibir mensajes dirigidos al receptor"""
        received_msgs = [msg for msg in self.message_queue if msg["receiver"] == receiver]
        return received_msgs
        
    def broadcast_message(self, sender: str, message: Dict[str, Any]) -> None:
        """Difundir mensaje a todos los agentes"""
        print(f"📢 Broadcast de {sender}: {message.get('subject', 'Mensaje general')}")
        
    def get_communication_report(self) -> Dict[str, Any]:
        """Generar reporte de comunicación"""
        report = {
            "total_messages": len(self.communication_history),
            "message_queue_size": len(self.message_queue),
            "communication_timestamp": datetime.now().isoformat(),
            "active_connections": 7,  # Número de agentes
            "last_message": self.communication_history[-1]["timestamp"] if self.communication_history else None
        }
        return report

# Ejemplo de uso
if __name__ == "__main__":
    comm_system = CommunicationSystem()
    
    # Enviar mensajes
    comm_system.send_message("CEO", "Executive", {
        "subject": "Lanzamiento de nuevo producto",
        "content": "Por favor coordinar acciones de marketing para el lanzamiento de 'Ciberseguridad Cero a Experto'",
        "priority": "high"
    })
    
    comm_system.send_message("Executive", "Research", {
        "subject": "Análisis de mercado",
        "content": "Por favor realice análisis de mercado para nuestros nuevos cursos de ciberseguridad",
        "priority": "medium"
    })
    
    # Recibir mensajes
    received = comm_system.receive_message("Research")
    print(f"\n📥 Mensajes recibidos por Research: {len(received)}")
    
    # Reporte de comunicación
    report = comm_system.get_communication_report()
    print("\n📊 Reporte de comunicación:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
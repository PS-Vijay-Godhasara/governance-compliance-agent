"""Multi-Agent Architecture - Base Agent"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class BaseAgent:
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_queue = asyncio.Queue()
        self.running = False
        self.capabilities = []
        
    async def start(self):
        """Start the agent"""
        self.running = True
        await self._initialize()
        
    async def stop(self):
        """Stop the agent"""
        self.running = False
        
    async def _initialize(self):
        """Initialize agent-specific resources"""
        pass
        
    async def send_message(self, recipient: str, message_type: str, content: Dict[str, Any]):
        """Send message to another agent"""
        message = Message(
            sender=self.agent_id,
            recipient=recipient,
            message_type=message_type,
            content=content
        )
        return message
        
    async def receive_message(self, message: Message) -> Optional[Message]:
        """Receive and process message"""
        await self.message_queue.put(message)
        return await self.process_message(message)
        
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming message - override in subclasses"""
        return None
        
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return self.capabilities
        
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "running": self.running,
            "capabilities": self.capabilities,
            "queue_size": self.message_queue.qsize()
        }
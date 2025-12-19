"""Base agent class for all governance agents"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from ..core.logger import setup_logging
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentMessage:
    """Message format for inter-agent communication"""
    sender: str
    recipient: str
    action: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None


@dataclass
class AgentResponse:
    """Response format from agents"""
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class BaseAgent(ABC):
    """Base class for all governance agents"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        self.message_queue = asyncio.Queue()
        self.running = False
        
    @abstractmethod
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process incoming message"""
        pass
    
    @abstractmethod
    async def initialize(self):
        """Initialize agent resources"""
        pass
    
    async def start(self):
        """Start agent message processing"""
        await self.initialize()
        self.running = True
        logger.info(f"Agent {self.name} started")
        
        while self.running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                response = await self.process_message(message)
                logger.debug(f"Agent {self.name} processed message: {message.action}")
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Agent {self.name} error: {e}")
    
    async def stop(self):
        """Stop agent"""
        self.running = False
        logger.info(f"Agent {self.name} stopped")
    
    async def send_message(self, recipient: str, action: str, payload: Dict[str, Any]) -> AgentResponse:
        """Send message to another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            action=action,
            payload=payload
        )
        # In real implementation, this would use message broker
        return AgentResponse(success=True, data={"message": "sent"})
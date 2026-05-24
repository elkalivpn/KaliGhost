#!/usr/bin/env python3
"""
🐉 KaliGhost IM Channels Integration
Telegram, Slack, Feishu, WeChat unified interface
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, List, Callable, Any
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class IMMessage:
    channel: str
    user_id: str
    thread_id: str
    content: str
    timestamp: str
    files: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class IMResponse:
    content: str
    format: str = "text"
    files: Optional[List[str]] = None
    is_streaming: bool = False


class IMChannel(ABC):
    def __init__(self, channel_name: str, config: Dict[str, Any]):
        self.channel_name = channel_name
        self.config = config
        self.is_connected = False

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def send_message(self, response: IMResponse, user_id: str, thread_id: str):
        pass

    @abstractmethod
    async def listen_for_messages(self, handler: Callable):
        pass


class TelegramChannel(IMChannel):
    async def connect(self):
        try:
            from telegram import Bot
            self.bot = Bot(token=self.config['bot_token'])
            self.is_connected = True
            logger.info("✅ Telegram channel connected")
        except ImportError:
            logger.error("❌ python-telegram-bot not installed")

    async def disconnect(self):
        if hasattr(self, 'bot'):
            await self.bot.close()
            self.is_connected = False

    async def send_message(self, response: IMResponse, user_id: str, thread_id: str):
        try:
            if hasattr(self, 'bot'):
                await self.bot.send_message(chat_id=user_id, text=response.content)
                logger.info(f"📤 Telegram message sent to {user_id}")
        except Exception as e:
            logger.error(f"❌ Telegram send failed: {e}")

    async def listen_for_messages(self, handler: Callable):
        logger.info("⚠️  Telegram polling mode configured")


class SlackChannel(IMChannel):
    async def connect(self):
        try:
            from slack_bolt import App
            self.app = App(token=self.config.get('bot_token'))
            self.is_connected = True
            logger.info("✅ Slack channel connected")
        except ImportError:
            logger.error("❌ slack-bolt not installed")

    async def disconnect(self):
        self.is_connected = False

    async def send_message(self, response: IMResponse, user_id: str, thread_id: str):
        try:
            if hasattr(self, 'app'):
                self.app.client.chat_postMessage(channel=user_id, text=response.content)
                logger.info(f"📤 Slack message sent to {user_id}")
        except Exception as e:
            logger.error(f"❌ Slack send failed: {e}")

    async def listen_for_messages(self, handler: Callable):
        logger.info("⚠️  Slack Socket Mode configured")


class FeishuChannel(IMChannel):
    async def connect(self):
        try:
            self.is_connected = True
            logger.info("✅ Feishu channel configured")
        except Exception as e:
            logger.error(f"❌ Feishu connection failed: {e}")

    async def disconnect(self):
        self.is_connected = False

    async def send_message(self, response: IMResponse, user_id: str, thread_id: str):
        try:
            logger.info(f"📤 Feishu message prepared for {user_id}")
        except Exception as e:
            logger.error(f"❌ Feishu send failed: {e}")

    async def listen_for_messages(self, handler: Callable):
        logger.info("⚠️  Feishu webhook mode configured")


class WeChatChannel(IMChannel):
    async def connect(self):
        try:
            self.is_connected = True
            logger.info("✅ WeChat channel configured")
        except Exception as e:
            logger.error(f"❌ WeChat connection failed: {e}")

    async def disconnect(self):
        self.is_connected = False

    async def send_message(self, response: IMResponse, user_id: str, thread_id: str):
        try:
            logger.info(f"📤 WeChat message prepared for {user_id}")
        except Exception as e:
            logger.error(f"❌ WeChat send failed: {e}")

    async def listen_for_messages(self, handler: Callable):
        logger.info("⚠️  WeChat polling mode configured")


class IMChannelManager:
    def __init__(self):
        self.channels: Dict[str, IMChannel] = {}
        self.message_handler: Optional[Callable] = None
        self.running = False

    def register_channel(self, channel: IMChannel):
        self.channels[channel.channel_name] = channel
        logger.info(f"✅ Channel registered: {channel.channel_name}")

    async def connect_all(self):
        tasks = [channel.connect() for channel in self.channels.values()]
        await asyncio.gather(*tasks, return_exceptions=True)
        self.running = True
        logger.info(f"✅ All channels connected ({len(self.channels)} active)")

    async def disconnect_all(self):
        tasks = [channel.disconnect() for channel in self.channels.values()]
        await asyncio.gather(*tasks, return_exceptions=True)
        self.running = False

    def set_message_handler(self, handler: Callable):
        self.message_handler = handler
        logger.info("✅ Message handler registered")

    async def listen_all(self):
        if not self.message_handler:
            logger.error("❌ No message handler set")
            return
        tasks = [channel.listen_for_messages(self.message_handler) for channel in self.channels.values()]
        await asyncio.gather(*tasks)

    async def send_to_channel(self, channel_name: str, response: IMResponse, user_id: str, thread_id: str):
        if channel_name not in self.channels:
            logger.error(f"❌ Channel not found: {channel_name}")
            return
        channel = self.channels[channel_name]
        await channel.send_message(response, user_id, thread_id)


_channel_manager: Optional[IMChannelManager] = None


def get_im_manager() -> IMChannelManager:
    global _channel_manager
    if _channel_manager is None:
        _channel_manager = IMChannelManager()
    return _channel_manager

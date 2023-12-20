from typing import List
import logging
from fastapi import WebSocket


class ConnectionManager:
    """Class defining socket events"""

    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
        self.logger = logging.getLogger("main")

    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        self.logger.info(f"Attempting to send message: {message}")
        if websocket:
            try:
                await websocket.send_text(message)
                self.logger.info(f"Message sent successfully: {message}")
            except Exception as e:
                self.logger.error(f"Error sending message: {e}")
        else:
            self.logger.error("WebSocket connection not found or closed")

    async def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)


# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     async def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

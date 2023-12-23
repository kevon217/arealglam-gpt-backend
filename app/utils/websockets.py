from typing import List
import logging
from fastapi import WebSocket


class ConnectionManager:
    """Class defining socket events"""

    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections: List[WebSocket] = []
        # Use the centralized logger
        self.logger = logging.getLogger("ARealGlamApp.async_thread")
        self.logger.propagate = (
            False  # Prevent logging messages from propagating to the root logger
        )

    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(f"New WebSocket connection: {websocket.client}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        self.logger.info(f"Attempting to send message: {message}")
        if websocket and websocket in self.active_connections:
            try:
                await websocket.send_text(message)
                self.logger.info(f"Message sent successfully: {message}")
            except Exception as e:
                self.logger.error(f"Error sending message: {e}")
        else:
            self.logger.error("WebSocket connection not found or closed")

    async def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        try:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
                self.logger.info(f"WebSocket disconnected: {websocket.client}")
        except Exception as e:
            self.logger.error(f"Error during WebSocket disconnection: {e}")


# class ConnectionManager:
#     """Class defining socket events"""

#     def __init__(self):
#         """init method, keeping track of connections"""
#         self.active_connections = []
#         self.logger = logging.getLogger("main")

#     async def connect(self, websocket: WebSocket):
#         """connect event"""
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         self.logger.info(f"Attempting to send message: {message}")
#         if websocket:
#             try:
#                 await websocket.send_text(message)
#                 self.logger.info(f"Message sent successfully: {message}")
#             except Exception as e:
#                 self.logger.error(f"Error sending message: {e}")
#         else:
#             self.logger.error("WebSocket connection not found or closed")

#     async def disconnect(self, websocket: WebSocket):
#         """disconnect event"""
#         self.active_connections.remove(websocket)

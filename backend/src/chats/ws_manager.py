import json
import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket connection manager for chat functionality."""

    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, lead_id: int):
        """Connect a WebSocket for a specific lead."""
        await websocket.accept()
        if lead_id not in self.active_connections:
            self.active_connections[lead_id] = []
        self.active_connections[lead_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lead_id: int):
        """Disconnect a WebSocket from a specific lead."""
        if lead_id in self.active_connections and websocket in self.active_connections[lead_id]:
            self.active_connections[lead_id].remove(websocket)
            if not self.active_connections[lead_id]:
                del self.active_connections[lead_id]

    async def send_message(self, message: dict, lead_id: int):
        """Send a message to all connected WebSockets for a lead."""
        if lead_id in self.active_connections:
            connections = self.active_connections[lead_id].copy()
            for connection in connections:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    # Remove disconnected connections
                    logger.warning(f"WS disconnect: {e}")
                    self.disconnect(connection, lead_id)


# Global connection manager instance
manager = ConnectionManager()
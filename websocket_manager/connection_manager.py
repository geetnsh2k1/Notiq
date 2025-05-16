from typing import Dict, List
from fastapi import WebSocket
from collections import defaultdict
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        async with self.lock:
            self.active_connections[user_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, user_id: str):
        async with self.lock:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        async with self.lock:
            for connection in self.active_connections.get(user_id, []):
                await connection.send_text(message)

    async def broadcast(self, message: str):
        async with self.lock:
            for connections in self.active_connections.values():
                for connection in connections:
                    await connection.send_text(message)

# Singleton manager instance
manager = ConnectionManager()

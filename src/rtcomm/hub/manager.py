from fastapi import WebSocket, WebSocketDisconnect, Depends
from rtcomm.hub.group_manager import GroupManager

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self.group_manager = GroupManager()

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        self.group_manager.remove_connection(client_id)

    async def send_personal_message(self, message: str, client_id: str):
        ws = self.active_connections.get(client_id)
        if ws:
            await ws.send_text(message)

    async def broadcast(self, message: str):
        for ws in self.active_connections.values():
            await ws.send_text(message)
    
    async def send_to_group(self, group_name: str, message: str, exclude_id: str = None):
        members = self.group_manager.get_group_members(group_name)
        for client_id in members:
            if client_id != exclude_id:
                await self.send_personal_message(message, client_id)
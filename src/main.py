from fastapi import FastAPI, WebSocket
from rtcomm.hub.base import RTCommHub
from rtcomm.hub.manager import ConnectionManager
from rtcomm.protocol.messages import HubMessage, InvocationMessage

app = FastAPI()
manager = ConnectionManager()

class MyHub(RTCommHub):
    async def on_connect(self, client_id: str):
        print(f"{client_id} connected")

    async def on_disconnect(self, client_id: str):
        print(f"{client_id} disconnected")

    # async def handle_message(self, client_id: str, websocket: WebSocket, message: HubMessage):
    #     print(f"Received from {client_id}: {message.to_dict()}")
    #     if isinstance(message, InvocationMessage):
    #         await websocket.send_text(message.to_json())

    async def handle_message(self, client_id: str, websocket: WebSocket, message: HubMessage):
        print(f"Received from {client_id}: {message.to_dict()}")

        if isinstance(message, InvocationMessage):
            target = message.target
            args = message.arguments

            if target == "broadcast":
                await self.manager.broadcast(message.to_json())

            elif target == "send_personal_message":
                if len(args) >= 2:
                    recipient, content = args[0], args[1]
                    await self.manager.send_personal_message(content, recipient)

            elif target == "create_group" and len(args) >= 1:
                self.manager.group_manager.create_group(args[0])
                await websocket.send_text(f"Group '{args[0]}' created.")

            elif target == "delete_group" and len(args) >= 1:
                self.manager.group_manager.delete_group(args[0])
                await websocket.send_text(f"Group '{args[0]}' deleted.")

            elif target == "join_group" and len(args) >= 1:
                self.manager.group_manager.add_to_group(args[0], client_id)
                await websocket.send_text(f"Joined group '{args[0]}'")

            elif target == "exit_group" and len(args) >= 1:
                self.manager.group_manager.remove_from_group(args[0], client_id)
                await websocket.send_text(f"Left group '{args[0]}'")

            elif target == "send_to_group" and len(args) >= 2:
                await self.manager.send_to_group(args[0], args[1], exclude_id=client_id)
            else:
                # echo or custom client-defined method, echoing back
                await websocket.send_text(message.to_json())

hub = MyHub(manager)

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket, access_token: str = ""):
    await hub(websocket, access_token)
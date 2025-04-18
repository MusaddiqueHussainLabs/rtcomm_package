```markdown
# 📡 RTComm - Real-Time Communication Hub (SignalR Style in Python)

**RTComm** is a scalable, distributed real-time communication hub built with **FastAPI**, **WebSockets**, and **JSON encoding** — inspired by **SignalR**. Designed for production with support for full **Hub Protocol**, client/server reflection, authentication, and bi-directional messaging.

---

## ✨ Features

- ✅ WebSocket Hub with FastAPI
- ✅ JSON Hub Protocol: Invocation, Completion, Stream, Ping, Close, Acks, etc.
- ✅ Client-Side and Server-Side Reflection (`invoke(method_name)`)
- ✅ Authentication with Access Token
- ✅ Modular Python SDK for Clients
- ✅ Built using OOP + SOLID Principles
- ✅ Designed for extensibility and microservice integration

---

## 🏗 Folder Structure


rtcomm_package/
├── src/
│   └── rtcomm/
│       ├── __init__.py
│       ├── protocol/
│       │   └── messages.py
│       ├── hub/
│       │   ├── base.py
│       │   └── manager.py
│       └── client/
│           └── sdk.py
├── README.md
├── pyproject.toml


---

## 🚀 Installation

```bash
pip install rtcomm
```

> Or for local development:

```bash
git clone https://github.com/your-username/rtcomm.git
cd rtcomm
pip install -e .
```

---

## 📡 Usage

### 🖥 1. Server Side

#### Run FastAPI App

```python
# main.py
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

    async def handle_message(self, client_id: str, websocket: WebSocket, message: HubMessage):
        print(f"Received from {client_id}: {message.to_dict()}")
        if isinstance(message, InvocationMessage):
            await websocket.send_text(message.to_json())
```

```bash
uvicorn app.main:app --reload
```

---

### 🤖 2. Client Side

#### Basic Example

```python
# client.py
import asyncio
from rtcomm.client.sdk import RTCommClient
from rtcomm.protocol.messages import InvocationMessage, MessageType

async def main():
    client = RTCommClient(uri="ws://localhost:8000/ws", access_token="token-user123")

    client.on(MessageType.INVOCATION, lambda msg: print("[Client] Got:", msg.arguments))

    await client.connect()

    await client.send(InvocationMessage(invocation_id="1", target="broadcast", arguments=["Hello"]))
    await asyncio.sleep(5)
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔐 Authentication

Add a `?access_token=your-token` query string when connecting via WebSocket. You can override the token verification logic in your `RTCommHub`.

```python
async def authenticate(self, token: str) -> str:
    if token.startswith("token-"):
        return token.split("-")[1]  # return user_id
    raise Exception("Unauthorized")
```

---

## 📜 Supported Message Types (SignalR Protocol)

| Type | Name               | Description                       |
|------|--------------------|-----------------------------------|
| 1    | Invocation         | Call a method                     |
| 2    | Stream Item        | Stream data item                  |
| 3    | Completion         | Result or error return            |
| 4    | Stream Invocation  | Start a stream                    |
| 5    | Cancel Invocation  | Cancel ongoing stream             |
| 6    | Ping               | Keep alive                        |
| 7    | Close              | Graceful close                    |
| 8    | Acknowledgment     | Confirm receipt (optional)        |
| 9    | Sequence Message   | Ordered message (optional)        |

---

## 🧪 Testing

```bash
pytest
```

---

## 🐍 Python Compatibility

- Python 3.8+
- Fully typed (PEP 561)
- Async-first design with `asyncio`

---

## 📦 Build & Publish

```bash
python -m build
twine upload dist/*
```

---

## 📚 License

MIT © [Your Name]

---

## 🤝 Contributing

PRs welcome! Please open issues for bugs, enhancements, or questions.

---

## 🛣 Roadmap

The goal of `rtcomm` is to offer full SignalR-like functionality in Python — scalable, secure, and cross-platform. Here's what's planned:

### ✅ Initial Release
- [x] WebSocket Hub with FastAPI
- [x] JSON-based SignalR Hub Protocol
- [x] Client-to-server & server-to-client method invocation
- [x] Basic authentication via access tokens
- [x] Reflection for dynamic method execution

---

### 🔜 Coming Soon

#### 👥 Group Management
- [ ] `add_to_group(client_id, group_name)`
- [ ] `remove_from_group(client_id, group_name)`
- [ ] `send_to_group(group_name, message)`
- [ ] In-memory and pluggable distributed store (Redis/Mongo/etc.)

#### 🔁 Persistent Connections
- [ ] Reconnection logic with exponential backoff
- [ ] Keep-alive and heartbeat support
- [ ] Resume session after disconnects

#### ⚙️ Scalability
- [ ] Plug-in support for Redis pub/sub or Kafka for multi-instance scaling
- [ ] Shared message bus to coordinate state
- [ ] Distributed group and client state store

#### 🔄 Automatic Reconnects (Client SDK)
- [ ] Reconnect with backoff strategy
- [ ] Resume invocation queue
- [ ] Client state restore

#### 📡 Streaming Support
- [ ] Server-to-client and client-to-server streaming
- [ ] Pause/resume/cancel stream control
- [ ] StreamItemMessage + StreamInvocationMessage handling

#### 🌍 Cross-Platform Support
- [ ] Python client ✅
- [ ] Node.js/TypeScript client (planned)
- [ ] REST fallbacks for non-WebSocket clients

#### 📚 Client Libraries
- [ ] TypeScript client for web browsers
- [ ] Python CLI & SDK
- [ ] CLI: `rtcomm connect ws://... --method=foo --args=bar`

#### 🧩 Hub Filters (Middleware)
- [ ] Support middleware for:
  - Logging
  - Authentication/authorization
  - Error handling
  - Message transformation

---

### 🧠 Have Ideas?
Feel free to [open an issue](https://github.com/MusaddiqueHussainLabs/rtcomm_package/issues) or submit a PR. Collaboration is welcome!

---
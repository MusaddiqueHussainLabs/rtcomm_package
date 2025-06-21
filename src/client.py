import asyncio
from rtcomm.client.sdk import RTCommClient
from rtcomm.protocol.messages import InvocationMessage, MessageType

async def main():
    client = RTCommClient(uri="ws://localhost:8000/ws", access_token="token-user123")

    client.on(MessageType.INVOCATION, lambda msg: print("[Client] Got:", msg.arguments))

    await client.connect()

    await client.send(InvocationMessage(invocation_id="1", target="broadcast", arguments=["Hello"]))
    await asyncio.sleep(5)
    await client.send(InvocationMessage("1", "create_group", ["room1"]))
    await client.send(InvocationMessage("1", "join_group", ["room1"]))
    await client.send(InvocationMessage("1", "send_to_group", ["room1", "Hello everyone!"]))
    await asyncio.sleep(1)
    await client.send(InvocationMessage("1", "exit_group", ["room1"]))
    await client.send(InvocationMessage("1", "delete_group", ["room1"]))
    await asyncio.sleep(2)
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
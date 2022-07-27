import asyncio
import websockets
import json

standard = None
clients = set()


async def handler(websocket):
    global clients
    global standard

    while True:
        try:
            message_json = await websocket.recv()
            message = json.loads(message_json)
            if message["device"] == "standard":
                standard = websocket

            if message["device"] == "client":
                clients.add(websocket)

            if websocket in clients:
                await handle_message_to_standard(message_json)
                print("[CLIENT]", message["cmd"])

            if websocket == standard:
                print("[STANDARD]", message["cmd"])
                await handle_message_to_clients(message["cmd"])

            payload = {"cmd": "ACK"}
            await websocket.send(json.dumps(payload))
        except(websockets.exceptions.ConnectionClosedOK,
               websockets.exceptions.ConnectionClosedError):
            if websocket == standard:
                print("[SERVER] Standard desconectado")
                standard = None
            if websocket in clients:
                print("[SERVER] Client desconectado")
                clients.remove(websocket)


async def handle_message_to_standard(message):
    global standard
    if standard is not None:
        await standard.send(message)
    else:
        websockets.broadcast(clients, "Standard desconectado")


async def handle_message_to_clients(message):
    global clients
    websockets.broadcast(clients, message)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

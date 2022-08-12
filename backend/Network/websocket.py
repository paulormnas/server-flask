import asyncio
import websockets
import json
from threading import Thread


class WebsocketServer(Thread):
    def __init__(self, host="0.0.0.0", port=8000):
        Thread.__init__(self)
        self.standard = None
        self.clients = set()
        self.websocket_host = host
        self.port = port

    async def handler(self, websocket):
        while True:
            try:
                message_json = await websocket.recv()
                message = json.loads(message_json)
                if message["device"] == "standard" and websocket != self.standard:
                    self.standard = websocket
                    print("[WEBSOCKET-SERVER] Standard conectado")

                if message["device"] == "client" and websocket not in self.clients:
                    self.clients.add(websocket)
                    print("[WEBSOCKET-SERVER] Client conectado")

                if websocket in self.clients:
                    await self.handle_message_to_standard(message_json)
                    print("[WEBSOCKET-CLIENT]", message["cmd"])

                if websocket == self.standard:
                    print("[WEBSOCKET-STANDARD]", message["cmd"])
                    await self.handle_message_to_clients(message["cmd"])

                payload = {"cmd": "ACK"}
                await websocket.send(json.dumps(payload))
            except (
                websockets.exceptions.ConnectionClosedOK,
                websockets.exceptions.ConnectionClosedError,
            ):
                if websocket == self.standard:
                    print("[WEBSOCKET-SERVER] Standard desconectado")
                    self.standard = None
                if websocket in self.clients:
                    print("[WEBSOCKET-SERVER] Client desconectado")
                    self.clients.remove(websocket)

    async def handle_message_to_standard(self, message):
        if self.standard is not None:
            await self.standard.send(message)
        else:
            websockets.broadcast(self.clients, "Standard desconectado")

    async def handle_message_to_clients(self, message):
        websockets.broadcast(self.clients, message)

    async def main(self):
        async with websockets.serve(self.handler, self.websocket_host, self.port):
            await asyncio.Future()  # run forever

    def run(self):
        asyncio.run(self.main())


if __name__ == "__main__":
    t = WebsocketServer()
    t.start()

import sys
from backend.Network.websocket import WebsocketServer
from backend.server_app import create_app

ws = WebsocketServer()
ws.start()

_mode = sys.argv[1] if len(sys.argv) > 1 else "development"
app = create_app(mode=_mode)
app.run(**app.config.get_namespace("RUN_"))

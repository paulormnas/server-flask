from flask import (Blueprint, request, render_template)
from flask_cors import cross_origin
from datetime import datetime
from backend.security.Sign import Signature
from os import path

import json

security = Signature()
simon_server_blueprint = Blueprint('simon-server-blueprint', __name__)


@simon_server_blueprint.route('/')
@simon_server_blueprint.route('/home')
@simon_server_blueprint.route('/index')
@cross_origin()
def index():
    return render_template("index.html")


@simon_server_blueprint.route('/registrar_dados', methods=['POST'])
@cross_origin()
def registrar_dados():
    parsed_data = json.loads(request.data)
    file_path = path.abspath(path.dirname(__file__))
    base_path_index = file_path.find('server-flask')
    file_path = file_path[:base_path_index + len('server-flask')]
    file_path = path.join(file_path, 'registros', str(datetime.now().timestamp()))
    with open(file_path, 'a+') as file:
        file.write(json.dumps(parsed_data))

    return 'OK!'

# @simon_server_blueprint.route('/verifica_dispositivo', methods=['GET'])
# @cross_origin()
# def verifica_assinatura():
#     data = request.args.get('data')
#     if security.verify_signature(data):
#         return "valid"
#     else:
#         return "invalid"

@simon_server_blueprint.route('/gerar_chaves/<device_id>')
@cross_origin()
def verifica_assinatura(device_id):
    keys = security.generate_key_pair(device_id)
    keys["pub_key"] = keys["pub_key"].decode("utf-8")
    keys["priv_key"] = keys["priv_key"].decode("utf-8")
    keys.pop("key_info")
    keys_json = json.dumps(keys)
    return keys_json

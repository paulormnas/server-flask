from flask import (Blueprint, request, send_from_directory)
from flask_cors import cross_origin
from datetime import datetime
from os import path

import json

simon_server_blueprint = Blueprint('simon-server-blueprint', __name__)


@simon_server_blueprint.route('/')
@cross_origin()
def index():
    return "Server funcionando"
    # return send_from_directory("backend/static/", "index.html")


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


import os
import unittest
import json
from backend.server_app import create_app
from flask import request
from os import path


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(mode="test")
        self.app.testing = True
        self.registers_path = path.realpath(path.join(path.curdir, '../registros/'))
        self.dados_de_teste = {
            "id": "dispositivo_001",
            "location": [-22.597412, -43.289396],
            "property": "TEMPERATURA",
            "date": 1604520278.332991,
            "value": 22.3
        }

    def test_da_rota_registrar_dados(self):
        # Faz assert da rota
        with self.app.test_request_context('/registrar_dados'):
            self.assertEqual(request.path, '/registrar_dados')

    def test_de_resposta_da_rota_raiz(self):
        # Utiliza contexto de cliente para uma requisiçao GET na raiz (/) e confere as respostas do serviço
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(200, response.status_code)
            self.assertEqual(b'Server funcionando', response.data)

    def test_de_envio_de_dados_na_rota_registrar_dados(self):
        # Verifica se a quantidade de arquivos a pasta "registros" esta maior apos o envio de dados via POST
        quantidade_inicial_arquivos = len(os.listdir(self.registers_path))
        with self.app.test_client() as client:
            response = client.post('/registrar_dados', data=json.dumps(self.dados_de_teste))
            self.assertEqual(200, response.status_code)

        quantidade_final_arquivos = len(os.listdir(self.registers_path))
        self.assertGreater(quantidade_final_arquivos, quantidade_inicial_arquivos)
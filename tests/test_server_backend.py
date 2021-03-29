import os
import unittest
import json
from backend.server_app import create_app
from flask import request
from os import path
from backend.security.Sign import Signature


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(mode="test")
        self.app.static_folder = "../static"
        self.app.template_folder = "../template"
        self.registers_path = path.realpath(path.join(path.curdir, '..', 'registros'))
        self.std_device_id = "SiMon-standard"
        self.dados_de_teste = {
            "id": "dispositivo_001",
            "location": [-22.597412, -43.289396],
            "property": "TEMPERATURA",
            "date": 1604520278.332991,
            "value": 22.3
        }

        security = Signature()
        assinatura = security.sign(self.dados_de_teste)
        self.dados_de_teste_assinados = self.dados_de_teste.copy()
        self.dados_de_teste_assinados["signature"] = assinatura

    def test_da_rota_registrar_dados(self):
        # Faz assert da rota
        with self.app.test_request_context('/registrar_dados'):
            self.assertEqual(request.path, '/registrar_dados')

    def test_de_resposta_da_rota_raiz(self):
        # Utiliza contexto de cliente para uma requisiçao GET na raiz (/) e confere as respostas do serviço
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertTrue(response.status_code == 200)
            # self.assertEqual(b'Server funcionando', response.data)

    def test_de_envio_de_dados_na_rota_registrar_dados(self):
        # Verifica se a quantidade de arquivos na pasta "registros" esta maior apos o envio de dados via POST
        quantidade_inicial_arquivos = len(os.listdir(self.registers_path))
        with self.app.test_client() as client:
            response = client.post('/registrar_dados', data=json.dumps(self.dados_de_teste))
            self.assertEqual(200, response.status_code)

        quantidade_final_arquivos = len(os.listdir(self.registers_path))
        self.assertGreater(quantidade_final_arquivos, quantidade_inicial_arquivos)

    def test_gerar_chaves_sem_id_do_dispositivo(self):
        # Testa rota de geraçao de chaves sem informar id do dispositivo

        with self.app.test_client() as client:
            response = client.get('/gerar_chaves/')
            self.assertEqual(404, response.status_code)

    def test_gerar_chaves_com_id_do_dispositivo(self):
        # Testa rota de geraçao de chaves informando id do dispositivo

        with self.app.test_client() as client:
            response = client.get('/gerar_chaves/{}'.format(self.std_device_id))
            self.assertEqual(200, response.status_code)
            keys_json = response.data
            keys = json.loads(keys_json)
            self.assertEqual(2, len(keys))

    def test_verificacao_de_assinatura_valida(self):
        # Testa rota de verificaçao de assinatura para chave publica correta
        with self.app.test_client() as client:
            assinatura = self.dados_de_teste_assinados["signature"]
            data = json.dumps(self.dados_de_teste)
            response = client.get('/verifica_dispositivo?device_id={}&data={}'.format(self.std_device_id, data),
                                  data=assinatura)
            self.assertEqual(200, response.status_code)
            verification_response = response.data.decode("utf-8")
            self.assertEqual("valid", verification_response)

    def test_verificacao_de_assinatura_invalida(self):
        # Testa rota de verificaçao de assinatura para chave publica incorreta
        with self.app.test_client() as client:
            assinatura = self.dados_de_teste_assinados["signature"]
            data = json.dumps(self.dados_de_teste)
            response = client.get('/verifica_dispositivo?device_id=SiMon-meter&data={}'.format(data),
                                  data=assinatura)
            self.assertEqual(200, response.status_code)
            verification_response = response.data.decode("utf-8")
            self.assertEqual("invalid", verification_response)

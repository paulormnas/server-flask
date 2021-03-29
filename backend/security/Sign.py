# -*- coding: utf-8 -*-
from datetime import datetime
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class Signature():
    '''
    Objeto para tratar as assinaturas RSA dos dispositivos e gerar chaves criptograficas.
    O arquivo para o banco de dados de chaves dos dispositivos de IoT, devera ser estruturado da seguinte maneira:
    {
        "id": "id_do_dispositivo",
        "date": "data_da_geraçao_da_chave",
        "key_algorithm": "Algoritmo de geraçao de chaves",
        "size": "Tamanho da chave",
        "curve": "Curva utilizada no caso do algoritmo ser curva eliptica, outro caso sera None",
        "sign_algorithm": "Algoritmos de assinatura. Ex.: ECDSA_SHA-256"
        "status": "revoked ou active",
        "key_pem": "chave publica no formato PEM"
    }
    '''
    def __init__(self):
        pass

    def format_key_info(self, device_id, key_size, key_pem, key_algorithm="RSA", sign_algorithm="RSA_SHA-256", curve = None):
        key_info = {
                    "id": device_id,
                    "date": datetime.now().timestamp(),
                    "key_algorithm": key_algorithm,
                    "size": key_size,
                    "curve": curve,
                    "sign_algorithm": sign_algorithm,
                    "status": "active",
                    "key_pem": key_pem
                }
        return key_info

    def generate_key_pair(self, device_id):
        '''
        Gera chaves criptograficas publica e privada, utilizando o algoritmo RSA, com tamanho fixo de 2048, escreve em arquivos e retorna as informaçoes.

        :param:
            device_id: identificaçao do dispositivo que sera utilizado no nome dos arquivos .pem
        :return: um dicionario com chaves publica e privada e informaçoes das chaves para armazenamento em banco de dados
        '''
        key_size = 2048
        priv_key = RSA.generate(key_size)
        priv_key_pem = priv_key.export_key('PEM')
        with open(device_id + '_priv_key.pem', 'wb') as f:
            f.write(priv_key_pem)

        pub_key = priv_key.public_key()
        pub_key_pem = pub_key.export_key('PEM')
        with open(device_id + '_public_key.pem', 'wb') as f:
            f.write(pub_key_pem)

        key_info = self.format_key_info(device_id=device_id, key_size=key_size, key_pem=pub_key_pem)
        return {"priv_key": priv_key_pem,
                "pub_key": pub_key_pem,
                "key_info": key_info}

    def sign(self, dados):
        '''Assina os dados recebidos como paramentro e retorna a assiantura em bytes'''

        convert = str(dados)   #Converte o dicionario em uma string para poder ser em seguida convertido em bytes.
        byte_message = convert.encode()   #Converte a string em bytes para poder gerar o Hash.
        h = SHA256.new(byte_message)   #Gera o Hash da mensagem
        key_path = "SiMon-standard_priv_key.pem"
        key = RSA.import_key(open(key_path).read())
        assinatura = pkcs1_15.new(key).sign(h)
        return assinatura
    
    def verify_signature(self, dados, device_id, signature):
        '''
        Verifica a assinatura dos dados de acordo com a chave publica correspondente ao id do dispositivo

        :param:
            dados: dicionario com os dados que foram assinados
            device_id: id do dispositivo
            signature: assinatura dos dados feita pelo dispositivo

        :return: string "valid" caso a assinatura seja valida ou "invalid" caso a assinatura nao seja valida
        '''
        copy = dados   # Copia o dicionario original para fazer as operacoes de comparacao sem alterar o original
        convert = str(copy)   # Converte o dicionario copiado em uma string para em seguida ser convertido em bytes.
        byte_message = convert.encode()   # Converte a string em bytes para poder gerar o Hash.
        h = SHA256.new(byte_message)   # Gera o Hash da mesagem
        key_path = device_id + "_public_key.pem"    # Informa o caminho para a chave publica a ser verificada
        key = RSA.import_key(open(key_path).read()) # Le a informaçao da chave publica
        try:
            pkcs1_15.new(key).verify(h, signature)  # Verifica assinatura a partir do Hash e da chave informados
        except ValueError:
            print("Assinatura invalida") # Caso ocorra uma exceçao, a assinatura nao e valida
            return "invalid"
        else:
            print("A assinatura e valida")
            return "valid"



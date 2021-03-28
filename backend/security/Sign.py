# -*- coding: utf-8 -*-
import configparser
from datetime import datetime
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class Signature():
    '''
    Classe para tratar as assinaturas RSA dos dispositivos e gerar chaves criptograficas.
    Para o banco de dados de chaves dos dispositivos de IoT, o arquivo devera ser estruturado da seguinte maneira:
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
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

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
        convert = str(dados)   #Converte o dicionario em uma string para poder ser em seguida convertido em bytes.
        bite_mensage = convert.encode()   #Converte a string em bytes para poder gerar o Hash.
        h = SHA256.new(bite_mensage)   #Gera o Hash da mensagem
        print(h.hexdigest())
        key_path = self.config.get('keys','private_key')
        key = RSA.import_key(open(key_path).read())
        assinatura = pkcs1_15.new(key).sign(h)
        print(assinatura)
        return assinatura
    
    def verify_signature(self, dados):

        if dados is isinstance(dict):
            copia = dados   #Copia o dicionario original para fazer as operacoes de comparacao sem alterar o original
            original = dados.get("signature")   #Armazena o valor do campo signature para ser usada na comparacao de chaves
            key_path = self.config.get('keys','private_key')
            key = RSA.import_key(open(key_path).read())
            copia.pop("signature")   #Remove o campo de assinatura da copia para poder gerar um novo hash para comparacao
            convert = str(copia)   #Converte o dicionario copiado em uma string para poder ser em seguida convertido em bytes.
            bite_mensage = convert.encode()   #Converte a string em bytes para poder gerar o Hash.
            h = SHA256.new(bite_mensage)   #Gera o Hash da mesagem
            key_path = self.config.get('keys','public_key')
            key = RSA.import_key(open(key_path).read())
            assinatura = pkcs1_15.new(key).sign(h)
            assinatura = str(assinatura)
            if assinatura == original:
                print("A assinatura e valida")
                return True
            else:
                print("Assinatura invalida")
                return False



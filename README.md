# server-flask
Este projeto e um servidor simples de teste para receber dados de sensores construido com o framework [Flask](https://flask.palletsprojects.com/en/1.1.x/).

Para iniciar o projeto e necessario configurar o ambiente virtual do Python com as dependencias e criar a pasta onde serao armazenados os registros de mediçoes dos sensore.

```bash
git clone https://github.com/paulormnas/server-flask.git
cd server-flask
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
mkdir registros
```
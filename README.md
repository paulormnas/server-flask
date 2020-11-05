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

Para iniciar o serviço basta executar o script 'run.py' e sera iniciado no modo "development" por padrao. Para alterar a instancia de execuçao indique a instancia desejada passando como paramentro na execuçao do script.

```bash
python3 run.py test 
```

Para testar a recepçao de requisiçoes pode-se executar o script de teste disponivel no projeto ou utilizar uma ferramenta como a [RESTED](https://addons.mozilla.org/en-US/firefox/addon/rested/), disponivel como um pluin em diversos browsers. O formato JSON a ser armazenado deve possuir a seguinte estrutura de chaves e valores. 


```json
{
    "id": "dispositivo_001",
    "location": [-22.597412, -43.289396],
    "property": "TEMPERATURA",
    "date": 1604520278.332991,
    "value": 22.3
}
```
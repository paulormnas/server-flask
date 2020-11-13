# server-flask
Este projeto e um servidor simples de teste para receber dados de sensores construido com o framework [Flask](https://flask.palletsprojects.com/en/1.1.x/).

Para iniciar o projeto e necessário configurar o ambiente virtual do Python com as dependências do projeto e criar a pasta onde serão armazenados os registros de medições dos sensores.

```bash
git clone https://github.com/paulormnas/server-flask.git
cd server-flask
pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
mkdir registros
```

Para usuários do Windows recomenda-se utilizar o terminal do [Git para Windows](https://git-scm.com/download/win) que permite executar grande parte dos comandos do ambiente Linux. Com as devidas correções, o ambiente será preparado com os seguintes comandos: 

```bash
git clone https://github.com/paulormnas/server-flask.git
cd server-flask
pip install virtualenv
virtualenv venv
source venv/Scripts/activate
pip install -r requirements.txt
mkdir registros
```

Para iniciar o serviço basta executar o script 'run.py' e será iniciado no modo "development" por padrão. Para alterar a instância de execução indique a instância desejada passando como argumento na execução do script.

```bash
python3 run.py test 
```

Para testar a recepção de requisições pode-se executar o script de teste disponível no projeto ou utilizar uma ferramenta como a [RESTED](https://addons.mozilla.org/en-US/firefox/addon/rested/), disponível como um plugin em diversos browsers. O formato JSON a ser armazenado deve possuir a seguinte estrutura de chaves e valores. 


```json
{
    "id": "dispositivo_001",
    "location": [-22.597412, -43.289396],
    "property": "TEMPERATURA",
    "date": 1604520278.332991,
    "value": 22.3
}
```
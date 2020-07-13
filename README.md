<a href="https://codecov.io/gh/LucasFDutra/flask-api">
  <img src="https://codecov.io/gh/LucasFDutra/flask-api/branch/dev/graph/badge.svg" />
</a>

# Instalando o poetry

- Para o bash execute os comando

```shell
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

$ source $HOME/.poetry/env

$ poetry --version
```

- Para o zsh execute o comando

```shell
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
```
adicione ao arquivo .zshrc a linha

```shell
export PATH=$PATH:$HOME/.poetry/bin
```
E depois rode o comando

```shell
$ poetry --version
```

# criando um projeto com o poetry

```shell
$ poetry new nome_do_projeto
```

Isso vai criar o arquivo .toml e os pacotes, mas o importante é o arquivo .toml

# configurando a virtualenv

instale o venv
```shell
$ sudo apt-get install python3-venv
```

Agora rode o comando

```shell
$ poetry env use 3.8
$ poetry shell
```

> OBS.: Esse 3.8 é a versão do python que irá rodar nesse env

> OBS.: Se quiser testar para ver que deu tudo certo, digite python3 no terminal, e importe alguma lib que tem no seu pc, se acusar que não existe então é pq está dentro do ambiente virtual. E Para sair do ambiente virtual, basta dar o comando exit no terminal.

# adicionar dependências com o poetry

```shell
$ poetry add nome_do_pacote
```

# Fazendo testes

Primeiramente instale a lib do pytest com o comando

```shell
$ poetry add --dev pytest
$ poetry add --dev pytest-cov
```

Agora crie arquivos com os nomes test_modulo.py ou modulo_test.py

para rodar os testes, rode com o comando

```shell
$ pytest --cov=./src --cov-report=xml
```

# Lint
fora da sua virtual env, rode os comandos:

```shell
$ pip3 install pylint
$ pip3 install flake8
$ pip3 install autopep8
```
e adicione essas configurações ao seu vscode

```json
"python.linting.flake8Enabled": true,
"[python]": {
"editor.formatOnSave": true
}
```

Agora o lint vai modificar seu arquivo assim que salvar


# gerar requiremenst.txt
dependencias de prod

```shell
poetry export -f requirements.txt > requirements.txt
```

dependencias de prod + dev

```shell
poetry export --dev -f requirements.txt > requirements.txt
```


# processo de ci com github actions

```yml
# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Python application CI
on:
  pull_request:
    branches: [ master, dev ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry export --dev -f requirements.txt > requirements.txt
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with pytest
      run: |
        pytest --cov=./src --cov-report=xml
    - uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml # optional
        name: codecov-umbrella # optional
        fail_ci_if_error: true # optional (default = false)
```


# docker

## instalar o gunicorn

```shell
$ poetry add gunicorn
```

gere o arquivo requirements.txt

```shell
$ poetry export -f requirements.txt > requirements.txt
```

crie os arquivos `Dockerfile`, `docker-compose.yml` e `.dockerignore`

Pege eles aqui no repositório

rode o comando
```shell
$ docker-compose up -d
```

ou crie o arquivo `init_docker.sh` e rode o comando

```shell
$ source init_docker.sh
```

isso vai fazer rodar o docker como ambiente de produção

# conexão com postgres.
vamos utilizar o psycopg para isso, então rode

```shell
$ poetry add psycopg2
```

se der um erro, veja se não é por falta da lib `libpq-fe.h`. se for rode o comando

```shell
$ sudo apt-get install libpq-dev
```

e mande instalar o psycopg2 novamente

vamos utilizar variáveis ambiente para poder gerenciar o nosso banco de dados, logo precisaremos da lib dotenv, que no python se chama `python-dotenv`. Criar o arquivo .env e chamar ele na conexão

rode

```shell
$ poetry add python-dotenv
```


# docker de testes

```shell
$ docker run -p 5433:5432 --name postgres-test -e POSTGRES_DB=FLASK-API-TEST -e POSTGRES_PASSWORD=1234 -d postgres
```

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

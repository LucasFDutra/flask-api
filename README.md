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

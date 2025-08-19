# WorkoutAPI

### Badges

![Linguagem](https://img.shields.io/badge/python-3.11.4-blue.svg)
![Framework](https://img.shields.io/badge/FastAPI-0.100.1-brightgreen.svg)
![Banco de Dados](https://img.shields.io/badge/PostgreSQL-11-blue.svg)
![Docker](https://img.shields.io/badge/Docker-24.0.5-blue.svg)

### Índice

* [Descrição do Projeto](#descrição-do-projeto)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Status do Projeto](#status-do-projeto)
* [Funcionalidades e Demonstração da Aplicação](#funcionalidades-e-demonstração-da-aplicação)
* [Equipe do Projeto](#equipe-do-projeto)
* [Conclusão](#conclusão)
* [Prévia do Projeto](#prévia-do-projeto)

## Descrição do Projeto

Esta é uma API de competição de crossfit chamada WorkoutAPI[cite: 53]. [cite_start]É uma API pequena, devido a ser um projeto mais hands-on e simplificado. A API é assíncrona, o que significa que a linguagem tem um jeito de dizer para o computador / programa que em certo ponto, ele terá que esperar por algo para finalizar em outro lugar.

### Tecnologias Utilizadas

A API foi desenvolvida utilizando `FastAPI` (async), junto das seguintes libs: `alembic`, `SQLAlchemy` e `pydantic`. Para salvar os dados, foi utilizado o `postgres`, por meio do `docker`.

### Estrutura do Projeto

O projeto segue uma arquitetura modular para garantir organização e fácil manutenção. A estrutura de pastas é a seguinte:

```bash
.
├── .gitignore
├── Makefile
├── README.md
├── alembic.ini
├── alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── c006e8463eb4_init_db.py
├── docker-compose.yml
├── mer.jpg
├── requirements.txt
└── workout_api
├── init.py
├── atleta
│   ├── init.py
│   ├── controller.py
│   ├── models.py
│   └── schemas.py
├── categorias
│   ├── init.py
│   ├── controller.py
│   ├── models.py
│   └── schemas.py
├── centro_treinamento
│   ├── init.py
│   ├── controller.py
│   ├── models.py
│   └── schemas.py
├── configs
│   ├── init.py
│   ├── database.py
│   └── settings.py
├── contrib
│   ├── init.py
│   ├── dependencies.py
│   ├── models.py
│   ├── repository
│   │   ├── init.py
│   │   └── models.py
│   └── schemas.py
├── main.py
└── routers.py
```

### Status do Projeto

✅ Concluído.

## Funcionalidades e Demonstração da Aplicação

### Principais Funcionalidades

* **CRUD completo** para Atletas, Categorias e Centros de Treinamento.
* **Manipulação de exceções** com retorno de mensagens amigáveis em caso de CPF duplicado, com `sqlalchemy.exc.IntegrityError` e o status code `303`.
* **Filtragem de atletas** por nome e CPF.
* **Paginação** de resultados em listagens, usando a biblioteca `fastapi-pagination` com `limit` e `offset`.
* **Resposta customizada** para o endpoint de consulta de atletas, retornando apenas nome, centro de treinamento e categoria.

### Como funciona

A API utiliza o FastAPI para receber requisições HTTP. O `Uvicorn` atua como o servidor web. Para interagir com o banco de dados, o `SQLAlchemy` é usado como um ORM (Object-Relational Mapper) que traduz os objetos Python em comandos SQL. O `Pydantic` valida os dados de entrada e saída. O `Docker` é responsável por rodar o banco de dados `PostgreSQL` em um ambiente isolado.

### Como Usar a Aplicação

1.  **Instale as dependências:**
    * Para executar o projeto, utilizei a [pyenv], com a versão 3.11.4 do `python` para o ambiente virtual.
    * Caso opte por usar pyenv, após instalar, execute:
      * `pyenv virtualenv 3.11.4 workoutapi`
      * `pyenv activate workoutapi`
      * `pip install -r requirements.txt` 

2.  **Suba o banco de dados com Docker Compose:**
    * Em seguida, execute `make run-docker`.

3.  **Crie as migrações e o banco de dados:**
    * Para criar uma migration nova, execute `make create-migrations d="nome_da_migration"`.
    * Para criar o banco de dados, execute `make run-migrations`.

4.  **Suba a API:**
    * Para subir a API, execute `make run`.
    * Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

## Equipe do Projeto

<a href="https://github.com/amaro-netto" title="Amaro Netto"><img width="180" src="https://github.com/user-attachments/assets/b7a3a1bf-304a-4974-b75f-1d620ad6ecf1"/></a>

## Conclusão

Este projeto demonstrou a criação de uma API robusta e escalável, utilizando as ferramentas mais modernas do ecossistema Python. A estrutura modular e as boas práticas de desenvolvimento garantem que o projeto possa ser facilmente expandido e mantido no futuro.

## Prévia do Projeto




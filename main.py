# Importa a classe FastAPI
from fastapi import FastAPI

# Cria uma instância da nossa API
app = FastAPI()

# Cria um "caminho" (endpoint) que responde a uma requisição GET
# Quando alguém acessar a URL principal, a função 'hello' será chamada.
@app.get("/")
def hello():
    return {"message": "Hello World!"}

# Para rodar a sua API, vamos usar o uvicorn, que já instalamos.
# No terminal, com o ambiente virtual ativado, digite:
# uvicorn main:app --reload
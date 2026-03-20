from fastapi import FastAPI
import psycopg2

app = FastAPI()


def conectar():

    conn = psycopg2.connect(
        host="localhost",
        database="scraper_db",
        user="postgres",
        password="postgres"
    )

    return conn


@app.get("/")
def home():
    return {"mensagem": "API de monitoramento de preços rodando"}


@app.get("/produtos")
def listar_produtos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"produtos": dados}


@app.get("/historico")
def historico_precos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT titulo, preco, data_coleta
        FROM produtos
        ORDER BY data_coleta DESC
        """
    )

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"historico": dados}
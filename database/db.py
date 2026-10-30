import psycopg2


def conectar():
    import os
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Defina DATABASE_URL ou execute python demo.py para demonstrar sem banco.")
    conn = psycopg2.connect(database_url)
    return conn


def salvar_produtos(produtos, fonte):

    conn = conectar()
    cursor = conn.cursor()

    for produto in produtos:

        titulo = produto.get("titulo", "Sem título")
        preco = produto.get("preco", "0")
        link = produto.get("link", "Sem link")

        cursor.execute(
            """
            INSERT INTO produtos (titulo, preco, link, fonte)
            VALUES (%s, %s, %s, %s)
            """,
            (titulo, str(preco), link, fonte)
        )

    conn.commit()

    cursor.close()
    conn.close()

    print(f"{len(produtos)} produtos salvos no banco.")


def buscar_ultimo_preco(titulo, fonte):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT preco
        FROM produtos
        WHERE titulo = %s AND fonte = %s
        ORDER BY data_coleta DESC
        LIMIT 1 OFFSET 1
        """,
        (titulo, fonte)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return resultado[0]

    return None


def salvar_quedas(quedas, tipo):

    if not quedas:
        return

    conn = conectar()
    cursor = conn.cursor()

    for queda in quedas:
        cursor.execute(
            """
            INSERT INTO quedas_detectadas
            (titulo, preco_anterior, preco_atual, fonte, tipo, link)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                queda["titulo"],
                queda["preco_anterior"],
                queda["preco_atual"],
                queda["fonte"],
                tipo,
                queda.get("link", "Sem link")
            )
        )

    conn.commit()

    cursor.close()
    conn.close()

    print(f"{len(quedas)} quedas do tipo '{tipo}' salvas no banco.")
import psycopg2
import pandas as pd
import os


def get_conn():
    conn = psycopg2.connect(
        host=os.getenv("HOST"), 
        port=os.getenv("PORT"), 
        dbname=os.getenv("DATABASE_NAME"), 
        user=os.getenv("DATABASE_USER"), 
        password=os.getenv("DATABASE_USER_PASSWORD")
    )

    return conn, conn.cursor()


def get_data(query): 
    conn, cur = get_conn()

    cur.execute(query)

    result = cur.fetchall()

    df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])

    cur.close()
    conn.close()

    return df

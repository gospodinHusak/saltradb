import psycopg2
import logging
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

def get_conn():
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"), 
            port=os.getenv("POSRT"), 
            dbname=os.getenv("DBNAME"), 
            user=os.getenv("USER"), 
            password=os.getenv("PASSWORD")
        )
    except:
        logger.error(Exception)
    return conn, conn.cursor()


def get_data(query): 
    conn, cur = get_conn()

    cur.execute(query)

    result = cur.fetchall()

    df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])

    cur.close()
    conn.close()

    return df

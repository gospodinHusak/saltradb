import psycopg2
import logging
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8')

logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)



def get_conn():
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"), 
            port=os.getenv("POSRT"), 
            dbname=os.getenv("DBNAME"), 
            user=os.getenv("USER"), 
            password=os.getenv("PASSWORD")
        )

        return conn, conn.cursor()
    
    except psycopg2.errors.ConnectionException as e:
        logger.error(e)
        raise e
    
    except psycopg2.errors.ConnectionFailure as e2:
        logger.error(e2)
        raise e2
    
    


def get_data(query): 
    conn, cur = get_conn()

    cur.execute(query)

    result = cur.fetchall()

    df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])

    cur.close()
    conn.close()

    return df

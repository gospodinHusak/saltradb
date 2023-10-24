import psycopg2
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

import os


def get_data(query): 
    conn = psycopg2.connect(
        host=os.getenv("HOST"), 
        port=os.getenv("POSRT"), 
        dbname=os.getenv("DBNAME"), 
        user=os.getenv("USER"), 
        password=os.getenv("PASSWORD")
    )
    cur = conn.cursor()

    cur.execute(query)

    result = cur.fetchall()

    df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])

    cur.close()
    conn.close()

    return df

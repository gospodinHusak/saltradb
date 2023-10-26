from funcs import get_data
from dotenv import load_dotenv
load_dotenv()

import os

full_df = get_data(query=f"SELECT * FROM {os.getenv('MAIN_VIEW')}")

col_rules = {
    'date': 'minmax',
    'market' : 'unique',
    'buyer': 'unique',
    'seller': 'unique',
    'production': 'unique',
    'amount': 'minmax',
    'cost': 'minmax',
    'price': 'minmax',
    'source': 'unique',
}

col_names = {
    'id_sale': 'ID',
    'date': 'Дата',
    'date2': 'Конечная Дата',
    'market' : 'Рынок',
    'buyer': 'Покупатель',
    'seller': 'Продавец',
    'production': 'Производство',
    'amount': 'Количество',
    'cost': 'Стоимость',
    'price': 'Цена',
    'source': 'Источник',
    'page': 'Л./Стр.'
}

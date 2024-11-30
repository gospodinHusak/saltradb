from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import os

OVERVIEW_TEXT = '''
    В качестве СУБД для построения базы данных о торговле солью в 17 веке в России используется PostgreSQL. Выбор в ее пользу обусловлен несколькими факторами. 
    Во-первых, PostgreSQL является универсальным решением для связки с веб-приложением, поскольку обеспечивает высокую производительность при работе с данными.
    Во-вторых, PostgreSQL - объектно-реляционная СУБД, что позволяет эффективно организовывать и управлять данными, сохраняя связь между разными сущностями, например, сделками, рынками, акторами. 
    Наконец, PostgreSQL является свободным (open-source) проектом, с крупным сообществом и обширной документацией, что помогает решать любые задачи в процессе разработки.
'''

def create_list(dic):
    return [html.Li([html.Strong(key), ' - ', description]) for key, description in dic.items()]

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("На главную", href="/")),
        html.Div(style={'borderLeft': '1px solid gray', 'height': '20px', 'margin': '10px 10px'}),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Источники", href="/sources"),
                dbc.DropdownMenuItem("Визуализации", href="/charts"),
                dbc.DropdownMenuItem("Контруктор таблиц", href="/table-constructor"),
            ],
            nav=True,
            align_end=True,
            in_navbar=True,
            label="Другие страницы",
        )
    ],
    brand="О базе данных",
    color="primary",
    dark=True
)

layout = dbc.Container(
    id='about-db-page',
    children=[
        navbar,
        html.Div(
            id='home-main-content',
            children=[                
                html.P(id='why-pgsql', children=OVERVIEW_TEXT),
                html.H3("Таблицы базы данных"),
                html.Ul(
                    create_list(
                        {
                            'sales': 'записи о сделках с солью',
                            'actors': 'акторы сделок',
                            'markets': 'рынки',
                            'productions': 'места производств',
                            'sources': 'источники',
                            'storages': 'уникальные связки фонд-опись',
                            'archives': 'архивы',
                            'silver': 'справочная таблица с разграммовкой серебра в рубле'
                        }
                    )
                ),
                html.H3("Структура таблиц"),
                html.H4("sales:"),
                html.Ol(
                    create_list(
                        {
                            "id_sale": "уникальный id сделки;",
                            "date": "дата сделки / нижняя граница промежутка, в котором была совершена сделка, если точная дата не известна;",
                            "date2": "NULL / верхняя граница промежутка, в котором была совершена сделка, если точная дата не известна;",
                            "amount": "количество товара в пудах;",
                            "cost": "стоимость в деньгах;",
                            "fid_market": "внешний id рынка сделки;",
                            "fid_seller": "внешний id продавца;",
                            "fid_buyer": "внешний id покупателя;",
                            "fid_production": "внешний id места производства соли;",
                            "fid_source": "внешний id источника;",
                            "page": "лист(ы) в источнике, откуда взяты данные."
                        }
                    )
                ),

                html.H4("actors:"),
                html.Ol(
                    create_list(
                        {
                            "id": "id актора, по которому осуществляется связь с fid_seller и fid_buyer из таблицы sales;",
                            "name": "имя/название участника сделки;",
                            "type": "человек, монастырь, др.",
                        }
                    )
                ),

                html.H4("markets:"),
                html.Ol(
                    create_list(
                        {
                            "id": "id рынка, по которому осуществляется связь с fid_market из таблицы sales;",
                            "name": "название рынка;",
                            "location": "краткое обозначение локации."
                        }
                    )
                ),

                html.H4("productions:"),
                html.Ol(
                    create_list(
                        {
                            "id": "id производства, по которому осуществляется связь с fid_production из таблицы sales;",
                            "name": "название производства;",
                            "location": "краткое обозначение локации."
                        }
                    )
                ),

                html.H4("sources:"),
                html.Ol(
                    create_list(
                        {
                            "id": "id источника;",
                            "fid_storage": "внешний id для связи с таблицей storages;",
                            "name": "название документа;",
                            "storage_unit": "единица хранения;",
                            "sheets": "общее количество листов."
                        }
                    )
                ),

                html.H4("storages:"),
                html.Ol(
                    create_list(
                        {
                            "id": "id фонда и описи;",
                            "fid_archive": "внешний id для связи с таблицей archives;",
                            "fund": "номер фонда;",
                            "inventory": "номер описи."
                        }
                    )
                ),

                html.H4("archives:"),
                html.Ol(
                    create_list(
                        {
                            "id": "id архива;",
                            "name": "название архива.",
                        }
                    )
                ),

                html.H4("silver:"),
                html.Ol(
                    create_list(
                        {
                            "date_start": "дата, с которой действует указанный в grams вес серебра;",
                            "date_end": "дата, до которой действует указанный в grams вес серебра;",
                            "grams": "вес серебра в одном рубле."
                        }
                    )
                ),

                html.P(
                    '''
                    Такая структура позволила компактно организовать данные, заменив повторяющиеся 
                    строковые значения (например, акторов, рынки, название источника) в таблице sales на целочисленные id.
                    '''
                )
            ]
        )
    ],
    class_name='page-layout',
    fluid=True
)

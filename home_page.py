from dash import html
import dash_bootstrap_components as dbc


# Описание проекта
overview = '''
    Описание ресурса
'''

# Карточки с ссылками на страницы
card1 = dbc.Card(
    [
        dbc.CardHeader(
            'SQL-редактор'
        ),
        dbc.CardBody(
            [
                html.P(
                    "В рамках проекта для пользователей, обладающих навыками работы с SQL, "
                    "создана страница, на которой можно строить собственные запросы к БД. ",
                    className="card-text",
                ),
            ]
        ),
        dbc.CardFooter(
            html.A('Перейти к SQL-редактору', href='/sql')
        )
    ],
    class_name='h-100'
)

card2 = dbc.Card(
    [
        dbc.CardHeader(
            'Таблица с фильтрами'
        ),
        dbc.CardBody(
            [
                html.P(
                    "Для пользователей, не владеющих языком SQL, а также для тех, "
                    "кто хочет ознакомиться с данными на самом базовом уровне "
                    "разработана страница, на которой размещена таблица со всеми "
                    "сделками имеющимися в БД.",
                    className="card-text",
                ),
            ]
        ),
        dbc.CardFooter(
            html.A('Перейти к таблице', href='/filtering')
        )
    ],
    class_name='h-100'
)

# Карточка с дополнительной страничкой
extra_card = dbc.Card(
    [
        dbc.CardHeader(
            'Графики'
        ),
        dbc.CardBody(
            [
                html.P(
                    "В качестве дополнительной опции для работы с БД было "
                    "подготовлено несколько графиков. Их основное предназначение "
                    "заключается в визуальном представлении содержания БД.",
                    className="card-text",
                ),
            ]
        ),
        dbc.CardFooter(
            html.A('Перейти к графикам', href='/dashboard')
        )
    ],
)


home_layout = dbc.Container(
    [
        dbc.Row(
            className='jumbotron',
            children=[
                html.H1('Название веб-ресурса'),
                html.P(overview)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(card1, style={'padding': '0 5px 0 0'}),
                dbc.Col(card2, style={'padding': '0 0 0 5px'})
            ],
            style={'marginBottom': '10px'},
            justify="around",
        ),
        dbc.Row(extra_card)
    ],
    id='home-page',
)
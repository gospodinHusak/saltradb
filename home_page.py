from dash import html
import dash_bootstrap_components as dbc


# Описание проекта
overview = '''
    Данное приложение представляет собой специализированный ресурс для работы с базой данных, 
    содержащей обширные количественные данные о торговле солью в XVII веке на Русском Севере. 
    Его основной целью является обеспечение свободного доступа к материалам источников и 
    возможности анализа данных с исследовательскими целями. Предполагается, что данный ресурс 
    будет продолжать свое развитие за счет накопления более широкого объема данных и 
    предоставления более детального инструментария для работы с ними.
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
            html.A('Перейти к SQL-редактору', href='/sql_editor')
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
            html.A('Перейти к таблице', href='/table')
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
            html.A('Перейти к графикам', href='/charts')
        )
    ],
    style={'padding': '0'}
)


home_layout = dbc.Container(
    [
        dbc.Row(
            className='jumbotron',
            children=[
                html.H3('Соляной рынок Русского Севера в XVII в.: открытая база данных'),
                html.P(overview, style={'padding': '5px', 'textAlign': 'justify'})
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
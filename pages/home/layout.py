from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import os

OVERVIEW_TEXT = '''
    Проект представляет собой веб-сервис для взаимодействия с базой данных, в которой 
    собраны сведения о торговле солью в XVII веке на Русском Севере. 
'''

def nav_card(id, title):
    return html.Div(
        id=id,
        children=html.A(
            html.H3(title),
            className='nav-button',
            href=f'/{id}',
        ),
        className='nav-card'
    )

cards_config={
    'charts': 'Визуализации',
    'table-constructor': 'Конструктор таблиц'
}


navbar = dbc.NavbarSimple(
    id='home-nav',
    children=[
        dbc.NavItem(dbc.NavLink("Конструктор таблиц", href="/table-constructor")),
        dbc.NavItem(dbc.NavLink("Визуализации", href="/charts")),
        dbc.NavItem(dbc.NavLink("О базе данных", href="/about-database", disabled=True)),
        dbc.NavItem(dbc.NavLink("Методология", href="/methodology", disabled=True))
    ],
    brand="Соляной рынок Русского Севера в XVII в.",
    color="primary",
    dark=True
)

layout = dbc.Container(
    id='home-page',
    children=[
        navbar,
        html.Div(
            id='home-main-content',
            children=[
                html.H2('О проекте'),
                html.P(OVERVIEW_TEXT),
                html.Hr(),
                html.Div(
                    id='nav-cards-container',
                    children=[
                        nav_card(id, title) 
                        for id, title in cards_config.items()
                    ],
                ),
                html.Hr()
            ]
        )
    ],
    class_name='page-layout',
    fluid=True
)

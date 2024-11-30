from dash import dcc, html
import dash_bootstrap_components as dbc


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("На главную", href="/")),
        html.Div(style={'borderLeft': '1px solid gray', 'height': '20px', 'margin': '10px 10px'}),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Визуализации", href="/charts"),
                dbc.DropdownMenuItem("Контруктор таблиц", href="/table-constructor"),
                dbc.DropdownMenuItem("О базе данных", href="/about-db"),
            ],
            nav=True,
            align_end=True,
            in_navbar=True,
            label="Другие страницы",
        )
    ],
    brand="Источники",
    color="primary",
    dark=True
)

layout = dbc.Container(
    id='sources-page',
    children=[
        dcc.Store(id='sources-store'),
        navbar,
        html.Div(
            id='home-main-content',
            children=[                
                html.Ol(
                    id='sources-list'
                )
            ]
        )
    ],
    class_name='page-layout',
    fluid=True
)

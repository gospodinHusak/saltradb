from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from common_components import card

cards_col = html.Div(
    id='filters-col',
    children=[
        card(
            title="Фильтры", 
            index='filters', 
            is_open=True,
            is_closable=False
        ),
        dbc.Button(
            children=[
                html.Span(
                    [
                        DashIconify(
                            icon="material-symbols-light:play-arrow",
                            width=30, 
                            style={'padding':'0','display':'inline-block'}
                        ),
                        html.Div(
                            'Применить фильтры', 
                            style={
                                'display':'inline-block',
                                'height':'24px', 
                                'line-height':'24px'
                            }
                        )
                    ], 
                    style={'display':'inline-block'}
                )
            ], 
            id='apply-filters-button',
            n_clicks=0,
            color='success',
            size='md',
            class_name='panel-button',
            style={
                'margin-top': '5px',
                'border-color': 'rgba(93,208,185, .5)',
                'width': '400px'
            }
        )
    ],
    style={
        'width': '400px',
        'height':'calc(100vh - 40px)',
        'overflow-y': 'auto'
    }
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("На главную", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Другие страницы",
        )
    ],
    brand="Визуализации",
    color="primary",
    dark=True
)


layout = dbc.Container(
    [
        dcc.Store(id='filters-store'),
        dcc.Store(id='charts-config-store'),
        dcc.Store(id='where-statement-store'),
        navbar,
        html.Div(
            [
                cards_col,
                html.Div(
                    id='chart-container',
                    style={'flex': '1'}
                )
            ],
            style={
                'display': 'flex',
                'height':'calc(100vh - 85px)'
            },
        )
        
    ],
    class_name='page-layout',
    fluid=True
)


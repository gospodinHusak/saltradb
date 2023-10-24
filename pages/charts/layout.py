from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from filter_funcs import create_components
from table import full_df, col_names, col_rules



components = create_components(rules=col_rules, names=col_names, df=full_df, page='dashboard')

navbar = html.Nav(
    html.Div(
        [
            html.Button(
                html.A(
                    DashIconify(icon='octicon:home-24', width=30), 
                    href='/'
                ), 
                className='nav-button'
            ),
            html.H3('Визуализации', className='brand'),
            html.Div(
                dbc.ButtonGroup(
                    [
                        html.Button(
                            DashIconify(icon='teenyicons:info-small-solid', width=30),
                            id='page-overview-toggle-btn',
                            n_clicks=0,
                            className='nav-button',
                        ),
                        html.Button(
                            DashIconify(icon='system-uicons:filtering', width=30),
                            id='filterpanel-toggle-btn',
                            n_clicks=0,
                            className='nav-button'
                        )
                    ]
                ),
                className='nav-panel-buttons'
            )
        ],
        className='d-flex'
    ),
    id='dashboard-navbar',
    className='custom-navbar'
)    

layout = html.Div(
    [
        navbar,
        html.Div(
            id='dashboard-filterpanel-container',
            children=[
                dbc.Accordion(components, flush=True),
                html.Button('Применить', id='dashboard-apply-filters-button', className='apply-button')
            ],
            className='collapsed'
        ),
        dbc.Tabs(
            id='tabs',
            children=[
                dbc.Tab(id='tab1', children=[dcc.Graph(id='graph1')], label='Количество сделок по рынкам'),
                dbc.Tab(id='tab2', children=[dcc.Graph(id='graph2')], label='Суммарная стоимость сделок по рынкам'),
                dbc.Tab(id='tab3', children=[dcc.Graph(id='graph3')], label='Динамика среднегодовых цен'),
            ]
        )
    ]
)


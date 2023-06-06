from dash import Dash, dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
import dash_ace
from filter_funcs import create_components
from table import full_df, col_names, col_rules



components = create_components(rules=col_rules, names=col_names, df=full_df, page='filtering')
df = full_df.rename(columns=col_names)

navbar = html.Nav(
    html.Div(
        [
            html.H3('Фильтрация данных', className='brand'),
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
    id='filtering-navbar',
    className='custom-navbar'
)    

filtering_layout = html.Div(
    [
        dcc.Download(id="download-dataframe-excel"),
        navbar,
        html.Div(
            id='filterpanel-container',
            children=[
                dbc.Accordion(components, flush=True),
                html.Button('Применить', id='filtering-apply-filters-button')
            ],
            className='collapsed'
        ),
        html.Div(
            [
                html.H5('Показать колонки:'),
                dbc.Checklist(
                    id="columns-list-checklist-all-value",
                    options=[{"label": "Все", "value": "Все"}],
                    value=['Все'],
                    persistence=True,
                    persistence_type="session",
                    class_name='all-value-option filter'
                ),
                dbc.Checklist(
                    id='columns-list-checklist',
                    options=[{'label': i, 'value': i} for i in df.columns],
                    value=df.columns,
                    persistence=True,
                    persistence_type="session",
                    class_name='filter'
                )
            ],
            style={'display':"none"},
            id='columns-list-div'
        ),
        html.Div(
            [
                dbc.ButtonGroup(
                    children=[
                        html.Button(
                            id='filtering-download-table', children=DashIconify(icon='ic:file-download', width=30), n_clicks=0,
                            className='little-button'
                        ),
                        html.Button(
                            id='columns-list-button', children=DashIconify(icon='material-symbols:event-list', width=30), n_clicks=0,
                            className='little-button'
                        )
                    ],
                    vertical=True, 
                    class_name='btn-grp-aaa'
                ),  
                html.Div(
                    [
                        dash_table.DataTable(
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.to_dict('records'), 
                            id='filtering-table',
                            cell_selectable=False,
                        )
                    ],
                    id='filtering-table-container'
                ),
            ],
            id='filtering-content'
        )
    ]
)


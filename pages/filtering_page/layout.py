from dash import Dash, dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
import dash_ace
import filter_funcs as ff
from pages.filtering_page.table import full_df
from pages.filtering_page.config import col_names, col_rules





def get_column_minmax(df, column):
    return df[column].sort_values().agg(['min', 'max']).tolist()

def get_column_unique(df, column):
    return df[column].unique().tolist()


funcs = {
    'minmax': get_column_minmax,
    'unique': get_column_unique
}


filter_config = {}
for k, v in col_rules.items():
    filter_config[k] = funcs[v](full_df, k)


components = []
for k, v in col_rules.items():
    if v == 'unique':
        components.append(ff.checkbox(name=col_names[k], col=k, values=filter_config[k]))
    elif v == 'minmax':
        if k == 'date':
            components.append(ff.date_filter(name=col_names[k], col=k, values=filter_config[k]))
        else: 
            components.append(ff.interval(name=col_names[k], col=k, values=filter_config[k]))



full_df.rename(columns=col_names, inplace=True)

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
                html.Button('Применить', id='apply-filters-button')
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
                    options=[{'label': i, 'value': i} for i in full_df.columns],
                    value=full_df.columns,
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
                        ),
                        html.Button(
                            id='filtering-plot', children=DashIconify(icon='carbon:qq-plot', width=30), n_clicks=0,
                            className='little-button'
                        ),
                    ],
                    vertical=True, 
                    class_name='btn-grp-aaa'
                ),  
                html.Div(
                    [
                        dash_table.DataTable(
                            columns=[{"name": i, "id": i} for i in full_df.columns],
                            data=full_df.to_dict('records'), 
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


from dash import dcc, html
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import sqlite3
from dash_ace import DashAceEditor



def get_tables():
    conn = sqlite3.connect('master.db')
    tables = [
        i[0] 
        for i in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() 
        if i[0] != 'sqlite_sequence'
    ]
    conn.close()
    return tables



navbar = html.Nav(
    html.Div(
        [
            html.H3('SQL-редактор', className='brand'),
            html.Div(
                dbc.ButtonGroup(
                    [
                        html.Button(
                            DashIconify(icon='teenyicons:info-small-solid', width=30),
                            id='page-overview-toggle-btn',
                            n_clicks=0,
                            className='nav-button',
                        )
                    ]
                ),
                className='nav-panel-buttons'
            )
        ],
        className='d-flex'
    ),
    id='sql-navbar',
    className='custom-navbar'
)

sql_textarea = html.Div(
    id='sql-text-area',
    children=[
        DashAceEditor(
            id='sql-query-input',
            value='SELECT * FROM Sales',
            theme='github',
            mode='sql',
            enableBasicAutocompletion=True,
            enableLiveAutocompletion=True,
            autocompleter='/autocompleter?prefix=',
            placeholder='SQL code'
        ),
        html.Button('Отработать запрос', id='sql-query-run'),
    ]
)


tables = get_tables()
db_schemas = html.Div(
    id='table-schemas',
    children=[
        html.Div(
            id='filter-column', 
            children=[
                html.P('Таблицы'),
                dcc.RadioItems(
                id='info-radio',
                options=[{'label': i, 'value': i} for i in tables],
                value=tables[0],
                labelStyle={'display': 'block'},
                ),
            ]
        ),
        html.Div(
            className='table-column', 
            children=[
                DataTable(
                    id='info-table',
                    columns=[
                        {'name': 'Name', 'id': 'name'},
                        {'name': 'Type', 'id': 'type'},
                        {'name': 'Nullable', 'id': 'nullable'},
                        {'name': 'Default Value', 'id': 'default_value'},
                        {'name': 'Primary Key', 'id': 'primary_key'}
                    ],
                    cell_selectable=False,
                    style_table={'width': '100%', 'height': 'calc(60vh - 60px)'}
                ),
            ]
        ),
    ],
)

main_content = html.Div(
    [
        html.Div(id='sql-editor-container', children=[sql_textarea, db_schemas]),
        html.Div(id='sql-data-container'),
    ],
    className='content'
)

sql_layout = html.Div(id='sql-page', children=[navbar, main_content])
    
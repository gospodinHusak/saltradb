from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc

from home_page import home_layout
from pages.sql_editor.layout import layout as sql_editor_layout
from pages.table.layout import layout as table_layout
from pages.charts.layout import layout as charts_layout


app = Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
)
app.config.suppress_callback_exceptions=True

app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ],
    id='page-body',
    # style={'width': '100vw', 'height': '100vh'}
)

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/sql_editor':
        return sql_editor_layout
    elif pathname == '/table':
        return table_layout
    elif pathname == '/charts':
        return charts_layout
    else:
        return 'Ошибка 404: страница не найдена'




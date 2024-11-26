from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc

from pages.home.layout import layout as home
from pages.charts.layout import layout as charts
from pages.table_constructor.layout import layout as table_constructor
from pages.about_db.layout import layout as about_db


app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
)

app.title = 'Salt Trade DB'
app._favicon = "logo.png"

app.config.suppress_callback_exceptions=True

app.layout = html.Div(
    id='page-body',
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]
)

PAGES = {
    '/': home,
    '/charts': charts,
    '/table-constructor': table_constructor,
    '/about-db': about_db
}

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname not in PAGES.keys():
        return 'Ошибка 404: страница не найдена'
    return PAGES[pathname]
        




from dash import html

home_layout = html.Div(
    id='home-page',
    children=[
        html.H1('Name'),
        html.P('Description'),
        html.Div(
            [
                html.A('go to SQL', href='/sql'),
                html.A('go to filtering', href='/filtering')
            ]
        ),
        html.P('Credits')
    ]
)
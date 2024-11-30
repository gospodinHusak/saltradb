from app import app
from dash import Output, Input, html
from funcs import get_data


@app.callback(
    Output('sources-list', 'children'),
    Input('sources-store', 'modified_timestamp')
)
def update_sources_store(*args):
    sources = get_data(
        '''
            SELECT *
            FROM vw_sources_list
        '''
    )

    return [html.Li(i) for i in sources.source.to_list()]
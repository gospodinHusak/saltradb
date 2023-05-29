from app import app
from dash import Output, Input, State, html
from dash.dash_table import DataTable
from pandas import DataFrame
import sqlite3


@app.callback(
    Output('info-table', 'data'),
    Input('info-radio', 'value'),
)
def show_table_schema(table):
        conn = sqlite3.connect('master.db')
        results = conn.execute(f"PRAGMA table_info({table})").fetchall()
        table_data = [{'name': result[1],
                       'type': result[2],
                       'nullable': result[3],
                       'default_value': result[4],
                       'primary_key': result[5]} for result in results]
        conn.close()
        return table_data
    
    
@app.callback(
    Output('sql-data-container', 'children'),
    Input('sql-query-run', 'n_clicks'),
    State('sql-query-input', 'value')
)
def query_data(clicks, query):
    if clicks:
        conn = sqlite3.connect('master.db')
        cursor = conn.cursor()
        results = cursor.execute(query).fetchall()
        
        if results:
            df = DataFrame(results, columns=[desc[0] for desc in cursor.description])
            conn.close()
            output = DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'), 
                id='sql-table',
                cell_selectable=False,
                # style_table={'overflowY': 'scroll'}
            )
            return output
        else: 
            return html.P('Error')
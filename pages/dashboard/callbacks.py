from app import app
from dash import Output, Input, State, dcc, callback_context
import pandas as pd
from table import full_df, col_rules, col_names
import plotly.express as px

filter_data_states = []
for col in col_rules.keys():
    if col != 'date':
        filter_data_states.append(State('dashboard-' + col, 'value'))
    else:
        filter_data_states.append(State('dashboard-' + col + '-min-input', 'value'))
        filter_data_states.append(State('dashboard-' + col + '-max-input', 'value'))

@app.callback(
    Output('dashboard-filterpanel-container', 'className'),
    Input('filterpanel-toggle-btn', 'n_clicks'),
    State('dashboard-filterpanel-container', 'className'),
    prevent_initial_call=True
)
def toggle_filterpanel(clicks, class_name):
    return "collapsed" if class_name == "toggled" else "toggled"

@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Input('dashboard-apply-filters-button', 'n_clicks'),
    filter_data_states
)
def update_graphs(*args):
    ctx = callback_context
    query_parts = []
    
    for k,v in ctx.states.items():
        cid_parts = k.split('.')[0].split('-')
        col = '-'.join([p for p in cid_parts if p != 'dashboard'])
        if col in col_rules.keys():
            if col_rules[col] == 'unique':
                query_parts.append(f'{col} in {v}')
            else:
                query_parts.append(f'{col} >= {v[0]} & {col} <= {v[1]}')
        else:
            if 'min-input' in col:
                query_parts.append(f'({col.split("-")[0]} >= "{v}" | `{col.split("-")[0] + "2"}` >= "{v}")')
            elif 'max-input' in col:
                query_parts.append(f'{col.split("-")[0]} <= "{v}"')
    query_str = ' & '.join(query_parts)
    df = full_df.query(query_str)
    
    fig1 = px.histogram(data_frame=df, x='market')
    return [fig1, fig1, fig1]
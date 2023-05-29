from app import app
from dash import Output, Input, State, dcc, callback_context
from dash.dash_table import DataTable
import sqlite3
import pandas as pd
from pages.filtering_page.table import full_df
from pages.filtering_page.config import col_rules, col_names



filter_data_states = []
for col in col_rules.keys():
    if col != 'date':
        filter_data_states.append(State(col, 'value'))
    else:
        filter_data_states.append(State(col + '-min-input', 'value'))
        filter_data_states.append(State(col + '-max-input', 'value'))


@app.callback(
    Output('filtering-table', 'data'),
    Input('apply-filters-button', 'n_clicks'),
    filter_data_states,
    prevent_initial_call=True
)
def filter_data(*args):
    ctx = callback_context
    query_parts = []
    for k,v in ctx.states.items():
        col = k.split('.')[0]
        if col in col_rules.keys():
            if col_rules[col] == 'unique':
                query_parts.append(f'{col_names[col]} in {v}')
            else:
                query_parts.append(f'{col_names[col]} >= {v[0]} & {col_names[col]} <= {v[1]}')
        else:
            if 'min-input' in col:
                query_parts.append(f'({col_names[col.split("-")[0]]} >= "{v}" | `{col_names[col.split("-")[0] + "2"]}` >= "{v}")')
            elif 'max-input' in col:
                query_parts.append(f'{col_names[col.split("-")[0]]} <= "{v}"')
    query_str = ' & '.join(query_parts)
    df = full_df.query(query_str)
    return df.to_dict('records')
 
       
@app.callback(
   Output('filtering-table', 'hidden_columns'),
   Input('columns-list-checklist', 'value'),
   State('filtering-table', 'columns')
)
def update_columns(selected_columns, table_columns):
    columns = [col['name'] for col in table_columns]
    hidden_columns = list(set(columns) - set(selected_columns))
    return hidden_columns


@app.callback(
    Output('filterpanel-container', 'className'),
    Input('filterpanel-toggle-btn', 'n_clicks'),
    State('filterpanel-container', 'className'),
    prevent_initial_call=True
)
def toggle_filterpanel(clicks, class_name):
    return "collapsed" if class_name == "toggled" else "toggled"


@app.callback(
    Output('columns-list-div', 'style'),
    Input('columns-list-button', 'n_clicks'),
    State('columns-list-div', 'style'),
    prevent_initial_call=True
)
def toggle_columns_list(clicks, style):
    return {'display': 'block'} if style == {'display':"none"} else {'display':"none"}


@app.callback(
    Output('download-dataframe-excel', 'data'),
    Input('filtering-download-table', 'n_clicks'),
    State('filtering-table', 'data'),
    prevent_initial_call=True
)
def download_data(clicks, data):
    return dcc.send_data_frame(pd.DataFrame(data).to_csv, "output.csv")


def checklists_sync(component_id):
    @app.callback(
        Output(component_id, 'value'),
        Output(component_id + '-all-value', 'value'),
        Input(component_id, 'value'),
        Input(component_id + '-all-value', 'value'),
        State(component_id, 'value'),
        State(component_id, 'options'),
        prevent_initial_call=True
    )
    def checkbox_sync_callback(listed_val, all_val, state_val, options):
        ctx = callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        trigger_options = [d['value'] for d in ctx.states[f'{component_id}.options']]
        if trigger_id.endswith("all-value"):
            all_value = ctx.triggered[0]['value']
            checklist_vals = trigger_options if all_value else []
        else:
            checklist_vals = ctx.triggered[0]['value']
            all_value = ['Все'] if set(checklist_vals) == set(trigger_options) else []
        return checklist_vals, all_value
    
def intervals_sync(component_id):
    @app.callback(
        Output(component_id, 'value'),
        Output(component_id + '-min-input', 'value'),
        Output(component_id + '-max-input', 'value'),
        Input(component_id, 'value'),
        Input(component_id + '-min-input', 'value'),
        Input(component_id + '-max-input', 'value'),
        State(component_id + '-min-input', 'value'),
        State(component_id + '-max-input', 'value'),
        prevent_initial_call=True
    )
    def interval_sync_callback(*args):
        ctx = callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id.endswith("input"):
            if 'min' in trigger_id:
                min_value = ctx.triggered[0]['value']
                max_value = ctx.states[component_id + '-max-input.value']
            else:
                max_value = ctx.triggered[0]['value']
                min_value = ctx.states[component_id + '-min-input.value']
            range_values = [min_value, max_value]
        else:
            range_values = ctx.triggered[0]['value']
            min_value = range_values[0]
            max_value = range_values[1]
        return range_values, min_value, max_value

for k, v in col_rules.items():
    if v == 'unique':
        checklists_sync(k)
    elif v == 'minmax' and k != 'date':
        intervals_sync(k)
        
checklists_sync('columns-list-checklist')
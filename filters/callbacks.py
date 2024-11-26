from app import app
from dash import Output, Input, State, callback_context, MATCH, ALL, exceptions
from funcs import get_conn
from common_components import accordion
import re
import pandas as pd

@app.callback(
    Output('filters-store', 'data'),
    Input('filters-store', 'modified_timestamp')
)
def update_filters_config(*args):
    conn, cur = get_conn()

    cur.execute(
        '''
            SELECT *
            FROM public.filters
            ORDER BY filter_order
        '''
    )

    output = {
        'columns': [desc[0] for desc in cur.description],
        'data': cur.fetchall()
    }

    conn.close()
    cur.close()

    return output


@app.callback(
    Output({'type': 'card-body', 'index': 'filters'}, 'children'),
    Input('filters-store', 'data')
)
def reset_filters(filters_store):
    return accordion(config=pd.DataFrame(**filters_store))

@app.callback(
    Output({'type': 'checklist', 'index': MATCH}, 'value'),
    Output({'type': 'checklist-all-value', 'index': MATCH}, 'value'),
    Input({'type': 'checklist', 'index': MATCH}, 'value'),
    Input({'type': 'checklist-all-value', 'index': MATCH}, 'value'),
    State({'type': 'checklist', 'index': MATCH}, 'options'),
    prevent_initial_call=True
)
def checkbox_sync_callback(checklist_values, all_value, checklist_options):
    triggered_id = callback_context.triggered_id
    checklist_available_values = [i['value'] for i in checklist_options]

    if triggered_id['type'] == 'checklist-all-value':
        checklist_values = checklist_available_values if all_value else []
    else:
        all_value = ['Все'] if set(checklist_values) == set(checklist_available_values) else []

    return checklist_values, all_value

@app.callback(
    Output({'type': 'interval-min-input', 'index': MATCH}, 'value'),
    Output({'type': 'interval-max-input', 'index': MATCH}, 'value'),
    Output({'type': 'interval-slider', 'index': MATCH}, 'value'),
    Input({'type': 'interval-min-input', 'index': MATCH}, 'value'),
    Input({'type': 'interval-max-input', 'index': MATCH}, 'value'),
    Input({'type': 'interval-slider', 'index': MATCH}, 'value'),
    State({'type': 'interval-slider', 'index': MATCH}, 'min'),
    State({'type': 'interval-slider', 'index': MATCH}, 'max'),
    prevent_initial_call=True
)
def interval_sync_callback(min_input, max_input, slider, min_value, max_value):
    triggered_id = callback_context.triggered_id
        
    if triggered_id['type'] == 'interval-min-input':
        slider[0] = max(min_input, min_value)
    elif triggered_id['type'] == 'interval-max-input':
        slider[1] = min(max_input, max_value)

    return slider[0], slider[1], slider


@app.callback(
    Output('where-statement-store', 'data'),
    Input({'type': 'interval-slider', 'index': ALL}, 'value'),
    Input({'type': 'checklist-exclude', 'index': ALL,}, 'value'),
    Input({'type': 'checklist', 'index': ALL}, 'value'),
    Input({'type': 'checklist-all-value', 'index': ALL}, 'value'),
    Input({'type': 'min-input', 'index': ALL}, 'value'),
    Input({'type': 'max-input', 'index': ALL}, 'value'),
    State('filters-store', 'data')
)
def where_statement_store(*args):
    if not callback_context.states['filters-store.data']:
        raise exceptions.PreventUpdate
    
    config = pd.DataFrame(**callback_context.states['filters-store.data'])

    modified_inputs = {}
    for component, value in callback_context.inputs.items():
        component_type = re.search(r'"type":"(.*?)"', component).group(1)
        component_index = re.search(r'"index":"(.*?)"', component).group(1)
        if component_index not in modified_inputs.keys():
            modified_inputs[component_index] = {component_type: value}
        else:
            modified_inputs[component_index][component_type] = value

    filters = []

    for col, param in modified_inputs.items():
        column = config.query(f"title_ru == '{col}'")['target_sales_column'].values[0]

        for filter_type, filter_value in param.items():
            if filter_type == 'checklist' and param['checklist-all-value'] != ['Все']:
                if len(filter_value) == 0:
                    filter_statement = f'{column} = -1'

                else:
                    existent_vals = [str(i) for i in filter_value if i]

                    parts = []

                    if len(existent_vals) > 0:
                        parts.append(f"{column} in ({', '.join(existent_vals)})")

                    if None in filter_value:
                        parts.append(f'{column} is null')

                    if len(parts) == 2:
                        filter_statement = f'({parts[0]} or {parts[1]})'
                    else:
                        filter_statement = parts[0]

                filters.append(filter_statement)

            elif filter_type == 'interval-slider':
                statement = f'{column} BETWEEN {filter_value[0]} AND {filter_value[1]}'

                if len(param['checklist-exclude']) > 0:
                    filters.append(statement)
                else:
                    filters.append(f'({statement} OR {column} IS NULL)')

            elif filter_type == 'min-input':
                filter_value = f"'{filter_value}'"
                filters.append(f'{column} >= {filter_value}')

            elif filter_type == 'max-input':
                filter_value = f"'{filter_value}'"
                filters.append(f'{column} <= {filter_value}')

    return ' AND '.join(filters)
        
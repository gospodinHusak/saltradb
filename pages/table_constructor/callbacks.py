from app import app
import pandas as pd
from dash import (
    Output, Input, State, dcc, callback_context, 
    html, ALL, MATCH, exceptions
)
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from funcs import get_conn, get_data
import re
from datetime import datetime
import io
from common_components import (
        add_row_button, field_row, metric_row, grouping_attr_row, order_row
    )

def reset_card(id:str, row_type, add_row_button_title:str, required_text:str=None, cols:list=None):
    initial_row = row_type(num=0) if not cols else row_type(num=0, cols=cols)

    container = []
    if required_text:
        container = [html.Div(id=f'{id}-required', children=required_text, style={'display':'none'})]
    
    return container + [
        dbc.Container(
            id={
                'type': 'container',
                'index': id
            },
            children=[initial_row],
            style={'padding': '0px'}
        ),
        html.Hr(className="my-2"),
        add_row_button(title=add_row_button_title, id=f'add-{id}-button')
    ]

@app.callback(
    Output('view-columns-store', 'data'),
    Input('view-columns-store', 'modified_timestamp')
)
def update_cols(*args):
    conn, cur = get_conn()

    cur.execute(
        '''
            SELECT
                column_name
            FROM information_schema.columns
            WHERE
                table_name = 'all_data'
        '''
    )

    cols = [i[0] for i in cur.fetchall()]

    conn.close()
    cur.close()
    return cols

@app.callback(
    Output({'type': 'card', 'index': 'fields'}, 'style'),
    Output({'type': 'card', 'index': 'grouping-attributes'}, 'style'),
    Output({'type': 'card', 'index': 'metrics'}, 'style'),
    Input('query-type', 'value')
)
def fill_cols_config(qt):
    if qt == 'raw':
        return {}, {'display': 'none'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {}, {}

@app.callback(
    Output({'type': 'card-body', 'index': MATCH}, 'style'),
    Output({'type': 'eye-button', 'index': MATCH}, 'children'),
    Input({'type': 'eye-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'card-body', 'index': MATCH}, 'style'),
    prevent_initial_call=True
)
def hide_show_cardbody(clicks, style):
    if style:
        return {}, DashIconify(icon="bi:eye-fill", width=24)
    else:
        return {'display': 'none'}, DashIconify(icon="bi:eye-slash-fill", width=24)
    
@app.callback(
    Output('cards-col', 'style'),
    Output('config-panel-arrow', 'icon'),
    Output('config-panel-text', 'children'),
    Output('loading-spinner', 'className'),
    Input('config-panel', 'n_clicks'),
    State('config-panel-arrow', 'icon'),
    prevent_initial_call=True
)
def hide_show_config_panel(clicks, icon):
    close_icon = 'material-symbols-light:stat-minus-1'
    open_icon = 'material-symbols-light:stat-1'
    display_style = {
        'width': '400px',
        'height':'calc(100vh - 85px)',
        'overflow-y': 'auto'
    }

    if icon == open_icon:
        return {'display': 'none'}, close_icon, 'Открыть конфигурационную панель', 'config-hidden'
    else:
        return display_style, open_icon, 'Скрыть конфигурационную панель', 'config-visible'
    
@app.callback(
    Output({'type': 'card-body', 'index': 'proccessing-type'}, 'children'),
    Input({'type': 'card', 'index': 'proccessing-type'}, 'children')
)
def proccessing_type(inp):
    return dbc.RadioItems(
        options=[
            {"label": "Первичные данные", "value": "raw"},
            {"label": "Агрегированные данные", "value": "agg"}
        ],
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-primary",
        labelCheckedClassName="active",
        value="raw",
        id="query-type"
    )

@app.callback(
    Output({'type': 'card-body', 'index': 'fields'}, 'children'),
    Input('view-columns-store', 'data'),
    Input('query-type', 'value')
)
def reset_fields(cols, qt):
    return reset_card(
        id='fields',
        row_type=field_row, 
        add_row_button_title='Добавить поле',
        required_text='Добавьте минимум одно поле!',
        cols=cols
    )

@app.callback(
    Output({'type': 'card-body', 'index': 'grouping-attributes'}, 'children'),
    Input('view-columns-store', 'data'),
    Input('query-type', 'value')
)
def reset_groupby(cols, qt):
    return reset_card(
        id='grouping-attributes',
        row_type=grouping_attr_row, 
        add_row_button_title='Добавить поле для группировки',
        cols=cols,
    )

@app.callback(
    Output({'type': 'card-body', 'index': 'metrics'}, 'children'),
    Input('view-columns-store', 'data'),
    Input('query-type', 'value')
)
def reset_metrics(cols, qt):
    return reset_card(
        id='metrics',
        row_type=metric_row, 
        add_row_button_title='Добавить метрику',
        required_text='Добавьте минимум одну метрику!',
        cols=cols,
    )

@app.callback(
    Output({'type': 'card-body', 'index': 'order'}, 'children'),
    Input('query-type', 'value')
)
def reset_orders(value):
    return reset_card(
        id='orders',
        row_type=order_row, 
        add_row_button_title='Добавить поле для сортировки',
    )


def transform_rows(card_id, func, method_dropdown=False, use_cols=True):
    @app.callback(
        Output({'type':'container', 'index': card_id}, 'children'),
        Input(f'add-{card_id}-button', 'n_clicks'),
        Input({'type': f'delete-{card_id}-row-button', 'index': ALL}, 'n_clicks'),
        State({'type':'container', 'index': f'{card_id}'}, 'children'),
        State('view-columns-store', 'data'),
        prevent_initial_call=True
    )
    def transform_grouping_attributes(*args):
        ctx = callback_context
        container = ctx.states['{"index":"' + card_id +'","type":"container"}.children']

        ids = [row['props']['id']['index'] for row in container]
        column_values = [row['props']['children'][0]['props']['value'] for row in container]
        if method_dropdown:
            method_values = [row['props']['children'][1]['props']['value'] for row in container]

        if ctx.triggered_id == f'add-{card_id}-button':
            if use_cols:
                cols = ctx.states['view-columns-store.data']

            current_rows = []
            for i in range(len(container)):
                args = dict(num=ids[i], column_value=column_values[i])
                
                if method_dropdown:
                    args['method_value'] = method_values[i]
                if use_cols:
                    args['cols'] = cols
                
                current_rows.append(func(**args))

            args = dict(num=ctx.inputs[f'add-{card_id}-button.n_clicks'])
            if use_cols:
                args['cols'] = cols
            new_row = [
                func(**args)
            ]
            return current_rows + new_row
        else:
            i = 0
            while True:
                if container[i]['props']['id']['index'] == ctx.triggered_id['index']:
                    del container[i]
                    break
                i += 1
            return container


transforming_cards = {
        'grouping-attributes': {
            'func': grouping_attr_row, 
            'method_dropdown': False,
            'use_cols': True
        }, 
        'fields': {
            'func': field_row, 
            'method_dropdown': False,
            'use_cols': True
        }, 
        'metrics': {
            'func': metric_row, 
            'method_dropdown': True,
            'use_cols': True
        }, 
        'orders': {
            'func': order_row, 
            'method_dropdown': True,
            'use_cols': False
        }
    }    

for card_id, config in transforming_cards.items():
    transform_rows(
        card_id=card_id,
        func=config['func'],
        method_dropdown=config['method_dropdown'],
        use_cols=config['use_cols']
    )           
    
@app.callback(
    Output({'type': 'orders-dropdown', 'index': ALL}, 'options'),
    Input({'type': 'grouping-attributes-dropdown', 'index': ALL}, 'value'),
    Input({'type': 'metrics-dropdown', 'index': ALL}, 'value'),
    Input({'type': 'fields-dropdown', 'index': ALL}, 'value'),
    State('query-type', 'value'),
    State({'type': 'grouping-attributes-dropdown', 'index': ALL}, 'value'),
    State({'type': 'metrics-dropdown', 'index': ALL}, 'value'),
    State({'type': 'fields-dropdown', 'index': ALL}, 'value'),
    State({'type': 'orders-dropdown', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def update_orders(*args):
    ctx = callback_context
    states = ctx.states
    qt = states['query-type.value']
    del states['query-type.value']

    active_vals = []
    ordering_attrs = len([key for key in states.keys() if 'orders-dropdown' in key])


    for key, value in states.items():
        if qt == 'raw':
            if 'fields-dropdown' in key and value:
                active_vals.append(value)
        else:
            if ('grouping-attributes-dropdown' in key or 'metrics-dropdown' in key) and value:
                active_vals.append(value)

    active_vals = list(set(active_vals))

    return [
        [
            {'label': val,'value': val} 
            for val in active_vals
        ] 
        for i in range(ordering_attrs)
    ]

@app.callback(
    Output({'type': 'orders-direction-dropdown','index': MATCH}, 'value'),
    Input({'type': 'orders-dropdown','index': MATCH}, 'value'),
    State({'type': 'orders-direction-dropdown','index': MATCH}, 'value'),
    prevent_initial_call=True
)
def default_direction(order_by_value, current_direction):
    return 'ASC' if not current_direction else current_direction

@app.callback(
    Output('fields-required', 'style'),
    Input({'type': 'container','index': 'fields'}, 'children'),
    prevent_initial_call=True
)
def show_hide_fields_required_alert(children):
    return {'display':'none'} if len(children) > 0 else {'color':'red'}

@app.callback(
    Output('metrics-required', 'style'),
    Input({'type': 'container','index': 'metrics'}, 'children'),
    prevent_initial_call=True
)
def show_hide_metrics_required_alert(children):
    return {'display':'none'} if len(children) > 0 else {'color':'red'}

@app.callback(
    Output({'type': 'fields-dropdown', 'index': MATCH}, 'className'),
    Input({'type': 'fields-dropdown', 'index': MATCH}, 'value'),
    prevent_initial_call=True
)
def change_fields_dropdown_border_color(value):
    return 'required' if not value else ''

@app.callback(
    Output({'type': 'metrics-dropdown', 'index': MATCH}, 'className'),
    Input({'type': 'metrics-dropdown', 'index': MATCH}, 'value'),
    prevent_initial_call=True
)
def change_metrics_dropdown_border_color(value):
    return 'required' if not value else ''

@app.callback(
    Output({'type': 'metrics-aggtype-dropdown', 'index': MATCH}, 'className'),
    Input({'type': 'metrics-aggtype-dropdown', 'index': MATCH}, 'value'),
    prevent_initial_call=True
)
def change_metrics_aggtype_dropdown_border_color(value):
    return 'required' if not value else ''

@app.callback(
    Output('run-query-button', 'disabled'),
    Output('run-query-button', 'color'),
    Output('run-query-button', 'style'),
    Input({'type': 'metrics-dropdown', 'index': ALL}, 'value'),
    Input({'type': 'metrics-aggtype-dropdown', 'index': ALL}, 'value'), 
    Input({'type': 'fields-dropdown', 'index': ALL}, 'value'),
    State('query-type', 'value'),
    State({'type': 'metrics-dropdown', 'index': ALL}, 'value'),
    State({'type': 'metrics-aggtype-dropdown', 'index': ALL}, 'value'), 
    State({'type': 'fields-dropdown', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def enable_disable_run_query_button(*args):
    ctx = callback_context
    states = ctx.states

    query_type = states['query-type.value']
    del states['query-type.value']

    modified_states = {}
    for key, value in states.items():
        component_type = re.search(r'"type":"(.*?)"', key).group(1)
        component_index = int(re.search(r'"index":(\d+)', key).group(1))
        if component_type not in modified_states.keys():
            modified_states[component_type] = {component_index: value}
        else:
            modified_states[component_type][component_index] = value

    if query_type == 'raw':
        if 'fields-dropdown' not in modified_states.keys():
            return True, 'warning', {'border-color': 'rgba(197, 127, 14, .5)'}
        
        if len([value for value in modified_states['fields-dropdown'].values() if not value]) > 0:
            return True, 'warning', {'border-color': 'rgba(197, 127, 14, .5)'}
        
    else:
        if 'metrics-dropdown' not in modified_states.keys():
            return True, 'warning', {'border-color': 'rgba(197, 127, 14, .5)'} 
        
        if len(
                [
                    value 
                    for value in modified_states['metrics-dropdown'].values() 
                    if not value
                ] 
                +
                [
                    value 
                    for value in modified_states['metrics-aggtype-dropdown'].values() 
                    if not value
                ]
            ) > 0:
            return True, 'warning', {'border-color': 'rgba(197, 127, 14, .5)'}
        
    return False, 'success', {'border-color': 'rgba(93,208,185, .5)'}

@app.callback(
    Output('filtering-table-container', 'children'),
    Output('retrieved-data','data'),
    Input('run-query-button', 'n_clicks'),
    State('query-type', 'value'),
    State({'type': 'grouping-attributes-dropdown', 'index': ALL}, 'value'),
    State({'type': 'metrics-dropdown', 'index': ALL}, 'value'),
    State({'type': 'metrics-aggtype-dropdown', 'index': ALL}, 'value'), 
    State({'type': 'fields-dropdown', 'index': ALL}, 'value'),
    State({'type': 'orders-dropdown', 'index': ALL}, 'value'),
    State({'type': 'orders-direction-dropdown', 'index': ALL}, 'value'),
    State('where-statement-store', 'data'),
    State('retrieved-data','data'),
    running=[
        (Output("run-query-button", "disabled"), True, False),
        (Output("excel-button", "disabled"), True, False),
        (Output("csv-button", "disabled"), True, False),
        (Output("download-button", "disabled"), True, False),
        (Output('loading-spinner', 'style'), {'display':'flex'}, {'display':'none'})
    ],
    prevent_initial_call=True
)
def produce_table(*args):
    ctx = callback_context
    
    states = ctx.states
    
    last_query = ''
    if states['retrieved-data.data']:
        if 'query' in states['retrieved-data.data'].keys(): 
            last_query = states['retrieved-data.data']['query']

    query_type = states['query-type.value']
    where_statement = bytes(states['where-statement-store.data'], "utf-8").decode("unicode_escape")
    del states['query-type.value']
    del states['where-statement-store.data']
    del states['retrieved-data.data'] 

    modified_states = {}
    for key, value in states.items():
        component_type = re.search(r'"type":"(.*?)"', key).group(1)
        component_index = int(re.search(r'"index":(\d+)', key).group(1))
        if component_type not in modified_states.keys():
            modified_states[component_type] = {component_index: value}
        else:
            modified_states[component_type][component_index] = value

    order_by_columns_str = ''
    if 'orders-dropdown' in modified_states.keys():
        order_by_columns_str = ', '.join(
            [
                f'"{modified_states['orders-dropdown'][key]}" {modified_states['orders-direction-dropdown'][key]}'
                for key in modified_states['orders-dropdown'].keys()
                if modified_states['orders-dropdown'][key] is not None
            ]
        )

    order_by_statement = f'ORDER BY {order_by_columns_str}' if len(order_by_columns_str) > 0 else ''

    if query_type == 'raw':
        select_columns_str = ', '.join(
            [
                f'"{column}"' 
                for column in modified_states['fields-dropdown'].values()
            ]
        )

        query = f'''
            SELECT {select_columns_str}
            FROM all_data
            WHERE "ID" IN (
                SELECT id
                FROM sales
                WHERE {where_statement}
            )
            {order_by_statement}
        '''
    
    else:
        metrics_columns = []
        for key in modified_states['metrics-dropdown'].keys():
            agg = modified_states['metrics-aggtype-dropdown'][key]
            col = modified_states['metrics-dropdown'][key]
            metric_agg = f'{agg}("{col}")'
            metric_name = f'{col} ({agg})'
            if col in order_by_statement:
                order_by_statement = order_by_statement.replace(col, metric_name)
            metrics_columns.append(f'{metric_agg} as "{metric_name}"')

        metrics_columns_str = ', '.join(metrics_columns)

        group_by_columns_str = ''

        if 'grouping-attributes-dropdown' in modified_states.keys():
            group_by_columns_str = ', '.join(
                [
                    f'"{column}"' 
                    for column in modified_states['grouping-attributes-dropdown'].values()
                    if column
                ]
            )

        if len(group_by_columns_str) > 0:
            select_columns_str = f'{group_by_columns_str}, {metrics_columns_str}'
            group_by_statement = f'GROUP BY {group_by_columns_str}'
        else:
            select_columns_str = metrics_columns_str
            group_by_statement = ''
        
        query = f'''
            SELECT {select_columns_str}
            FROM all_data
            WHERE "ID" IN (
                SELECT id
                FROM sales
                WHERE {where_statement}
            )
            {group_by_statement}
            {order_by_statement}
        '''

    if query == last_query:
        raise exceptions.PreventUpdate
    
    print(query)

    df = get_data(query)

    table_header = [
        html.Thead(
            html.Tr(
                [html.Th(i) for i in df.columns]
            ),
            style={
                'position': 'sticky',
                'top': '0',
            }
        )
    ]

    table_body = [
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(str(r[c])) for c in df.columns
                    ]
                ) 
                for r in df.to_dict('records')
            ]
        )
    ]

    return [
        dbc.Table(
            table_header + table_body, 
            id='filtering-table', 
            bordered=True,
        ),
        {
            'query': query,
            'records': df.to_dict('records')
        }
    ]

@app.callback(
    Output('download-data', 'data'),
    Input('excel-button', 'n_clicks'),
    Input('csv-button', 'n_clicks'),
    State('retrieved-data', 'data'),
    State('file-name-input', 'value'),
    prevent_initial_call=True
)
def download_data(excel_button, csv_button, data, fname):
    fname = f'output_{datetime.now()}' if not fname else fname
    df = pd.DataFrame.from_dict(data['records'])

    if callback_context.triggered_id.split('-')[0] == 'csv':
        return dcc.send_data_frame(
            df.to_csv, 
            f"{fname}.csv", 
            index=False, 
            encoding='utf-8'
        )
    else:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet_name_1', index=False)
        return dcc.send_bytes(output.getvalue(), f'{fname}.xlsx')

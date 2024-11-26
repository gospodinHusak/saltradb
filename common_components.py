import dash_bootstrap_components as dbc
from dash import dcc, html
from funcs import get_conn
from math import ceil, floor
from dash_iconify import DashIconify


def checklist(cur, vw_name, title) -> dbc.AccordionItem:
    cur.execute(f'SELECT * FROM {vw_name}')

    data = cur.fetchall()

    all_value_item = dbc.Checklist(
        id={
            'index': title,
            'type' : f'checklist-all-value'
        },
        options=[{"label": "Все", "value": "Все"}],
        value=['Все'],
        persistence=True,
        persistence_type="session", 
        class_name='all-value-option filter'
    )
    listed_values_item = dbc.Checklist(
        id={
            'index': title,
            'type' : f'checklist'
        },
        options=[{'label': i[0], 'value': i[1]} for i in data],
        value=[i[1] for i in data],
        persistence=True,
        persistence_type="session",
        class_name='filter'
    )
    return dbc.AccordionItem(
        children=[all_value_item, listed_values_item],
        title=title,
        class_name='checkbox'
    )

        
def interval(cur, vw_name, title) -> dbc.AccordionItem:
    cur.execute(f'SELECT * FROM {vw_name}')

    min_value, max_value = cur.fetchone()

    # min_value = floor(min_value)
    # max_value = ceil(max_value)
    min_value = 0
    max_value = max_value*100

    component = html.Div(
        [
            html.Div(
                [
                    dcc.Input(
                        id={
                            'index': title,
                            'type' : 'interval-min-input'
                        },
                        type='number',
                        value=min_value,
                        className='interval-input'
                    ),
                    dcc.RangeSlider(
                        id={
                            'index': title,
                            'type' : 'interval-slider'
                        },
                        marks=None,
                        min=min_value,
                        max=max_value,
                        value=[min_value, max_value],
                        allowCross=False,
                        updatemode='drag',
                        className='interval-slider'
                    ),
                    dcc.Input(
                        id={
                            'index': title,
                            'type' : 'interval-max-input'
                        },
                        type='number',
                        value=max_value,
                        className='interval-input'
                    ),
                ],
                className='interval-components'
            ),
            html.Div(
                dbc.Checklist(
                    id={
                        'index': title,
                        'type' : 'checklist-exclude'
                    },

                    options=[
                        {"label": "Исключить, если отсутствует значение", "value": "exclude_null"}
                    ],
                    value=[],
                    persistence=True,
                    persistence_type="session", 
                    class_name='filter'
                ),
                style={'margin-top': '2px'}
            )
        ]
    )

    return dbc.AccordionItem(
        children=component,
        title=title,
        class_name='interval'
    )

        
def date_filter(cur, vw_name, title) -> dbc.AccordionItem:
    cur.execute(f'SELECT * FROM {vw_name}')

    min_date, max_date = cur.fetchone()

    component = html.Div(
        [
            dcc.Input(
                id={
                    'index': title,
                    'type' : 'min-input'
                },
                type='text',
                value=min_date,
                className='interval-input'
            ),
            ' - ',
            dcc.Input(
                id={
                    'index': title,
                    'type' : 'max-input'
                },
                type='text',
                value=max_date,
                className='interval-input'
            ),
        ],
        className='interval-components'
    )

    return dbc.AccordionItem(
        children=component,
        title=title,
        class_name='date-filter'
    )

def accordion(config):
    filter_funcs = {
        'date': date_filter,
        'checklist': checklist,
        'interval': interval
    }

    conn, cur = get_conn()

    children=[
            filter_funcs[r['filter_type']](
                cur=cur, 
                vw_name=r['view_name'], 
                title=r['title_ru']
            ) 
            for i, r in config.iterrows()
        ]
    cur.close()
    conn.close()

    return dbc.Accordion(
        children=children, 
        flush=True
    )


def eye_button(index, is_open:bool):
    return html.A(
        id={
            'type': 'eye-button',
            'index': index
        },
        children=DashIconify(
            icon='bi:eye-fill' if is_open else 'bi:eye-slash-fill', 
            width=24
        ),
        style={
            'width': '24px'
        },
        className='eye-button'
    )


def card_header(title, index, is_open=True, is_closable=True):
    div_children = [html.Div(title, style={'flex': '1'})]
    if is_closable:
        div_children.append(eye_button(index, is_open))

    return dbc.CardHeader(
        id={
            'type': 'card-header',
            'index': index
        },
        children=[
            html.Div(
                div_children,
                style={
                    'display': 'flex'
                }
            )
        ]
    )

def card_body(index, is_open=True):
    return dbc.CardBody(
        id={
            'type': 'card-body',
            'index': index
        },
        children=dbc.Row(
            dbc.Col(
                dbc.Spinner(
                    color='secondary',
                    spinner_style={
                        "width": "60px", 
                        "height": "60px",
                    }
                ),
                width='auto'
            ),
            justify="center"
        ),
        style={} if is_open else {'display': 'none'}
    )


def card(title, index, is_open=True, is_closable=True):
    return dbc.Card(
        id={
            'type': 'card',
            'index': index
        },
        children=[
            card_header(
                title=title, 
                index=index, 
                is_open=is_open,
                is_closable=is_closable
            ),
            card_body(
                index=index, 
                is_open=is_open,
            )
        ],
        color='light',
    )

def add_row_button(title, id):
    return dbc.Button(
        children=[
            html.Span(
                [
                    DashIconify(icon="material-symbols:add", width=24, style={'padding':'0','display':'inline-block'}),
                    html.Div(title, 
                style={'display':'inline-block','height':'24px', 'line-height':'24px'})
                ], 
                style={'display':'inline-block'}
            )
        ], 
        id=id,
        n_clicks=0,
        color='secondary',
        size='sm',
        style={'textAlign':'center'}
    )


def delete_row_button(id, num):
    return dbc.Button(
        DashIconify(
            icon="material-symbols:delete-outline-rounded", 
            width=34, 
            style={'padding':'0'}
        ),
        id={
            'type': f'delete-{id}-row-button',
            'index': num
        },
        outline=True,
        color='danger',
        style={'padding':'0', 'width': '36px'}
    )


def metric_row(num, cols, column_value=None, method_value=None):
    return html.Div(
        id={
            'type': 'metrics-row',
            'index': num
        },
        children=[
            dcc.Dropdown(
                id={
                    'type': 'metrics-dropdown',
                    'index': num
                },
                options=[{'label': i, 'value': i} for i in cols],
                value=column_value,
                multi=False,
                placeholder="Поле",
                className='required' if not column_value else '',
                style={
                    'flex': '2', 
                    'padding-right': '10px'
                }
            ),
            dcc.Dropdown(
                id={
                    'type': 'metrics-aggtype-dropdown',
                    'index': num
                },
                options=[
                    {"label": "sum", "value": "sum"},
                    {"label": "avg", "value": "avg"},
                    {"label": "max", "value": "max"},
                    {"label": "min", "value": "min"},
                    {"label": "count", "value": "count"},
                ],
                value=method_value,
                multi=False,
                placeholder="Метод",
                clearable=False,
                className='required' if not method_value else '',
                style={
                    'flex': '1', 
                    'padding-right': '10px'
                }
            ),
            delete_row_button(id='metrics', num=num)
        ],
        className='config-row'
    )


def order_row(num, cols=None, column_value=None, method_value=None):
    return html.Div(
        id={
            'type': 'orders-row',
            'index': num
        },
        children=[
            dcc.Dropdown(
                id={
                    'type': 'orders-dropdown',
                    'index': num
                },
                options=[{'label': i, 'value': i} for i in cols] if cols else [],
                value=column_value,
                multi=False,
                placeholder="Поле",
                style={
                    'flex': '2', 
                    'padding-right': '10px'
                }
            ),
            dcc.Dropdown(
                id={
                    'type': 'orders-direction-dropdown',
                    'index': num
                },
                options=[
                    {"label": "ASC", "value": "ASC"},
                    {"label": "DESC", "value": "DESC"},
                ],
                value=method_value,
                clearable=False,
                multi=False,
                placeholder="Порядок",
                style={
                    'flex': '1', 
                    'padding-right': '10px'
                }
            ),
            delete_row_button(id='orders', num=num)
        ],
        className='config-row'
    )


def grouping_attr_row(num, cols, column_value=None):
    return html.Div(
        id={
            'type': 'grouping-attributes-row',
            'index': num
        },
        children=[
            dcc.Dropdown(
                id={
                    'type': 'grouping-attributes-dropdown',
                    'index': num
                },
                options=[{'label': i, 'value': i} for i in cols],
                value=column_value,
                multi=False,
                placeholder="Поле",
                style={
                    'flex': '1', 
                    'padding-right': '10px'
                }
            ),
            delete_row_button(id='grouping-attributes', num=num)
        ],
        className='config-row'
    )


def field_row(num, cols, column_value=None):
    return html.Div(
        id={
            'type': 'fields-row',
            'index': num
        },
        children=[
            dcc.Dropdown(
                id={
                    'type': 'fields-dropdown',
                    'index': num
                },
                options=[{'label': i, 'value': i} for i in cols],
                value=column_value,
                multi=False,
                placeholder="Поле",
                className='required' if not column_value else '',
                style={
                    'flex': '1', 
                    'padding-right': '10px'
                }
            ),
            delete_row_button(id='fields', num=num)
        ],
        className='config-row'
    )
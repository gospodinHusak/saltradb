from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from common_components import card


cards_col = html.Div(
    id='cards-col',
    children=[
        card(
            title="Тип вывода данных", 
            index='proccessing-type', 
            is_open=True
        ),
        card(
            title="Поля для отображения", 
            index='fields', 
            is_open=True
        ),
        card(
            title="Поля для группировки", 
            index='grouping-attributes', 
            is_open=True,
        ),
        card(
            title="Метрики", 
            index='metrics', 
            is_open=True
        ),
        card(
            title="Фильтры", 
            index='filters', 
            is_open=False
        ),
        card(
            title="Сортировка", 
            index='order', 
            is_open=True
        )
    ],
    style={
        'width': '400px',
        'height': 'calc(100vh - 85px)',
        'overflow-y': 'auto'
    }
)

table_placeholder = html.Div(
    DashIconify(
        icon="material-symbols-light:table-sharp", 
        width=600,
        style={
            'color': 'rgba(149, 165, 166, .5)'
        }
    ),
    style={
        'margin-top': '400px',
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
    }
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("На главную", href="/")),
        html.Div(style={'borderLeft': '1px solid gray', 'height': '20px', 'margin': '10px 10px'}),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("О базе данных", href="/about-db"),
                dbc.DropdownMenuItem("Источники", href="/sources"),
                dbc.DropdownMenuItem("Визуализации", href="/charts"),
            ],
            nav=True,
            in_navbar=True,
            align_end=True,
            label="Другие страницы",
        )
    ],
    brand="Конструктор таблиц",
    color="primary",
    dark=True
)

loading_spinner = html.Div(
    id='loading-spinner',
    children=dbc.Spinner(
        spinner_style={
            'width': '20rem', 
            'height': '20rem'
        }
    ),
    style={
        'display':'none'
    },
    className='config-visible',
)


table_container = html.Div(
    id='filtering-table-container',
    children=table_placeholder, 
    style={
        'flex': '1'
    },
)

excel_button = dbc.Button(
    children=[
        '.xlsx',
        DashIconify(
            icon="mdi:file-excel-outline",
            width=30, 
            style={
                'padding':'0',
                'display':'inline-block'
            }
        )
    ],
    id='excel-button',
    n_clicks=0,
    color='dark',
    size='md',
)

csv_button = dbc.Button(
    children=[
        '.csv',
        DashIconify(
            icon="mdi:file-csv-outline",
            width=30, 
            style={
                'padding':'0',
                'display':'inline-block'
            }
        )
    ],
    id='csv-button',
    n_clicks=0,
    color='dark',
    size='md',
)

download_popover = dbc.Popover(
    id="file-download-popover",
    children=[
        dbc.PopoverHeader("Параметры скачивания"),
        dbc.PopoverBody(
            dbc.Form(
                [
                    html.Div(
                        [
                            dbc.Label("Имя файла"),
                            dbc.Input(
                                id='file-name-input',
                                placeholder='Введите имя файла'
                            ),
                            dbc.FormText(
                                'Если не введено, то генерируется автоматически'
                            ),
                        ],
                        className="mb-3"
                    ),
                    html.Div(
                        [
                            dbc.Label("Формат файла"),
                            dbc.ButtonGroup(
                                children=[excel_button, csv_button],
                                style={'border-radius':'0px'}
                            ),
                            dbc.FormText(
                                'Для скачивания файла выберите один из предложенных форматов'
                            ),
                        ],
                        style={
                            'display':'flex',
                            'flex-direction': 'column'
                        },
                        className="mb-3"
                    )
                ]
            )
        )
    ],
    trigger='legacy',
    target="download-button",
    placement='bottom',
    hide_arrow=True,
    autohide=True,
    is_open=False,
)

config_panel_button = dbc.Button(
    children=[
        html.Span(
            [
                DashIconify(
                    id='config-panel-arrow',
                    icon="material-symbols-light:stat-1",
                    width=30, 
                    style={'padding':'0','display':'inline-block'}
                ),
                html.Div(
                    id='config-panel-text',
                    children='Скрыть конфигурационную панель', 
                    style={
                        'display':'inline-block',
                        'height':'24px', 
                        'line-height':'24px'
                    }
                )
            ], 
            style={'display':'inline-block'}
        )
    ],
    id='config-panel',
    color='dark',
    class_name='panel-button',
    style={
        'width': '400px',
        'border-color': 'rgba(149, 165, 166, .5)'
    }
)

run_query_button = dbc.Button(
    children=[
        html.Span(
            [
                DashIconify(
                    icon="material-symbols-light:play-arrow",
                    width=30, 
                    style={'padding':'0','display':'inline-block'}
                ),
                html.Div(
                    'Построить таблицу', 
                    style={
                        'display':'inline-block',
                        'height':'24px', 
                        'line-height':'24px'
                    }
                )
            ], 
            style={'display':'inline-block'}
        )
    ], 
    id='run-query-button',
    n_clicks=0,
    color='warning',
    disabled=True,
    size='md',
    class_name='panel-button',
    style={'border-color': 'rgba(197, 127, 14, .5)'}
)

dowload_button = dbc.Button(
    DashIconify(
        icon="material-symbols-light:download-sharp",
        width=30, 
        style={'padding':'0','display':'inline-block'}
    ),
    id='download-button',
    n_clicks=0,
    color='dark',
    disabled=True,
    size='md',
    class_name='panel-button',
    style={
        'border-color': 'rgba(149, 165, 166, .5)',
        'margin-left': '2px',
    }
)

layout = dbc.Container(
    children=[
        dcc.Download(id="download-data"),
        dcc.Store(id='filters-store'),
        dcc.Store(id='view-columns-store'),
        dcc.Store(id='orders-options-store'),
        dcc.Store(id='where-statement-store'),
        dcc.Store(id='retrieved-data'),
        download_popover,
        loading_spinner,
        navbar,
        html.Div(
            [
                config_panel_button,
                run_query_button,
                dowload_button
            ]
        ),
        html.Div(
            [
                cards_col,
                table_container
            ],
            style={
                'display': 'flex',
                'height':'calc(100vh - 85px)'
            },
        )
    ],
    class_name='page-layout',
    fluid=True
)
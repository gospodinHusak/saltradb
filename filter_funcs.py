import dash_bootstrap_components as dbc
from dash import dcc, html


def checkbox(name, col, values) -> dbc.AccordionItem:
        all_value_item = dbc.Checklist(
            id=col + "-all-value",
            options=[{"label": "Все", "value": "Все"}],
            value=['Все'],
            persistence=True,
            persistence_type="session",
            class_name='all-value-option filter'
        )
        listed_values_item = dbc.Checklist(
            id=col,
            options=[{'label': i, 'value': i} for i in values],
            value=values,
            persistence=True,
            persistence_type="session",
            class_name='filter'
        )
        return dbc.AccordionItem(
            children=[all_value_item, listed_values_item],
            title=name,
            class_name='checkbox'
        )
        
def date_filter(name, col, values) -> dbc.AccordionItem:
    minv, maxv = values
    component = html.Div(
        [
            dcc.Input(
                id=col + f'-min-input',
                type='text',
                value=minv,
                className='interval-input'
            ),
            dcc.Input(
                id=col + f'-max-input',
                type='text',
                value=maxv,
                className='interval-input'
            ),
        ],
        className='interval-components'
    )
    return dbc.AccordionItem(
        children=component,
        title=name,
        class_name='date-filter'
    )
        
        
def interval(name, col, values) -> dbc.AccordionItem:
    minv, maxv = values
    component = html.Div(
        [
            dcc.Input(
                id=col + f'-min-input',
                type='number',
                value=minv,
                className='interval-input'
            ),
            dcc.RangeSlider(
                id=col,
                marks=None,
                min=minv,
                max=maxv,
                value=values,
                allowCross=False,
                updatemode='drag',
                className='interval-slider'
            ),
            dcc.Input(
                id=col + f'-max-input',
                type='number',
                value=maxv,
                className='interval-input'
            ),
        ],
        className='interval-components'
    )
    return dbc.AccordionItem(
        children=component,
        title=name,
        class_name='interval'
    )
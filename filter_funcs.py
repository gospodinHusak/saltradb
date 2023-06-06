import dash_bootstrap_components as dbc
from dash import dcc, html




def checkbox(name, page, col, values) -> dbc.AccordionItem:
        all_value_item = dbc.Checklist(
            id=f"{page}-{col}-all-value",
            options=[{"label": "Все", "value": "Все"}],
            value=['Все'],
            persistence=True,
            persistence_type="session",
            class_name='all-value-option filter'
        )
        listed_values_item = dbc.Checklist(
            id=f"{page}-{col}",
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
        
def date_filter(name, page, col, values) -> dbc.AccordionItem:
    minv, maxv = values
    component = html.Div(
        [
            dcc.Input(
                id=f"{page}-{col}-min-input",
                type='text',
                value=minv,
                className='interval-input'
            ),
            dcc.Input(
                id=f"{page}-{col}-max-input",
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
        
        
def interval(name, page, col, values) -> dbc.AccordionItem:
    minv, maxv = values
    component = html.Div(
        [
            dcc.Input(
                id=f"{page}-{col}-min-input",
                type='number',
                value=minv,
                className='interval-input'
            ),
            dcc.RangeSlider(
                id=f"{page}-{col}",
                marks=None,
                min=minv,
                max=maxv,
                value=values,
                allowCross=False,
                updatemode='drag',
                className='interval-slider'
            ),
            dcc.Input(
                id=f"{page}-{col}-max-input",
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
    
def create_components(rules, names, df, page):
    components = []
    for k, v in rules.items():
        if v == 'unique':
            values = df[k].unique().tolist()
            components.append(checkbox(name=names[k], page=page, col=k, values=values))
        elif v == 'minmax':
            values = df[k].sort_values().agg(['min', 'max']).tolist()
            if k == 'date':
                components.append(date_filter(name=names[k], page=page, col=k, values=values))
            else: 
                components.append(interval(name=names[k], page=page, col=k, values=values))
    return components
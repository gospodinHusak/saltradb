from app import app
from dash import Output, Input, State, dcc, callback_context
import pandas as pd
from table import full_df, col_rules, col_names
import plotly.express as px
import plotly.graph_objects as go

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
    
    trade_acts = df.groupby('market').size().reset_index(name='count').sort_values(by='count', ascending=False)
    
    # количество сделок на представленных рынках
    fig1 = px.bar(
        data_frame=trade_acts, 
        x='market',
        y='count',
        labels={
            "market": "Рынки",  "count": 'Количество сделок'
        },
        text_auto=True,
    )
    fig1.update_layout(
        hovermode=False
    )

    costs = df.groupby('market')['cost'].sum().reset_index().sort_values(by='cost', ascending=False)
    fig2 = px.bar(
        data_frame=costs, 
        x='market',
        y='cost',
        labels={
            "market": "Рынки",  "cost": 'Оборот (в ден.)'
        },
        text_auto=True,
    )
    fig2.update_layout(
        hovermode=False,
        yaxis=dict(tickformat=",.1f")
    )
    
    def new_col(date):
        year = date[:4]
        month = int(date[5:7])
        if month > 8:
            return int(year)
        else:
            return int(year)-1

    df['year'] = df['date'].apply(new_col)
    
    years = [df.year.min() + i for i in range(df.year.max() - df.year.min() + 1)]
    print(years)
    seasons = [f'{y}/{y+1}' for y in years]
    print(seasons)
    markets = sorted(df.market.unique())
    avg_prices = df.groupby(['year', 'market'])['price'].mean().reset_index().sort_values(by=['year','market'])
    avg_prices['price'] = round(avg_prices['price'], 2)
    
    fig_data = []
    for market in markets:
        trace_data = avg_prices.query(f'market == "{market}"').sort_values(by='year')
        fig_data.append(
            go.Scatter(
                x=trace_data['year'],
                y=trace_data['price'],
                # text=trace_data['price'],
                # textposition='top center',
                mode="lines+markers",
                name=market
            )
        )

    fig3=go.Figure(data=fig_data)
    
    fig3.update_layout(
        xaxis=dict(
            ticktext=seasons,
            tickvals=years
        )
    )
    
    
    
    # количество сделок на представленных рынках
    return [fig1, fig2, fig3]
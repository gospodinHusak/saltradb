from app import app
from dash import Output, Input, State, callback_context, exceptions, MATCH, ALL, dcc
import dash_bootstrap_components as dbc
import re
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from funcs import get_conn
from dash_bootstrap_templates import load_figure_template


load_figure_template(['flatly'])


def make_fig(chart_df, chart_type, x, y, color=None, title_font_size=20, 
             tick_font_size=16, chart_font_size=14):
    charts = {
        'bar': px.bar
    }

    fig = charts[chart_type](
        data_frame=chart_df, 
        x=x,
        y=y,
        color=color if color else None,
        text_auto=True,
        template='flatly',
    )

    fig.update_layout(hovermode=False)
    fig.update_traces(textfont_size=chart_font_size)
    fig.update_yaxes(
        title_font={'size': title_font_size},
        tickfont_size=tick_font_size,
        tickformat ='d'
    )
    fig.update_xaxes(
        title_font={'size': title_font_size},
        tickfont_size=tick_font_size
    )

    return fig

@app.callback(
    Output('charts-config-store', 'data'),
    Input('charts-config-store', 'modified_timestamp')
)
def update_charts_config(*args):
    conn, cur = get_conn()

    cur.execute(
        '''
            SELECT *
            FROM saltradb.charts
            WHERE to_use = 1
            ORDER BY chart_order ASC
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
    Output('chart-container', 'children'),
    Input('charts-config-store', 'data')
)
def make_graphs(charts_config):
    charts_config = pd.DataFrame(**charts_config)

    tabs = []
    for i, r in charts_config.iterrows():
        grp_select = f'"{r.x}" AS "{r.x_axis_title}"'
        agg_select = f'{r.agg_y}("{r.y}") "{r.y_axis_title}"'
        group_by = f'"{r.x_axis_title}"'

        order_by = f'{r.order_by}'

        if r.color:
            group_by = f'{group_by}, "{r.color}"'
            grp_select = f'{grp_select}, "{r.color}"'

        conn, cur = get_conn()
        
        cur.execute(
            f'''
                SELECT 
                    {grp_select}, {agg_select}
                FROM all_data
                GROUP BY {group_by}
                ORDER BY {order_by}
            '''
        )

        chart_df = pd.DataFrame(
            columns=[desc[0] for desc in cur.description],
            data=cur.fetchall()
        )

        conn.close()
        cur.close()

        fig = make_fig(
            chart_df=chart_df,
            chart_type=r.chart_type,
            x=f'{r.x_axis_title}',
            y=f'{r.y_axis_title}',
            color=f'{r.color}' if r.color else None,
            tick_font_size=r.tick_font_size,
            title_font_size=r.title_font_size,
            chart_font_size=r.chart_font_size
        )

        tabs.append(
            dbc.Tab(
                tab_id=f'tab-{r.chart_order}',
                children=dcc.Graph(
                    id={'type': 'graph', 'index': r.chart_order},
                    figure=fig,
                    style={'width': 'calc(100vw - 400px)', 'height': 'calc(100vh - 82px)'}
                ),
                label=r.chart_title
            )
        )
    return dbc.Tabs(
        id='tabs',
        children=tabs,
        active_tab='tab-1'
    )

@app.callback(
    Output({'type':'graph', 'index': ALL}, 'figure'),
    Input('apply-filters-button', 'n_clicks'),
    State('where-statement-store', 'data'),
    State('charts-config-store', 'data'),
    prevent_initial_call=True
)
def update_graphs(clicks, where_statement, charts_config):
    if not where_statement or not charts_config:
        raise exceptions.PreventUpdate

    charts_config = pd.DataFrame(**charts_config)
    where_statement = bytes(where_statement, "utf-8").decode("unicode_escape")

    figs = []
    for i, r in charts_config.iterrows():
        grp_select = f'"{r.x}" AS "{r.x_axis_title}"'
        agg_select = f'{r.agg_y}("{r.y}") "{r.y_axis_title}"'
        group_by = f'"{r.x_axis_title}"'

        order_by = f'{r.order_by}'

        if r.color:
            group_by = f'{group_by}, "{r.color}"'
            grp_select = f'{grp_select}, "{r.color}"'

        conn, cur = get_conn()

        cur.execute(
            f'''
                SELECT 
                    {grp_select}, {agg_select}
                FROM all_data
                WHERE "ID" IN (
                        SELECT id
                        FROM sales
                        WHERE {where_statement}
                    )
                GROUP BY {group_by}
                ORDER BY {order_by}
            '''
        )

        chart_df = pd.DataFrame(
            columns=[desc[0] for desc in cur.description],
            data=cur.fetchall()
        )

        conn.close()
        cur.close()

        figs.append(
            make_fig(
                chart_df=chart_df,
                chart_type=r.chart_type,
                x=f'{r.x_axis_title}',
                y=f'{r.y_axis_title}',
                color=f'{r.color}' if r.color else None,
                tick_font_size=r.tick_font_size,
                title_font_size=r.title_font_size,
                chart_font_size=r.chart_font_size
            )
        )

#     costs = df.groupby('market')['cost'].sum().reset_index().sort_values(by='cost', ascending=False)
#     fig2 = px.bar(
#         data_frame=costs, 
#         x='market',
#         y='cost',
#         labels={
#             "market": "Рынки",  "cost": 'Оборот (в ден.)'
#         },
#         text_auto=True,
#     )
#     fig2.update_layout(
#         hovermode=False,
#         yaxis=dict(tickformat=",.1f")
#     )
    
#     def new_col(date):
#         year = date[:4]
#         month = int(date[5:7])
#         if month > 8:
#             return int(year)
#         else:
#             return int(year)-1

#     df['year'] = df['date'].apply(new_col)
    
#     years = [df.year.min() + i for i in range(df.year.max() - df.year.min() + 1)]
#     seasons = [f'{y}/{y+1}' for y in years]
#     markets = sorted(df.market.unique())
#     avg_prices = df.groupby(['year', 'market'])['price'].mean().reset_index().sort_values(by=['year','market'])
#     avg_prices['price'] = round(avg_prices['price'], 2)
    
#     fig_data = []
#     for market in markets:
#         trace_data = avg_prices.query(f'market == "{market}"').sort_values(by='year')
#         fig_data.append(
#             go.Scatter(
#                 x=trace_data['year'],
#                 y=trace_data['price'],
#                 # text=trace_data['price'],
#                 # textposition='top center',
#                 mode="lines+markers",
#                 name=market
#             )
#         )

#     fig3=go.Figure(data=fig_data)
    
#     fig3.update_layout(
#         xaxis=dict(
#             ticktext=seasons,
#             tickvals=years
#         )
#     )
    return figs[0] if len(figs) == 1 else figs

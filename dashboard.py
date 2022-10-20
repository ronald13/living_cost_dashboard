import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dash_table, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from charts import create_map, make_spider, findCountryAlpha3

# read data
df = pd.read_csv('data/cost_of_living_2022.csv')
df['country_alpha_3'] = df.apply(lambda row: findCountryAlpha3(row.country) , axis = 1)
df['country_alpha_3'] = df['country_alpha_3'].replace({'Moldova':'MDA'}) # change Moldova to alpha_3 format
print(df)
# create map
map = create_map(df)


app = Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server

@app.callback(
    [Output('spider_plot', 'figure'),
    Output('country_list', 'value')],
    Input('world_map', 'selectedData'))

def update_spider(SelectedFromMap):

    if SelectedFromMap is not None:
        SelectedCountries = [piece['text'] for piece in SelectedFromMap['points']][0]
    else:
        SelectedCountries = df['country'][1]
        # MapData = MapData.loc[MapData['Nation(s) (List)'].isin(SelectedCountries)]
    spider = make_spider(df, df.loc[df['country'] == SelectedCountries].values.flatten().tolist()[2:-1])

    return spider, SelectedCountries

# @app.callback(
#     Output('world_map', 'figure'),
#     Input('country_list', 'value'))
#
# def update_map(country):
#
#     df_active = df.loc[df['country'] == country]
#     map = create_map(df_active)
#     return map

header = html.Div([
    html.Div([
        html.H1('Cost of Living in Europe'),
        html.P('Cost of living index by country, in 2022'),
        html.P('Indices are relative to New York City, value of 100. Click on a country to filter all the indeces from the right.', className='description'),
    ], className='table2x'),
    html.Div([
        html.P('All the indeces for ', style={'margin':'0 10px 0 0'}),
        dcc.Dropdown(
                id='country_list',
                options=df['country'],
                value=df['country'],
                placeholder='Choose country',
                multi=False,
                className='dropdown'
        )
    ], className='table2x', style={'display':'flex', 'align-items':'center', 'margin':0, 'justify-content':'center'})

], className='dash__header')

footer = html.Div([
    html.P('Design: Sergiu Rotaru', style={'border-right':'1px solid #000'}),
    html.P('Data Sourrce: Numbeo')

], className='dash__footer')

app.layout = html.Div([
                    header,
                    html.Div([
                        dcc.Graph(id='world_map', figure=create_map(df)),
                        dcc.Graph(id='spider_plot'),
                        # spider
                    ], className='dash__graph_block'),
                    footer

                ], className='dash__wrapper', style={})


# don't run when imported, only when standalone
if __name__ == '__main__':
    port = os.getenv("DASH_PORT", 8053)
    app.run_server(debug=True,  port=port)

import pandas as pd
import plotly.graph_objects as go
from styling import COLOR_STYLE
import pycountry


def findCountryAlpha3 (country_name):
    # convert country name to alpha_3 format
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except:
        return country_name




# WORLD MAP
def create_map(df):
    map = go.Figure()
    map.add_trace(
        go.Choropleth(
            locations=df['country_alpha_3'],
            z=df['Cost of Living Index'],
            text=df['country'],
            hovertemplate="%{text}<br>%{z}<extra></extra>",
            autocolorscale=False,
            reversescale=False,
            colorscale='plasma',
            # colorscale=COLOR_STYLE[1:], marker={'line': {'color': 'rgb(180,180,180)', 'width': 0.5}},
            colorbar={"thickness": 10,"len": 0.3,"x": 0.9,"y": 0.7,
                    'title': {"text": 'persons', "side": "bottom"},
                    'tickvals': [ 2, 10],
                    'ticktext': ['100', '100,000']}
            )
        )
    _ = map.update_traces(showscale=False)
    _ = map.update_layout(
        font_family='Open Sans',
        showlegend=False,
        dragmode=False,
        clickmode='event+select',
        margin={'t': 0, 'r': 0, 'l': 0, 'b': 0},
        geo={
            'showframe': True, 'framecolor': "#e0e0e0", 'showcoastlines': False,
            'showcountries':True, 'countrycolor': "#e0e0e0", 'landcolor':"#f3f3f3",
            'projection': {'type': "patterson"}
            },
        geo_scope='europe',
        font=dict(family="Open Sans"),
    )
    return  map



def make_spider(df, values):
    fig = go.Figure(
        go.Scatterpolar(
            r=values,
            theta=df.columns[2:-1],
            fill='toself',
            marker_color='#C0D8C0',
            hovertemplate='%{theta}' + '<br>' +
                          '<b>%{r}</b>'+
                          '<extra></extra>',
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont_size=6,
            ),
        ),
        margin={'t': 25, 'r': 45, 'l': 45, 'pad': 0},
        template='plotly_white',
        showlegend=False,
    )
    fig.update_polars(angularaxis_rotation=-30)
    return fig
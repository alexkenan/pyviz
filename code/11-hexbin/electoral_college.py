"""
Show hexbinning with Electoral College data
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import requests


df = pd.read_csv('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/elect.csv')
j_file_str = requests.get('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/geoJSONstates.json').text
j_file = json.loads(j_file_str)
df['Needed to Win'] = df['Cumulative Count'] <= 270


def binary_win(row):
    if row['Needed to Win']:
        return 1
    else:
        return 0


def hover_text(row):
    if row['Needed to Win']:
        return '{} <b>is</b> needed to win with {} electors'.format(row['State'], row['Electors'])
    else:
        return '{} <b>is not</b> needed to win with {} electors'.format(row['State'], row['Electors'])


df['Binary'] = df.apply(binary_win, axis=1)
df['Display Text'] = df.apply(hover_text, axis=1)


# Plotly Express US states needed to win
fig = px.choropleth(df, locations=df['Abbr'], locationmode="USA-states", color="Needed to Win",
                    color_discrete_sequence=['#0c68e6', '#f4f4f6'], scope="usa")
fig.update_layout(title="Electoral College Minimum States Needed to Win")
fig.show()


# Plotly GO US map with faded states that aren't needed to win
fig = go.Figure(data=go.Choropleth(locations=df['Abbr'], locationmode="USA-states",
                                   z=df['Binary'],
                                   colorscale=['#f4f4f6', '#0c68e6'],
                                   marker_line_color='white',
                                   marker_line_width=0.01,
                                   showscale=False,
                                   text=df['Display Text'],
                                   hovertemplate='%{text}',
                                   name=""))
fig.update_layout(geo_scope='usa', title="Electoral College Minimum States Needed to Win")
fig.show()

# Plotly Hexbin of US Electoral College
fig = px.choropleth_mapbox(df, geojson=j_file, color="Needed to Win",
                           color_discrete_sequence=['#0c68e6', '#dadbde'],
                           locations="State", featureidkey="properties.State",
                           center={"lat": 5.0, "lon": 10.0},  # hover_data=['State', 'Electors'],
                           zoom=4.2, hover_data={'State': True, 'Electors': True, 'Abbr': False,
                                                 'Needed to Win': False})

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                  mapbox_style="white-bg")
fig.show()

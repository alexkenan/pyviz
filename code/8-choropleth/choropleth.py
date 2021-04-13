"""
Learn choropleths with Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.renderers.default = "browser"
df = pd.read_csv('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/states.csv')


# Plotly choropleth of state populations
fig = px.choropleth(df, locations='Postal', locationmode="USA-states", scope="usa",
                    color='Population', color_continuous_scale='Blues')
fig.update_layout(title='US State Populations in 2014')
fig.show()


# Plotly GO US map with populations
def readable_pop(row):
    if row['Population'] >= 1E6:
        return '{} ({})<br>Population {:.1f}M'.format(row['State'], row['Postal'], row['Population']/1E6)
    else:
        return '{} ({})<br>Population {:.1f}K'.format(row['State'], row['Postal'], row['Population']/1E3)


df['Readable'] = df.apply(readable_pop, axis=1)
fig = go.Figure(data=go.Choropleth(locations=df['Postal'], 
                                   locationmode="USA-states",
                                   z=df['Population'],
                                   colorscale='Blues',
                                   text=df['Readable'],
                                   hovertemplate='%{text}',
                                   name=""))
fig.update_layout(geo_scope='usa', title="US State Populations in 2014")
fig.show()

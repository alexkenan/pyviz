"""
Demonstrate bar chart visualizations with Matplotlib, Seaborn, and Plotly
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats
import plotly.io as pio
pio.renderers.default = "browser"
mpg = sns.load_dataset('mpg')
plt.style.use('default')


# matplotlib scatterplot with color by origin
usa = mpg[mpg['origin'] == 'usa']
japan = mpg[mpg['origin'] == 'japan']
europe = mpg[mpg['origin'] == 'europe']
plt.scatter(usa['mpg'], usa['acceleration'],
            label="USA", color='b')
plt.scatter(japan['mpg'], japan['acceleration'],
            label="Japan", color='r')
plt.scatter(europe['mpg'], europe['acceleration'],
            label="Europe", color='k')
plt.xlabel('MPG')
plt.ylabel('Acceleration (0-60 time)')
plt.title('Acceleration (0-60 time) vs MPG')
plt.legend()
plt.show()

# seaborn scatterplot with origin/marker with color
sns.scatterplot(data=mpg, x='mpg', y='acceleration', hue='origin',
                style='origin', palette='deep')
plt.xlabel('MPG')
plt.ylabel('Acceleration (0-60 time)')
plt.title('Acceleration (0-60 time) vs MPG')
plt.show()


# plotly express with different color and size options
fig = px.scatter(mpg, x='mpg', y='acceleration', color='origin',
                 hover_data=['name', 'model_year', 'cylinders'],
                 title="Acceleration (0-60 time) vs MPG",
                 labels={"mpg": "MPG", 
                         "acceleration": "Acceleration (0-60) time"})
fig.show()


# Plotly GO scatter with different markers
usa = mpg[mpg['origin'] == 'usa']
japan = mpg[mpg['origin'] == 'japan']
europe = mpg[mpg['origin'] == 'europe']

fig = go.Figure(data=go.Scatter(x=usa['mpg'],
                                y=usa['acceleration'],
                                mode='markers',
                                marker={'color': 'blue'},
                                name="usa",
                                hovertemplate="MPG: %{x}<br>Acceleration: %{y}"))
fig.add_trace(go.Scatter(x=japan['mpg'],
                         y=japan['acceleration'],
                         mode='markers',
                         marker={'color': 'red'},
                         name="japan",
                         hovertemplate="MPG: %{x}<br>Acceleration: %{y}"))
fig.add_trace(go.Scatter(x=europe['mpg'],
                         y=europe['acceleration'],
                         mode='markers',
                         marker={'color': 'green'},
                         name="europe",
                         hovertemplate="MPG: %{x}<br>Acceleration: %{y}"))
fig.update_layout(title="Acceleration (0-60 time) vs MPG",
                  xaxis_title="MPG",
                  yaxis_title="Acceleration (0-60) time")
fig.show()

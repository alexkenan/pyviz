"""
Demonstrate basic pie chart visualizations
"""
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"
alcohol = pd.read_csv('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/alcohol.csv')
countries = alcohol[(alcohol['location'] == 'Belarus') 
                        | (alcohol['location'] == 'France')
                        | (alcohol['location'] == 'Japan')
                        | (alcohol['location'] == 'Honduras')]
plt.style.use('default')


# Matplotlib selection of countries with pct labels
plt.pie(countries['alcohol'], labels=countries['location'],
        autopct='%1.1f%%')
plt.title('Alcohol Consumption for Select Countries')
plt.show()


# Plotly Express pie customization
fig = px.pie(countries, values='alcohol', names='location',
             title="Alcohol Consumption by Select Countries")
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
    
# Plotly Graph Objects
fig = go.Figure(data=[go.Pie(labels=countries['location'],
                             values=countries['alcohol'])])
fig.update_layout(title="Alcohol Consumption by Select Countries")
fig.show()
    

# PX treemap for narrowed df
fig = px.treemap(countries, names='location',
                 values='alcohol',
                 parents=["" for _ in countries['location']])
fig.update_layout(title="Alcohol Consumption by Select Countries")
fig.show()


# PX treemap for alcohol df
fig = px.treemap(alcohol, names='location',
                 values='alcohol',
                 parents=["World" for _ in alcohol['location']])
fig.update_layout(title='Alcohol Consumption by Country')
fig.show()

"""
Demonstrate basic visualizations with Matplotlib, Seaborn, and Plotly
"""
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"
flights = sns.load_dataset("flights")
plt.style.use('default')

def create_date(row):
        return datetime.datetime.strptime('{} {}'.format(row['month'], row['year']), '%b %Y').date()

# Matplotlib linestyles
one = flights[flights['year'] == 1956]
two = flights[flights['year'] == 1957]
three = flights[flights['year'] == 1958]
four = flights[flights['year'] == 1959]
plt.plot(one['month'], one['passengers'], 'k-', label="1956")
plt.plot(two['month'], two['passengers'], 'b:', label="1957")
plt.plot(three['month'], three['passengers'], 'g--', label="1958")
plt.plot(four['month'], four['passengers'], 'r-.', label="1959")
plt.xlabel('Month')
plt.ylabel('Passengers')
plt.title('Flights')
plt.legend()
plt.show()
   
# Seaborn with fixed dates
flights['date'] = flights.apply(create_date, axis=1)
sns.lineplot(data=flights, x='date', y='passengers')
plt.title('Flights')
plt.show()
    
# Plotly Express with corrected dates
flights['date'] = flights.apply(create_date, axis=1)
fig = px.line(flights, x='date', y='passengers',
              title="Flights")
fig.show()
    
    
# Plotly Graph Objects
year1952 = flights[flights['year'] == 1952]
year1955 = flights[flights['year'] == 1955]

fig = go.Figure()
fig.add_trace(go.Scatter(x=year1952['month'],
                         y=year1952['passengers'],
                         mode='lines',
                         line={'color': '#2882BD',
                               'width': 2},
                         name="1952"))
fig.add_trace(go.Scatter(x=year1955['month'],
                         y=year1955['passengers'],
                         mode='lines',
                         line={'color': '#434343',
                               'width': 2},
                         name="1955"))
fig.update_layout(title='Flights',
                  xaxis_title="Month",
                  yaxis_title="Passengers")
fig.show()

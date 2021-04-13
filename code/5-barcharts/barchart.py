"""
Demonstrate bar chart visualizations with Matplotlib, Seaborn, and Plotly
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"
mpg = sns.load_dataset('mpg')


def h_autolabel(rects, axis) -> None:
    """
    Write data labels to the right of bars in horizontal bar charts
    :param rects: The result of calling ax.barh(), a BarContainer that is list-like
    :param axis: Typically the "ax" figure used to plot.
    :return: None
    """
    for position, rect in enumerate(rects):
        x = rect.get_width()
        y = position
        axis.annotate('{}'.format(x),
                      xy=(x, y + 0.5),
                      xytext=(9, 0),
                      textcoords="offset points",
                      ha='center', va='bottom', size=7)

def v_autolabel(rects, axis) -> None:
    """
    Write data labels to the right of bars in horizontal bar charts
    :param rects: The result of calling ax.bar(), a BarContainer that is list-like
    :param axis: Typically the "ax" figure used to plot.
    :return: None
    """
    for rect in rects:
        height = rect.get_height()
        axis.annotate('{}'.format(int(round(height, 0))),
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      xytext=(0, 3),
                      textcoords="offset points",
                      ha='center', va='bottom', size=7)


# matplotlib basic bar chart
pinto = mpg[mpg['name'] == 'ford pinto']
plt.bar(pinto['model_year'], pinto['mpg'])
plt.xlabel('Model Year')
plt.ylabel('MPG')
plt.title('Ford Pinto MPG vs Model Year')
plt.show()

# matplotlib basic horizontal bar chart
year1976 = mpg[mpg['model_year'] == 76]
year1976 = year1976.iloc[0:5]
year1976.sort_values(by='mpg', ascending=True,
                     inplace=True)
plt.barh(year1976['name'], year1976['mpg'])
plt.xlabel('MPG')
plt.title('Select Model Year 1976 Cars vs MPG')
plt.show()

# Matplotlib grouped bar chart with label at end
# if you want to avoid the default colors, you can pass your own argument
fig, ax = plt.subplots()
bar_width = 0.3
mpg_usa = mpg[mpg['origin'] == 'usa'].groupby('model_year')['mpg'].mean().reset_index()
mpg_usa['model_year'] = mpg_usa['model_year'] - bar_width
mpg_japan = mpg[mpg['origin'] == 'japan'].groupby('model_year')['mpg'].mean().reset_index()
mpg_europe = mpg[mpg['origin'] == 'europe'].groupby('model_year')['mpg'].mean().reset_index()
mpg_europe['model_year'] = mpg_europe['model_year'] + bar_width
usa = ax.bar(mpg_usa['model_year'], mpg_usa['mpg'],
             label="USA", width=bar_width)
japan = ax.bar(mpg_japan['model_year'], mpg_japan['mpg'],
               label="Japan", width=bar_width)
europe = ax.bar(mpg_europe['model_year'], mpg_europe['mpg'],
                label="Europe", width=bar_width)
ax.set_ylabel("Average MPG")
ax.set_title("Average MPG by model year and origin")
ax.legend()
ax.set_xticks(mpg_japan['model_year'])
v_autolabel(usa, ax)
v_autolabel(japan, ax)
v_autolabel(europe, ax)
plt.show()

# Plotly Express bar chart with corrected data
pinto = mpg[mpg['name'] == 'ford pinto']
pinto = pinto[pinto['cylinders'] == 4]
fig = px.bar(pinto, x='model_year', y='mpg')
fig.update_layout(title='Ford Pinto MPG vs Model Year',
                  xaxis_title="Model Year",
                  yaxis_title="MPG")
fig.show()

# Plotly Express bar chart with direct labeling
hornet = mpg[mpg['name'] == 'amc hornet']
fig = px.bar(hornet, x='model_year', y='mpg',
             text=hornet['mpg'])
fig.update_layout(title='AMC Hornet Model Year and MPG',
                  xaxis_title="Model Year",
                  yaxis_title="MPG")
fig.update_traces(textposition='outside')
fig.show()

# Advanced stacked bar chart
crashes = sns.load_dataset('car_crashes').sort_values(by='total', ascending=True)
# needed to reduce overlap of text
plt.figure(figsize=(12.0, 8.0))
plt.subplot(1, 2, 1)
sns.set_color_codes('pastel')
sns.barplot(data=crashes, x='total', y='abbrev',
            color='b', label='Total')

sns.set_color_codes('dark')
sns.barplot(data=crashes, x='speeding', y='abbrev',
            color='b', label='Speeding-involved')
plt.legend()
plt.xlabel('Car crashes per 1 billion miles')
plt.ylabel('State')
plt.title('Speeding involvement in car crashes per billion miles')

plt.subplot(1, 2, 2)
sns.set_color_codes('pastel')
sns.barplot(data=crashes, x='total', y='abbrev',
            color='b', label='Total')

sns.set_color_codes('colorblind')
sns.barplot(data=crashes, x='alcohol', y='abbrev',
            color='b', label='Alcohol-involved')

plt.xlabel('Car crashes per 1 billion miles')
plt.ylabel('State')
plt.title('Alcohol involvement in car crashes per billion miles')
sns.despine(left=True, bottom=True)
plt.legend()
#plt.savefig('crashes.png')
plt.show()

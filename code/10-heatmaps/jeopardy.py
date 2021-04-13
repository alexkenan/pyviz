"""
Make a heatmap of Jeopardy daily double locations
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
pio.renderers.default = "browser"


def jeopardy(path: str) -> dict:
    """
    Acts as a helper function to load Daily Double data
    :param path: str of path to load JSON from
    :return: dict of all_info of Jeopardy Daily Doubles
    """
    imported_dict = pd.read_json(path)
    new_dict = {"locations": {}}

    for key in imported_dict['locations'].keys():
        newkey = int(key)
        new_dict["locations"][newkey] = imported_dict['locations'][key]

    return new_dict


def fmt(input_num, *args):
    return '{:.0%}'.format(input_num)


all_info = jeopardy('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/jeopardy_dd.json')
daily = all_info["locations"]
location_array = np.array([[daily[0], daily[1], daily[2], daily[3], daily[4], daily[5]],
                           [daily[6], daily[7], daily[8], daily[9], daily[10], daily[11]],
                           [daily[12], daily[13], daily[14], daily[15], daily[16], daily[17]],
                           [daily[18], daily[19], daily[20], daily[21], daily[22], daily[23]],
                           [daily[24], daily[25], daily[26], daily[27], daily[28], daily[29]]])

# Matplotlib
y = ['$200', '$400', '$600', '$800', '$1000']
x = ['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'Cat 5', 'Cat 6']

fig, ax = plt.subplots()
im = ax.imshow(location_array, cmap='Blues')

ax.set_xticks(np.arange(len(x)))
ax.set_yticks(np.arange(len(y)))
ax.set_xticklabels(x)
ax.xaxis.tick_top()
ax.set_yticklabels(y)

for i in range(len(y)):
    for j in range(len(x)):
        if location_array[i, j]*100 >= 3.50:
            text_color = "w"
        else:
            text_color = "k"

        ax.text(j, i, '{:.2f}%'.format(location_array[i, j]*100),
                ha="center", va="center", color=text_color)

cbar = ax.figure.colorbar(im, ax=ax, format=ticker.FuncFormatter(fmt), shrink=0.85, pad=0.09)
cbar.ax.set_title("Probability (%)")

ax.set_title("Jeopardy Daily Double Location Probability\n")
fig.tight_layout()
fig.set_size_inches((8, 6))
plt.show()

# Seaborn
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(location_array, cmap="Blues", annot=True, fmt=".2%",
            yticklabels=['$200', '$400', '$600', '$800', '$1000'],
            xticklabels=['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'Cat 5', 'Cat 6'],
            cbar=True,
            cbar_kws={'format': ticker.FuncFormatter(fmt), 'label': ''})
ax.xaxis.tick_top()
ax.set_title("Jeopardy Daily Double Location Probability")
# Rotate the tick labels and set their alignment.
plt.setp(ax.get_yticklabels(), rotation=0)
fig.tight_layout()
fig.set_size_inches((8, 6))
plt.show()

# Plotly Express
x = ['<b>Cat 1</b>', '<b>Cat 2</b>', '<b>Cat 3</b>', '<b>Cat 4</b>',
     '<b>Cat 5</b>', '<b>Cat 6</b>']
y = ['<b>$200</b> ', '<b>$400</b> ', '<b>$600</b> ', '<b>$800</b> ',
                   '<b>$1000</b> ']
fig = px.imshow(location_array*100,
                labels={'x': '', 'y': '', 'color': '<b>Probability (%)</b>'},
                x=x,
                color_continuous_scale='blues')
fig.update_xaxes(side="top")
for i in range(len(y)):
    for j in range(len(x)):
        if location_array[i, j]*100 >= 3.50:
            text_color = 'white'
        else:
            text_color = 'black'

        fig.add_annotation(x=j, y=i,
                           text='{:.2f}%'.format(location_array[i, j]*100),
                           showarrow=False, align="center",
                           font={'color': text_color})

fig.update_layout(title="<b>Jeopardy Daily Double Location Probability</b>",
                  yaxis={'tickmode': 'array',
                         'tickvals': [0, 1, 2, 3, 4],
                         'ticktext': y})
fig.update_traces(hovertemplate="Probability: %{z:.2f}%", name="")
fig.show()

# Plotly Graph Objects
x = ['<b>Cat 1</b>', '<b>Cat 2</b>', '<b>Cat 3</b>', '<b>Cat 4</b>',
     '<b>Cat 5</b>', '<b>Cat 6</b>']
y = ['<b>$200</b> ', '<b>$400</b> ', '<b>$600</b> ', '<b>$800</b> ',
     '<b>$1000</b> ']
location_array = np.array(list(reversed(location_array)))
fig = go.Figure(go.Heatmap(z=location_array*100,
                           x=x,
                           colorscale='Blues',
                           hovertemplate='Probability: %{z:.2f}%',
                           colorbar={'title': '<b>Probability</b>',
                                     'tickvals': [1, 2, 3, 4, 5,
                                                  6, 7],
                                     'ticktext': ['1%', '2%', '3%',
                                                  '4%', '5%', '6%',
                                                  '7%']},
                           name=""))
fig.update_xaxes(side="top")
for i in range(len(y)):
    for j in range(len(x)):
        if location_array[i, j]*100 >= 3.50:
            text_color = 'white'
        else:
            text_color = 'black'

        fig.add_annotation(x=j, y=i,
                           text='{:.2f}%'.format(location_array[i, j]*100),
                           showarrow=False, align="center",
                           font={'color': text_color})

fig.update_layout(title="<b>Jeopardy Daily Double Location Probability</b>",
                  yaxis={'tickmode': 'array',
                         'tickvals': [4, 3, 2, 1, 0],
                         'ticktext': y})
fig.show()

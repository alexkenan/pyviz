"""
Make bump charts, slope charts, and cleveland dot plots with Matplotlib, Seaborn, and Plotly

Team rankings courtesy of Premier League
https://www.premierleague.com/tables filtered for 2018/19

Some team primary colors from
https://github.com/jalapic/engsoccerdata/blob/master/data-raw/england_club_data.csv

The Guardian predictions are from
https://www.theguardian.com/football/2019/may/15/premier-league-season-review-predicted-happened
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.io as pio
pio.renderers.default = "browser"
plt.style.use('default')

df = pd.read_csv('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/prem.csv',
                 names=['Matchweek', 'Team', 'Rank'], header=0)
preds = pd.read_csv('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/predictions.csv',
                    names=['Team', 'Actual', 'Predicted'], header=0)

orange = '#ff7f0e'  # predicted performance
blue = '#1f77b4'    # actual performance

def add_team_color(df1: pd.DataFrame) -> str:
    """
    Add the primary team color to the df
    Data courtesy https://github.com/jalapic/engsoccerdata/blob/master/data-raw/england_club_data.csv
    :return: str of the HEX color code
    """
    name = df1['Team']
    colors = {'Bournemouth': '#cc2900',
              "Crystal Palace": "#0000FF",
              'Liverpool': '#CD0206',
              'Chelsea': '#0000CC',
              'Manchester City': '#99CCFF',
              'Watford': '#cccc00',
              'Manchester United': '#FF0000',
              'Tottenham Hotspur': '#FFFFFF',
              'Everton': '#0000CC',
              'Wolverhampton Wanderers': '#EFBE29',
              'Burnley': '#99172B',
              'Southampton': '#FF0000',
              'Leicester City': '#6666ff',
              'Newcastle United': '#000000',
              'Arsenal': '#ff3333',
              'Brighton and Hove Albion': '#47a5ff',
              'Cardiff City': '#0039e6',
              'Fulham': '#FFFFFF',
              'Huddersfield Town': '#0099FF',
              'West Ham United': '#99182B'
              }

    if name in colors.keys():
        return colors[name]
    else:
        return '#000000'


df['Color'] = df.apply(add_team_color, axis=1)

# Bump chart, Matplotlib
plt.style.use('default')
for team in df['Team'].unique():
    info = df[df['Team'] == team]
    linecolor = info['Color'].unique()[0]
    plt.plot(info['Matchweek'], info['Rank'], color=linecolor, linestyle='-')
    plt.plot(info['Matchweek'], info['Rank'], color=linecolor, marker='o')
    plt.annotate(text=team, xy=(40, info['Rank'].tail(1) + 0.15), fontsize=7, color=linecolor)

plt.yticks(np.arange(0, 21, 1))
plt.xticks(np.arange(0, 39, 2))
plt.xlim(0.33, 52)
plt.ylim(0.33, 20.66)
plt.gca().invert_yaxis()
plt.gca().get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
plt.gcf().set_size_inches((9, 6))
plt.xlabel('Matchweek')
plt.title('Premier League 2018-2019 Season')
plt.gca().set_facecolor('#e6e6e6')
plt.show()

# Bump chart, Plotly
def ranking_text(df1: pd.DataFrame) -> str:
    """
    Create a ranking from a position. Turn 1 in 1st, 22 in 22nd, etc
    :param df1: pd.DataFrame which is basically each row in the actual df DataFrame
    :return: str of the "word" ranking
    """
    place = str(df1['Rank'])
    teamname = df1['Team']
    conversion_dict = {'1': 'st', '2': 'nd', '3': 'rd'}

    if place in conversion_dict.keys():
        return '{} was in {}{}'.format(teamname, place, conversion_dict[place[-1]])
    else:
        return '{} was in {}th'.format(teamname, place)


df['Place'] = df[['Rank', 'Team']].apply(ranking_text, axis=1)
size_of_dots = 14
fig = go.Figure()
for team in df['Team'].unique():
    temp_df = df[df['Team'] == team].reset_index()
    fig.add_trace(go.Scatter(x=temp_df['Matchweek'], y=temp_df['Rank'],
                             mode="lines+markers",
                             marker={'size': size_of_dots, 'color': temp_df['Color'][0]},
                             line={'color': temp_df['Color'][0]},
                             name="", showlegend=False,
                             hovertemplate='%{text} on Matchweek %{x}',
                             text=temp_df['Place']))
    fig.add_annotation(text=team, x=39, y=temp_df['Rank'].tail(1)[37], showarrow=False, xref='x',
                       xanchor='left', font={'size': 10, 'color': temp_df['Color'][0]})

fig.update_yaxes(range=[21, 0], showticklabels=False, ticks="")
fig.update_xaxes(showticklabels=True, title_text='Matchweek',
                 tickmode="array", tickvals=[val for val in range(1, 39, 1)])
fig.update_layout({'template': 'simple_white',
                   'plot_bgcolor': '#e6e6e6',
                   'title': 'Premier League 2018-2019 Season Bump Chart'},
                  hoverlabel={'bgcolor': '#F3F0EF'})
fig.show()

# Slope chart, Matplotlib
plt.style.use('default')
mw19 = df[df['Matchweek'] == 19]
mw38 = df[df['Matchweek'] == 38]
slope_data = mw19.append(mw38, ignore_index=True)

for team in slope_data['Team'].unique():
    temp_df = slope_data[slope_data['Team'] == team].reset_index()
    linecolor = temp_df['Color'][0]
    plt.plot(temp_df['Matchweek'], temp_df['Rank'], color=linecolor,
             linestyle='-')
    plt.plot(temp_df['Matchweek'], temp_df['Rank'], color=linecolor,
             marker='o')
    plt.annotate(text=team, xy=(40, temp_df['Rank'].tail(1) + 0.15), fontsize=7, color=linecolor)
plt.xlim(17, 50)
plt.ylim(0.33, 21)
plt.yticks(range(1, 21, 1))
plt.xticks([19, 38])
plt.gca().invert_yaxis()
plt.gca().get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
plt.xlabel('Matchweek')
plt.title('Premier League 2018-2019 Season')
plt.gca().set_facecolor('#e6e6e6')
plt.show()

# Slope chart, Plotly
def ranking_text(df1: pd.DataFrame) -> str:
    """
    Create a ranking from a position. Turn 1 in 1st, 22 in 22nd, etc
    :param df1: pd.DataFrame which is basically each row in the actual df DataFrame
    :return: str of the "word" ranking
    """
    place = str(df1['Rank'])
    teamname = df1['Team']
    conversion_dict = {'1': 'st', '2': 'nd', '3': 'rd'}

    if place in conversion_dict.keys():
        return '{} was in {}{}'.format(teamname, place, conversion_dict[place[-1]])
    else:
        return '{} was in {}th'.format(teamname, place)


slope_data['Place'] = slope_data[['Rank', 'Team']].apply(ranking_text, axis=1)
size_of_dots = 14
fig = go.Figure()
for team in slope_data['Team'].unique():
    temp_df = slope_data[slope_data['Team'] == team].reset_index()
    fig.add_trace(go.Scatter(x=temp_df['Matchweek'], y=temp_df['Rank'],
                             mode="lines+markers",
                             marker={'size': size_of_dots, 'color': temp_df['Color'][0]},
                             line={'color': temp_df['Color'][0]},
                             name="", showlegend=False,
                             hovertemplate='%{text} on Matchweek %{x}',
                             text=temp_df['Place']))
    fig.add_annotation(text=team, x=39, y=temp_df['Rank'].tail(1)[1], showarrow=False, xref='x',
                       xanchor='left', font={'size': 10, 'color': temp_df['Color'][0]})

fig.update_yaxes(range=[21, 0], showticklabels=False, ticks="")
fig.update_xaxes(showticklabels=True, title_text='Matchweek',
                 tickmode="array", tickvals=[19, 38])
fig.update_layout({'template': 'simple_white',
                   'plot_bgcolor': '#e6e6e6',
                   'title': 'Premier League 2018-2019 Season Slope Chart'},
                  hoverlabel={'bgcolor': '#F3F0EF'})
fig.show()


# Lollipop chart, Matplotlib
plt.style.use('default')
size_of_dots = 11
for team in preds['Team'].unique():
    temp_df = preds[preds['Team'] == team].reset_index()
    predicted = temp_df['Predicted'][0]
    actual = temp_df['Actual'][0]
    if actual != predicted:
        plt.plot([actual, predicted], [actual, actual], color='gray', linestyle='-')
        plt.plot(actual, actual, color=blue, marker='o', markersize=size_of_dots)
        plt.plot(predicted, actual, color=orange, marker='o', markersize=size_of_dots)
    else:
        plt.plot(actual, actual, color=blue, marker='o', markersize=size_of_dots)

    if actual < 10:
        plt.annotate(text=actual, xy=(actual - 0.15, actual + 0.15), fontsize=7, color='w')
    else:
        plt.annotate(text=actual, xy=(actual - 0.31, actual + 0.15), fontsize=7, color='w')

    if predicted < 10:
        plt.annotate(text=predicted, xy=(predicted - 0.15, actual + 0.15), fontsize=7, color='w')
    else:
        plt.annotate(text=predicted, xy=(predicted - 0.31, actual + 0.15), fontsize=7, color='w')

    if actual > predicted:
        toplot = actual
    elif predicted > actual:
        toplot = predicted
    else:
        toplot = actual
    plt.annotate(text=team, xy=(toplot + 1, actual + 0.15),
                 fontsize=7, color='black')
plt.gca().get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
plt.yticks(np.arange(0, 21, 1))
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=False, left=False, labelleft=False)
plt.xlim(0.33, 27)
plt.ylim(0.33, 20.66)
plt.gca().invert_yaxis()
plt.plot(27, 27, color=blue, label="Actual Performance")
plt.plot(28, 28, color=orange, label="Predicted Performance")
plt.legend()
plt.title('English Premier League 2018-2019 Cleveland Dot Plot')
plt.show()

# Lollipop chart, Plotly
size_of_dots = 18
fig = go.Figure(layout={'xaxis': {'mirror': True, 'ticks': 'outside', 'showline': True},
                        'yaxis': {'mirror': True, 'ticks': 'outside', 'showline': True}})

for team in preds['Team'].unique():
    temp_df = preds[preds['Team'] == team].reset_index()
    predicted = temp_df['Predicted'][0]
    actual = temp_df['Actual'][0]
    if predicted != actual:
        fig.add_trace(go.Scatter(x=[actual, predicted], y=[actual, actual], mode='lines',
                                 marker={'color': 'gray'}, name="", showlegend=False))
        fig.add_trace(go.Scatter(x=temp_df['Predicted'], y=temp_df['Actual'], mode='markers', name="",
                                 showlegend=False,
                                 fillcolor=orange, marker={'size': size_of_dots, 'color': orange},
                                 hovertemplate='Team: %{text}<br>Predicted: %{x}<br>Actual: %{y}',
                                 text=temp_df['Team']))
        fig.add_trace(go.Scatter(x=temp_df['Actual'], y=temp_df['Actual'], mode='markers', name="",
                                 showlegend=False,
                                 marker={'size': size_of_dots, 'color': blue}, hoverinfo='text',
                                 hovertemplate='Team: %{text}<br>Predicted: %{x}<br>Actual: %{y}',
                                 text=temp_df['Team']))
    else:
        fig.add_trace(go.Scatter(x=temp_df['Actual'], y=temp_df['Actual'], mode='markers', name="",
                                 showlegend=False,
                                 marker={'size': size_of_dots, 'color': blue},
                                 hovertemplate='Team: %{text}<br>Predicted: %{x}<br>Actual: %{y}',
                                 text=temp_df['Team']))

    if actual < 10:
        fig.add_annotation(text=str(actual), x=actual, y=actual, showarrow=False,
                           font={'size': 10, 'color': 'white'})
    else:
        fig.add_annotation(text=str(actual), x=actual, y=actual, showarrow=False,
                           font={'size': 10, 'color': 'white'})

    if predicted < 10:
        fig.add_annotation(text=str(predicted), x=predicted, y=actual, showarrow=False,
                           font={'size': 10, 'color': 'white'})
    else:
        fig.add_annotation(text=str(predicted), x=predicted, y=actual, showarrow=False,
                           font={'size': 10, 'color': 'white'})

    if actual > predicted:
        toplot = actual
    elif predicted > actual:
        toplot = predicted
    else:
        toplot = actual

    fig.add_annotation(text=team, x=toplot + 0.38, y=actual, showarrow=False, xref='x', xanchor='left',
                       font={'size': 10, 'color': 'black'})

fig.add_trace(go.Scatter(x=[27], y=[27], mode='markers', name="Actual Performance", showlegend=True,
                         marker={'size': size_of_dots, 'color': blue}))
fig.add_trace(go.Scatter(x=[28], y=[28], mode='markers', name="Predicted Performance", showlegend=True,
                         marker={'size': size_of_dots, 'color': orange}))
fig.update_yaxes(range=[21, 0], showticklabels=False, ticks="")
fig.update_xaxes(range=[0, 25], showticklabels=False, ticks="")
fig.update_layout({'template': 'simple_white',
                   'title': 'English Premier League 2018-2019 Cleveland Dot Plot'},
                  hoverlabel={'bgcolor': '#F3F0EF'})
fig.show()

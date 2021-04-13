"""
Use Matplotlib and Plotly to animate the distribution of the Birthday Problem
https://en.wikipedia.org/wiki/Birthday_problem
"""
try:
    from math import perm
except ImportError:
    from math import factorial


    def perm(n, k):
        if n > k:
            return factorial(n)/(factorial(n - k))
        else:
            return 0
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import plotly.express as px
import pandas as pd
import plotly.io as pio
pio.renderers.default = "browser"

blue = '#5e83f6'
red = '#df4728'
upper_limit = 71

def calculate_probabilities(upperlimit):
    num_people_list = []
    matches_list = []
    no_matches_list = []
    for num_people in range(2, upperlimit):
        num_people_list.append(num_people)
        start = 365.0
        prob_no_matches = perm(int(start), num_people)/start ** num_people
        prob_matches = 1.0 - prob_no_matches
        matches_list.append(round(prob_matches*100, 1))
        no_matches_list.append(round(prob_no_matches*100, 1))

    df_calcs = pd.DataFrame(data={'Number of People': num_people_list, 'Match Prob': matches_list,
                                  'No Match Prob': no_matches_list})

    return df_calcs

# Matplotlib one stacked bar
number_of_people = 23
starting_number = 365.0
prob_no_matches = 1.0
for i in range(1, number_of_people):
    prob_no_matches *= (starting_number - i)/starting_number
    # would have an off-by-one error if not for the range() behavior

prob_matches = (1.0 - prob_no_matches)*100
prob_no_matches *= 100
plt.bar(number_of_people, prob_matches, label='Match',
        color=blue)
plt.bar(number_of_people, prob_no_matches, label="No Match",
        bottom=prob_matches, color=red)
plt.xlim(number_of_people - 3, number_of_people + 3)
plt.xticks([number_of_people])
plt.ylim(0, 103)
plt.title('Birthday Problem with {} People'.format(number_of_people))
plt.xlabel('Number of People')
plt.ylabel('Percentage (%)')
plt.legend()
plt.show()

# Matplotlib all stacked stacked bar chart
df = calculate_probabilities(upper_limit)

plt.bar(df['Number of People'], df['Match Prob'], label="Match Probability", color=blue)
plt.bar(df['Number of People'], df['No Match Prob'], label="No Match Probability",
        bottom=df['Match Prob'], color=red)
plt.title('Visualizing the Birthday Problem')
plt.xlabel('Number of People')
plt.ylabel('Percentage (%)')
plt.gca().set_yticks(range(20, 120, 20))
plt.ylim(0, 120)
plt.legend()
plt.show()


# Matplotlib animation
fig, ax = plt.subplots()
df = calculate_probabilities(upper_limit)

def animate_chart(i):
    actual_i = min(i, len(df) - 1)
    ax.bar(df.iloc[actual_i]['Number of People'],
           df.iloc[actual_i]['Match Prob'], color=blue)
    ax.bar(df.iloc[actual_i]['Number of People'],
           df.iloc[actual_i]['No Match Prob'], color=red,
           bottom=df.iloc[actual_i]['Match Prob'])


# Get the labels right by plotting bars off screen with the right label and color
ax.bar(upper_limit*100 + 1, 1, color=blue,
       label="Match Probability")
ax.bar(upper_limit*100, 1, color=red,
       label="No Match Probability")

# create animation using the animate() function
myAnimation = animation.FuncAnimation(fig, animate_chart, interval=len(df), repeat=False)

plt.title('Animated Birthday Problem')
plt.xlabel("Number of People")
plt.ylabel('Probability (%)')
plt.xlim(0, upper_limit + 1)
plt.gca().set_yticks(range(20, 120, 20))
plt.ylim(0, 120)
plt.legend()
plt.show()
"""
To save a gif:
from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=30)

myAnimation.save('myAnimation.gif', writer=writer)
"""

# Plotly Express static bar chart
df = calculate_probabilities(upper_limit)
fig = px.bar(df, x="Number of People", y=["Match Prob", 'No Match Prob'],
             color_discrete_sequence=[blue, red], title="Visualizing the Birthday Problem",
             labels={'value': 'Probability (%)',
                     "Match Prob": "Match Probability",
                     'No Match Prob': "No Match Probability"})
fig.show()

# Plotly Express animation
df = calculate_probabilities(upper_limit)

# plot the data
fig = px.bar(df, x="Number of People", y=["Match Prob", 'No Match Prob'],
             color_discrete_sequence=[blue, red],
             animation_frame="Number of People", range_y=[0, 101],
             range_x=[1, upper_limit],
             title="Visualizing the Birthday Problem",
             labels={'value': 'Probability (%)',
                     "Match Prob": "Match Probability",
                     'No Match Prob': "No Match Probability"})
fig.show()

"""
Learn how to make boxplots with Matplotlib, Seaborn, and Plotly
https://catalog.data.gov/dataset/sat-results-e88d7
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.renderers.default = "browser"
df = pd.read_csv('https://raw.githubusercontent.com/alexkenan/pyviz/main/datasets/sat.csv')
df.dropna(inplace=True)
del df['Number of Test Takers']
df.rename(columns={'Critical Reading Mean': 'Reading',
                   'Mathematics Mean': 'Math',
                   'Writing Mean': 'Writing'},
          inplace=True)


# Matplotlib boxplot with customized parameters
data = [df['Reading'],
        df['Math'],
        df['Writing']]
plt.boxplot(data, notch=True, sym='+', whis=3.5)
plt.xticks(ticks=[1, 2, 3], labels=['Reading','Math', 'Writing'])
plt.title('Boxplots for NY SAT Testing')
plt.ylabel('Score')
plt.show()
'''
# Matplotlib violinplot with custom parameters
data = [df['Reading'],
        df['Math'],
        df['Writing']]
plt.violinplot(data, vert=True, showmedians=True,
               quantiles=[[0.25, 0.75], [0.25, 0.75],
                         [0.25, 0.75]],
               showextrema=False)
plt.xticks(ticks=[1, 2, 3], labels=['Reading','Math', 'Writing'])
plt.title('Violinplot for NY SAT Testing')
plt.ylabel('Score')
plt.show()

# Seaborn boxplot
sns.boxplot(data=df, orient='v', palette="Set2", 
            width=0.25)
plt.ylabel('Score')
plt.title('Boxplots for NY SAT Testing')
plt.show()

# Seaborn violinplot
sns.violinplot(data=df, orient='v', palette='Set2',
               width=0.25)
plt.title('Violinplot for NY SAT Testing')
plt.ylabel('Score')
plt.xticks(ticks=[0, 1, 2],
           labels=['Reading','Math', 'Writing'])
plt.show()

# Seaborn swarmplot
sns.swarmplot(data=df, orient='v', palette="Set2", size=3)
plt.plot([-0.33, 0.33], [df['Reading'].median(),
                         df['Reading'].median()],
         'k-')
plt.plot([0.67, 1.33], [df['Math'].mean(),
                        df['Math'].mean()],
         'k-')
plt.plot([1.67, 2.33], [df['Writing'].mean(),
                        df['Writing'].mean()],
         'k-')
plt.ylabel('Score')
plt.title('Swarmplot for NY SAT Testing')
plt.show()


# Plotly Express box plot customized
fig = px.box(df, y=["Reading", 'Math', 'Writing'],
             notched=True, 
             color=["Reading", 'Math', 'Writing'],
             labels={'variable': "", "value": 'Score'},
             title='Boxplots for NY SAT Testing',
             hover_data=['School Name'])
fig.update_traces(quartilemethod="inclusive")
fig.show()

# Plotly Express violinplot
fig = px.violin(df, y=['Reading', 'Math', 'Writing'],
                title="New York School System SAT Scores",
                points=False,
                labels={'variable': "", 'value': 'Score'})
fig.show()
    

# Plotly express more advanced swarmplot and violinplot
fig = px.violin(df, y=['Reading', 'Math', 'Writing'],
                points="suspectedoutliers", 
                labels={'variable': "", 'value': 'Score'},
                title="New York School System SAT Scores")
fig.update_traces(marker={'outliercolor': 'red'})
fig.show()
'''

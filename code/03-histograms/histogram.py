"""
Make histogram charts with Matplotlib, Seaborn, and Plotly
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"
tips = sns.load_dataset('tips')
plt.style.use('default')


# Matplotlib
plt.hist(tips['total_bill'], bins=20)
plt.xlabel('Total Bill')
plt.ylabel('Number of Bills')
plt.title('Tips Total Bill Histogram')
plt.show()

# Seaborn multiple probability function histograms
sns.displot(tips, x='total_bill', hue="sex",
            multiple="stack",
            kind="kde", fill=True)
plt.xlabel('Total Bill')
plt.ylabel('Probability')
plt.show()


# Plotly Express histogram
fig = px.histogram(tips, x='total_bill', nbins=20)
fig.update_layout(title='Tips Total Bill Histogram',
                  xaxis_title="Total Bill",
                  yaxis_title="Count")
fig.show()
 
# Plotly Graph Objects histogram
fig = go.Figure(data=[go.Histogram(x=tips['total_bill'])])
fig.update_layout(title='Tips Total Bill Histogram',
                  xaxis_title="Total Bill",
                  yaxis_title="Count")
fig.show()

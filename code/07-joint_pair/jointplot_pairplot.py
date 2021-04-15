"""
Extra charts offered by Seaborn and Plotly
"""
import matplotlib.pyplot as plt
import seaborn as sns
tips = sns.load_dataset('tips')

# Seaborn 2D density plot
sns.displot(tips, x='total_bill', y="tip")
plt.xlabel('Total Bill')
plt.ylabel('Tip')
plt.suptitle('Tips Total Bill 2D Density Plot')
plt.show()

# Seaborn contour with rug
sns.displot(tips, x='total_bill', y='tip',
            kind="kde", rug=True)
plt.suptitle('Seaborn Tips Contour Plot')
plt.show()

# Seaborn bivariate jointplot
sns.jointplot(data=tips, x='total_bill',
              y='tip', alpha=0.75)
plt.suptitle('Seaborn Tips Jointplot')
plt.show()

# Seaborn hex bivariate jointplot
sns.jointplot(data=tips, x='total_bill',
              y='tip', kind='hex')
plt.suptitle('     Seaborn Tips Hex Jointplot')
plt.show()

# Seaborn pairplot
pairplot = sns.pairplot(tips)
pairplot.savefig("tips_pairplot.png")

# or, to show the pairplot:
# plt.show()


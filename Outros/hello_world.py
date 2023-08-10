import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
    'Hello World': ['Seaborn', 'Matplotlib'],
    r'$\sigma^2$': [1.5, 2]  # LaTeX
}
df = pd.DataFrame(data)

palette = {'Seaborn': 'blue', 'Matplotlib': 'red'}
sns.barplot(x='Hello World', y=r'$\sigma^2$', data=df, palette=palette)
plt.title(r"$\theta^2$")
plt.ylabel(r"$\sigma^2$")

plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
    'Include': ['Seaborn', 'Matplotlib'],
    'e_2': [1, 2]
}

df = pd.DataFrame(data)

sns.barplot(x='Include', y='e_2', data=df)
plt.title("Hello World")
plt.show()

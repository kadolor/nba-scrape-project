import csv
import unicodedata 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
from shamscrape import knicks_master

#df.plot(x='Salary', y='Winning pct', style='o')
sns.regplot(y="Salary", x="Winning pct", data= knicks_master, fit_reg = True)
plt.show()

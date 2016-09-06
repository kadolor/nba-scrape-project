import csv
import unicodedata 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
from shamscrape import knicks_master
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import cross_val_predict
import statsmodels.api as sm
from statsmodels.formula.api import ols


lm = LinearRegression()
lr = linear_model.LinearRegression()

X = knicks_master['Salary Rank']
Y = knicks_master['Conference Rank']
"""
	This script plots New York Knicks' payroll and conference standing data.
    Copyright (C) 2016  Kelly-Ann R. Dolor

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#df.plot(x='Salary Rank', y='Conference Rank', style='o')
#sns.regplot(y="Salary Rank", x="Conference Rank", data= knicks_master, fit_reg = True)

m = ols('')

# lm.fit(X, Y)
# plt.show()


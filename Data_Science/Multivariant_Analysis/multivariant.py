import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np

df = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

df['annual_inc'] = df['Monthly.Income'].map(lambda x: x * 12)
df['int_rate'] = df['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) / 100, 4))
df['home_ownership'] = df['Home.Ownership']

annual_inc = df['annual_inc']
int_rate = df['int_rate']
home_ownership = df['home_ownership']

est1 = smf.ols(formula = 'int_rate ~ annual_inc', data=df).fit()

est2 = smf.ols(formula = 'int_rate ~ annual_inc + home_ownership', data=df).fit()

print(est1.summary())
print(est2.summary())

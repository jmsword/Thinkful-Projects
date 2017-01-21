import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv('LoanStats3b.csv', header=1, low_memory=False)

df['issue_d_format'] = pd.to_datetime(df['issue_d'])
dfts = df.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x: x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

loan_count_summary.plot()
plt.show()

#The loan_count_summary data is not stationary. To make it stationary,
#we could truncate the dataset on both ends and only use data from the
#middle portion of the graph. (not sure the proper way to express this
#or which data to remove)

sm.graphics.tsa.plot_acf(loan_count_summary)
plt.show()

sm.graphics.tsa.plot_pacf(loan_count_summary)
plt.show()

print('Yes, there are auto-correlated structures in the series, due to the fact that the series is not stationary.')
#print(loan_count_summary)
#print(df['issue_d'])

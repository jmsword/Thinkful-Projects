import pandas as pd
import statsmodels.api as sm
import numpy as np

#read in clean loan data
df = pd.read_csv('loansData_clean.csv')

#create column to highlight interest rates below 12%
df['IR_TF'] = df['Interest.Rate'] > .12

#map true/false values to 1 or 0
df['IR_TF'] = df['IR_TF'].map(lambda x: 1 if x == True else 0)

#create intercept column and set values to 1
df['Statsmodel.Intercept'] = df['Interest.Rate'].map(lambda x: 1)

#list of independent variables for logit
ind_vars = ['FICO.Score', 'Amount.Requested', 'Statsmodel.Intercept']

#find coefficient values for variables
logit = sm.Logit(df['IR_TF'], df[ind_vars])
result = logit.fit()

coeff = result.params
print(coeff)

#create variables to use in logistic function
intercept = coeff['Statsmodel.Intercept']
Loan_coeff = coeff['Amount.Requested']
FICO_coeff = coeff['FICO.Score']

#logistic function
def logistic_function(FICO, Loan, coeff):
	x = intercept + (Loan_coeff * Loan) + (FICO_coeff * FICO)
	p = 1/(1 + np.exp(x))
	return p

#Input loan amount and FICO score for logistic function
print('The probability of obtaining the loan is:')
print(logistic_function(720, 10000, coeff))
print('which is greater than 70% so the answer is YES, we will obtain the loan.')


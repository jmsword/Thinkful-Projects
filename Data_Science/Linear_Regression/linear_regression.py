import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

#Remove '%' from 'Interest.Rate' column and contert to number
loansData['Interest.Rate']=loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) / 100, 4))
#Remove 'months' from the 'Loan.Length' column
loansData['Loan.Length']=loansData['Loan.Length'].map(lambda x: int(x.rstrip('months')))
#Split 'FICO.Range' column on the '-' to make each item a list
loansData['FICO.Range']=loansData['FICO.Range'].map(lambda x: x.split('-'))
#Convert each FICO score in the list to an int
loansData['FICO.Range']=loansData['FICO.Range'].map(lambda x: [int(n) for n in x])
#Populate the column with the first number in the FICO range
loansData['FICO.Score']=[val[0] for val in loansData['FICO.Range']]

#Plot histogram
plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()

#Plot scatter matrix
plt.figure()
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()

#Extract columns for analysis
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

#Reshape series 
y = np.matrix(intrate).transpose()
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

#Combine columns to create input matrix
x = np.column_stack([x1,x2])

#Create linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

#Print P, R values
print ('P-Values: ', f.pvalues)
print ('R-Squared: ', f.rsquared)

loansData.to_csv('loansData_clean.csv', header=True, index=False)



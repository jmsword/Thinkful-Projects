import pandas as pd
df = pd.DataFrame({'bull': [.9, .15, .25],
					'bear': [.075, .8, .25],
					'stagnant':[.025, .05, .5]
					},
					index=["bull", "bear", "stagnant"])

df_1=(df.dot(df))

df_2=(df.dot(df(5)))

df_3=(df.dot(df(10)))

print(df)
print(df_1)
print(df_2)
print(df_3)

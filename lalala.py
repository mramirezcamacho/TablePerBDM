import pandas as pd

data = pd.read_csv('MX.csv')
print(data[data['BDM'] == 'jorgegarcia']
      [['Role', 'Support city', 'Vertical']])

lala = data
# lala = lala[lala['Role'] == 'Hunter']
lala = lala[lala['Support city'] == 'Mexico City']
lala = lala[lala['Vertical'] == 'SME']
lala = lala[['Role', 'Support city', 'Vertical']]
print(len(lala))

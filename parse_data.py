import pandas as pd

df = pd.read_excel('data.xlsx', sheet_name='Jahr', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20])

df.columns.values[5] = 'Ebene'

for index, row in df.iterrows():
    if pd.notna(row['Unnamed: 0']) == True:
        df.loc[index, 'Ebene'] = '1'
    if pd.notna(row['Unnamed: 1']) == True:
        df.loc[index, 'Unnamed: 0'] = row['Unnamed: 1']
        df.loc[index, 'Ebene'] = '2'
    if pd.notna(row['Unnamed: 2']) == True:
        df.loc[index, 'Unnamed: 0'] = row['Unnamed: 2']
        df.loc[index, 'Ebene'] = '3'
    if pd.notna(row['Unnamed: 3']) == True:
        df.loc[index, 'Unnamed: 0'] = row['Unnamed: 3']
        df.loc[index, 'Ebene'] = '4'
    if pd.notna(row['Unnamed: 4']) == True:
        df.loc[index, 'Unnamed: 0'] = row['Unnamed: 4']
        df.loc[index, 'Ebene'] = '5'

df.set_index(df.columns[0], inplace=True)

df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1 , inplace=True)

print(df['Ebene'].head(5)) 









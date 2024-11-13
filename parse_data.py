import pandas as pd

# Aufgabe 7a
df_year = pd.read_excel('data.xlsx', sheet_name='Jahr', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20])
df_age = pd.read_excel('data.xlsx', sheet_name='Altersklasse', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20])
df_income = pd.read_excel('data.xlsx', sheet_name='Einkommen', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20])
df_type = pd.read_excel('data.xlsx', sheet_name='Haushaltstyp', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20])

def clean_data(dataframe):
    dataframe.columns.values[5] = 'Ebene'
    dataframe['Ebene'] = dataframe['Ebene'].astype(object)
    for index, row in dataframe.iterrows():
        if pd.notna(row['Unnamed: 0']):
            dataframe.loc[index, 'Ebene'] = '1'
        if pd.notna(row['Unnamed: 1']):
            dataframe.loc[index, 'Unnamed: 0'] = row['Unnamed: 1']
            dataframe.loc[index, 'Ebene'] = '2'
        if pd.notna(row['Unnamed: 2']):
            dataframe.loc[index, 'Unnamed: 0'] = row['Unnamed: 2']
            dataframe.loc[index, 'Ebene'] = '3'
        if pd.notna(row['Unnamed: 3']):
            dataframe.loc[index, 'Unnamed: 0'] = row['Unnamed: 3']
            dataframe.loc[index, 'Ebene'] = '4'
        if pd.notna(row['Unnamed: 4']):
            dataframe.loc[index, 'Unnamed: 0'] = row['Unnamed: 4']
            dataframe.loc[index, 'Ebene'] = '5'

    dataframe.set_index(dataframe.columns[0], inplace=True)
    dataframe.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1 , inplace=True)
    return dataframe

df_year = clean_data(df_year)
df_age = clean_data(df_age)
df_income = clean_data(df_income)
df_type = clean_data(df_type)

print(df_income.head(10))












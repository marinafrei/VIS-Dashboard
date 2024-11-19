import pandas as pd
import plotly.express as px

# Aufgabe 7a
df_year_chf = pd.read_excel('data.xlsx', sheet_name='Jahr', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20], usecols='A:G,I,K,M')
#df_year_percent = pd.read_excel('data.xlsx', sheet_name='Jahr', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20], usecols='A:F,H,J,L,M')
df_age_chf = pd.read_excel('data.xlsx', sheet_name='Altersklasse', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20], usecols='A:G,I,K,M,O,Q')
#df_age_percent = pd.read_excel('data.xlsx', sheet_name='Altersklasse', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20], usecols='A:F,H,J,L,N,P,R')
df_income_chf = pd.read_excel('data.xlsx', sheet_name='Einkommen', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20], usecols='A:G,I,K,M,O')
#df_income_percent = pd.read_excel('data.xlsx', sheet_name='Einkommen', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20], usecols='A:F,H,J,L,N,P')
df_type_chf = pd.read_excel('data.xlsx', sheet_name='Haushaltstyp', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20], usecols='A:G,I,K,M,O,Q')
#df_type_percent = pd.read_excel('data.xlsx', sheet_name='Haushaltstyp', skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20], usecols= 'A:F,H,J,L,N,P,R')

#Die Zellenbeschreibungen sind nicht alle in der ersten Spalte, sondern je nach Ebene eins eingerückt.
#Dies wird hier bereinigt und damit man die Info zur Ebene nicht verliert eine zusätzliche Spalte 'Ebene' eingefügt
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

df_year_chf = clean_data(df_year_chf)
df_age_chf = clean_data(df_age_chf)
df_income_chf = clean_data(df_income_chf)
df_type_chf = clean_data(df_type_chf)


#Aufgabe 7b

column_names_chf = df_age_chf.columns.tolist()

fig = px.scatter(x=column_names_chf[1:], y=df_age_chf.loc['61: Gesundheitsausgaben'][1:])
fig.show()











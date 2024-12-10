from dash import Dash, dcc, html, Input, Output, callback, MATCH, State
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash (__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

rows_to_skip= list(range(0,13)) + [14,15,16,18,19,20] + list(range(553,583))
df_year_chf = pd.read_excel('data.xlsx', sheet_name='Jahr', skiprows=rows_to_skip, usecols='A:G,I,K,M')
df_age_chf = pd.read_excel('data.xlsx', sheet_name='Altersklasse', skiprows=rows_to_skip, usecols='A:G,I,K,M,O,Q')
df_income_chf = pd.read_excel('data.xlsx', sheet_name='Einkommen', skiprows=rows_to_skip, usecols='A:G,I,K,M,O')
df_type_chf = pd.read_excel('data.xlsx', sheet_name='Haushaltstyp', skiprows=rows_to_skip, usecols='A:G,I,K,M,O,Q')


#Die Zellenbeschreibungen sind nicht alle in der ersten Spalte, sondern pro Ebene eins eingerückt.
#Dies wird hier bereinigt und damit man die Info zur Ebene nicht verliert eine zusätzliche Spalte 'Ebene' eingefügt
def clean_data(dataframe, columnnames):
    dataframe.rename(columns={dataframe.columns[0]: 'Kategorie', dataframe.columns[5]: 'Ebene'}, inplace= True)
    dataframe['Ebene'] = dataframe['Ebene'].astype(object) #damit der datatype stimmt
    for index, row in dataframe.iterrows():
        if pd.notna(row['Kategorie']):
            if row['Kategorie'] == 'Bruttoeinkommen':
                dataframe.loc[index, 'Ebene'] = '0'
            else:
                dataframe.loc[index, 'Ebene'] = '1'
        if pd.notna(row['Unnamed: 1']):
            dataframe.loc[index, 'Kategorie'] = row['Unnamed: 1']
            dataframe.loc[index, 'Ebene'] = '2'
        if pd.notna(row['Unnamed: 2']):
            dataframe.loc[index, 'Kategorie'] = row['Unnamed: 2']
            dataframe.loc[index, 'Ebene'] = '3'
        if pd.notna(row['Unnamed: 3']):
            dataframe.loc[index, 'Kategorie'] = row['Unnamed: 3']
            dataframe.loc[index, 'Ebene'] = '4'
        if pd.notna(row['Unnamed: 4']):
            dataframe.loc[index, 'Kategorie'] = row['Unnamed: 4']
            dataframe.loc[index, 'Ebene'] = '5'

    dataframe.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1 , inplace=True)
    dataframe_long = dataframe.melt(id_vars=['Kategorie', 'Ebene'], var_name=columnnames, value_name='CHF') #Hier wird der df in das Long-Format geändert, da man so viel einfacher Diagramme mit plotly erstellen kann.
    return dataframe_long


df_year_chf = clean_data(df_year_chf, 'Jahr')
df_age_chf = clean_data(df_age_chf, 'Altersklasse')
df_income_chf = clean_data(df_income_chf, 'Einkommensklasse')
df_type_chf = clean_data(df_type_chf, 'Haushaltstyp')


# Erzeugen eines dict mit den Kategorien >> wird für die Checkliste benötigt
# Dabei kann ein beliebiger dict von oben verwendet werden, da die Kategorien bei allen gleich sind
categories_data = {}
for index, row in df_year_chf.iterrows():
    #Da die Kategorien im df im Long-Format mehrmals vorkommen, wird hier gestoppt, wenn 'Bruttoeinkommen' das zweite Mal vorkommt. Denn dann ist die Liste bereits komplett.
    if row['Ebene'] == '0':
        if len(categories_data) == 0:            
            rowkey_level0 = row['Kategorie']
            categories_data[rowkey_level0] = {}
        else:
            break
    elif row['Ebene'] == '1':
        rowkey_level1 = row['Kategorie']
        categories_data[rowkey_level0][rowkey_level1] = {}
    elif row['Ebene'] == '2':
        rowkey_level2 = row['Kategorie']
        categories_data[rowkey_level0][rowkey_level1][rowkey_level2] = {}
    elif row['Ebene'] == '3':
        rowkey_level3 = row['Kategorie']
        categories_data[rowkey_level0][rowkey_level1][rowkey_level2][rowkey_level3] = {}
    elif row['Ebene'] == '4':
        rowkey_level4 = row['Kategorie']
        categories_data[rowkey_level0][rowkey_level1][rowkey_level2][rowkey_level3][rowkey_level4] = {}
    elif row['Ebene'] == '5':
        rowkey_level5 = row['Kategorie']
        categories_data[rowkey_level0][rowkey_level1][rowkey_level2][rowkey_level3][rowkey_level4][rowkey_level5] = {}


#Für die Checklisterstellung kann ein beliebiger df von oben verwendet werden, da die Kategorie bei allen gleich ist.
#Da der df in das Long-Format kovertiert wurde, sind die Kategorien mehrfach vorhanden.
checklist_values = df_year_chf['Kategorie'].tolist()


def generate_checklist(data, level=0):
    #Erzeugt rekursiv eine verschachtelte Checkliste aus einer Datenstruktur.
    checklists = []
    for key, value in data.items():
        if isinstance(value, dict):  # Verschachtelte Aufgaben
            checklists.append(
                html.Div([
                    dcc.Checklist(
                        id={"type": "checklist", "level": level, "key": key},
                        options=[{"label": key, "value": key}],
                        value=[],
                        labelStyle={"display": "block"},
                    ),
                    html.Div(
                        generate_checklist(value, level=level + 1),
                        style={"margin-left": "20px"}
                    ),
                ])
            )
        elif isinstance(value, list):  # Endebene der Checkliste
            checklists.append(
                html.Div([
                    dcc.Checklist(
                        id={"type": "checklist", "level": level, "key": key},
                        options=[{"label": item, "value": item} for item in value],
                        value=[],
                        labelStyle={"display": "block"},
                    )
                ], style={"margin-left": "20px"})
            )
    return checklists

app.layout = html.Div([html.H1("Dashboard Haushaltsausgaben"),
dbc.Tabs([
    dbc.Tab(label='Nach Jahr', tab_id='tab_year', children=[
       dbc.Row([
           dbc.Col([html.Div(generate_checklist(categories_data))], width=3),
           dbc.Col([dcc.Graph(id='graph_year')], width=9)
       ]) 
    ]),
    dbc.Tab(label='Nach Altersklasse', tab_id='tab_age', children=[
        dbc.Row([
            dbc.Col([dcc.Checklist(checklist_values, id='checklist_age')], width=3),
            dbc.Col([dcc.Graph(id='graph_age')], width=9)
        ])
    ]),
    dbc.Tab(label='Nach Einkommen', tab_id='tab_income', children=[
        dbc.Row([
            dbc.Col([dcc.Checklist(checklist_values, id='checklist_income')], width=3),
            dbc.Col([dcc.Graph(id='graph_income')], width=9)
        ])
    ]),
    dbc.Tab(label='Nach Haushaltstyp', tab_id='tab_type', children=[
        dbc.Row([
            dbc.Col([dcc.Checklist(checklist_values, id='checklist_type')], width=3),
            dbc.Col([dcc.Graph(id='graph_type')], width=9)
        ])
    ])
])  
])


"""
@callback(Output('graph_year', 'figure'), 
          Input({'type': 'checklist', 'level': MATCH, 'key': MATCH}, 'value'))

def update_graph_year(chosen_categories):
    df_graph = df_year_chf[df_year_chf['Kategorie'].isin(chosen_categories)]
    graph = px.line(df_graph, x='Jahr', y='CHF', color='Kategorie')
    graph.update_layout()
    return graph
"""

@callback(Output('graph_age', 'figure'), Input('checklist_age', 'value'))

def update_graph_age(chosen_categories):
    df_graph = df_age_chf[df_age_chf['Kategorie'].isin(chosen_categories)]
    graph = px.bar(df_graph, x='Altersklasse', y='CHF', color='Kategorie', barmode='group')
    graph.update_layout()
    return graph

@callback(Output('graph_income', 'figure'), Input('checklist_income', 'value'))

def update_graph_income(chosen_categories):
    df_graph = df_income_chf[df_income_chf['Kategorie'].isin(chosen_categories)]
    graph = px.bar(df_graph, x='Einkommensklasse', y='CHF', color='Kategorie', barmode='group')
    graph.update_layout()
    return graph

@callback(Output('graph_type', 'figure'), Input('checklist_type', 'value'))

def update_graph_type(chosen_categories):
    df_graph = df_type_chf[df_type_chf['Kategorie'].isin(chosen_categories)]
    graph = px.bar(df_graph, x='Haushaltstyp', y='CHF', color='Kategorie', barmode='group')
    graph.update_layout()
    return graph

if __name__ == '__main__':
    app.run_server(debug=False)

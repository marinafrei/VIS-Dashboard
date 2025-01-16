from dash import Dash, dcc, html, Input, Output, callback, ALL, MATCH, State, no_update
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash (__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

rows_to_skip= list(range(0,13)) + [14,15,16,18,19,20] + list(range(553,583))
df_year_chf = pd.read_excel('data.xlsx', sheet_name='Jahr', skiprows=rows_to_skip, usecols='A:G,I,K,M')
df_region_chf = pd.read_excel('data.xlsx', sheet_name='Grossregion', skiprows=rows_to_skip, usecols='A:G,I,K,M,O,Q,S')
df_lang_chf = pd.read_excel('data.xlsx', sheet_name='Sprachregion', skiprows=rows_to_skip, usecols='A:G,I,K')
df_canton_chf = pd.read_excel('data.xlsx', sheet_name='Kantone', skiprows=rows_to_skip, usecols='A:G,I,K,M,O,Q,S,U')
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
    dataframe_long['CHF'] = pd.to_numeric(dataframe_long['CHF'], errors='coerce') #konvertiert die Spalte CHF in numerische Werte und wandelt nicht-kobertierbare Werte d.h. '( )' zu NaN um
    dataframe_long['CHF'] = dataframe_long['CHF'].round(2) #Rundet die Spalte CHF auf zwei Nachkommastellen    
    return dataframe_long


df_year_chf = clean_data(df_year_chf, 'Jahr')
df_region_chf = clean_data(df_region_chf, 'Grossregion')
df_lang_chf = clean_data(df_lang_chf, 'Sprachregion')
df_canton_chf = clean_data(df_canton_chf, 'Kanton')
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

    def search_checklist(data, search_value, styles={}, no_result=True):
            for key, value in data.items():
                styles[key] = [{'margin-left': '20px', 'display': 'flex'}]
                if key == 'Bruttoeinkommen': #oberste Ebene immer einblenden
                    styles[key].append({'margin-left': '20px', 'display': 'block'})
                    styles[key].append('▾')
                elif '.' not in key[0:6]: #die untersten Ebenen haben einen Punkt im key und bei der untersten Ebenen gibt es kein toggle-div, da es dort keine Unterpunkte mehr gibt zum Einblenden.
                    styles[key].append({'margin-left': '20px', 'display': 'none'})
                    styles[key].append('▸')
                elif '.' in key[0:6]:
                    styles[key].append('empty')
                    styles[key].append('empty')                    
                if search_value.lower() in key.lower():
                    styles[key][0] = {'margin': '3px','margin-left': '20px', 'display': 'flex', 'backgroundColor': 'lightblue'}
                    no_result=False
                    for styles_key in styles:
                        category_number = styles_key.split(':')[0]
                        if category_number in key and styles_key != key:
                            styles[styles_key][1] = {'margin-left': '20px', 'display': 'block'}
                            styles[styles_key][2] = '▾'
                        if key.startswith('5') or key.startswith('6'):
                            styles['50: Konsumausgaben'][1] = {'margin-left': '20px', 'display': 'block'}
                            styles['50: Konsumausgaben'][2] = '▾'
                        elif key.startswith('31') or key.startswith('32') or key.startswith('33'):
                            styles['30: Obligatorische Transferausgaben'][1] = {'margin-left': '20px', 'display': 'block'}
                            styles['30: Obligatorische Transferausgaben'][2] = '▾'
                        elif key.startswith('36'):
                            styles['35: Monetäre Transferausgaben an andere Haushalte'][1] = {'margin-left': '20px', 'display': 'block'}
                            styles['35: Monetäre Transferausgaben an andere Haushalte'][2] = '▾'
                        elif key.startswith('4'):
                            styles['40: Übrige Versicherungen, Gebühren und Übertragungen'][1] = {'margin-left': '20px', 'display': 'block'}
                            styles['40: Übrige Versicherungen, Gebühren und Übertragungen'][2] = '▾'
                        elif key.startswith('8'):
                            styles['80: Prämien für die Lebensversicherung'][1] = {'margin-left': '20px', 'display': 'block'}
                            styles['80: Prämien für die Lebensversicherung'][2] = '▾'
                if isinstance(value, dict):
                    _, child_no_result = search_checklist(value, search_value, styles, no_result)
                    no_result = no_result and child_no_result        
            return styles, no_result

def generate_checklist(data, level=0, return_values=None, checked_values=None):
    # Erzeugt rekursiv eine verschachtelte Checkliste.
    checklists = []
    for key, value in data.items():
        # Dynamische IDs für Button und das zu toggelnde Div
        button_id = {"type": "toggle-button", "key": key}
        toggle_div_id = {"type": "toggle-div", "key": key}
        checklist_id = {"type": "checklist", "key": key}
        if return_values:
            checklist_style = return_values[key][0]
            toggle_div_style = return_values[key][1]
            button_value = return_values[key][2]
        if checked_values:
            if key in checked_values:
                checked_key = [key]
            else:
                checked_key = None
        if isinstance(value, dict) and value:  # Verschachtelte Aufgaben (nicht-leeres Dict)
            checklists.append(
                html.Div([
                    html.Div([
                            dbc.Button(
                                button_value if return_values else ('▾' if key == 'Bruttoeinkommen' else '▸'),
                                id=button_id,
                                style={
                                    'color': 'black',
                                    'padding': '0px',
                                    'background-color': 'transparent',
                                    'border-style': 'none',
                                    'display': 'flex',
                                    'align-items': 'flex-start'
                                }
                            ),
                            dcc.Checklist(
                                id=checklist_id,
                                options=[{"label": key, "value": key}],
                                value=checked_key if checked_values and checked_key else ([key] if key == "50: Konsumausgaben" and not checked_values else []), #Konsumausgaben als Default-Wert setzen beim Starten des Dashboard
                                labelStyle={"display": "block"},
                            )
                        ], style=checklist_style if return_values else {'display': 'flex'}
                    ),
                    # Rekursive Erzeugung für den nächsten Level
                    html.Div(
                        generate_checklist(value, level=level + 1, return_values=return_values, checked_values=checked_values),
                        id=toggle_div_id,  # ID für das darunterliegende Div
                        style=toggle_div_style if return_values else ({"margin-left": "20px", "display": "block" if key == 'Bruttoeinkommen' else 'none'})  # Standardmäßig ausgeblendet
                    ),
                ])
            )
        elif isinstance(value, dict) and not value:  # Endebene: leeres Dict
            checklists.append(
                html.Div([
                    dcc.Checklist(
                        id={"type": "checklist", "key": key},
                        options=[{"label": key, "value": key}],
                        value=checked_key if checked_values and checked_key else [],
                        labelStyle={"display": "block"},
                    )
                ], style=checklist_style if return_values else {"margin-left": "20px", 'display': 'flex'})
            )
    return checklists


nested_checklist = generate_checklist(categories_data)


app.layout = html.Div([
    dbc.Row([
        dbc.Col([html.H1("Dashboard Haushaltsausgaben", style={'padding': '0px 10px'})], style={'padding': '0px'}, width=11),
        dbc.Col([dbc.Button('i', id='info', style={'width': '30px', 'height': '30px', 'border-radius': '50%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'backgroundColor': '#6C53C8', 'border-color': 'white', 'border-width': '3px'}),
                 dbc.Modal([
                     dbc.ModalHeader(dbc.ModalTitle('Informationen zum Datensatz')),
                     dbc.ModalBody([
                         html.Div([
                             'In diesem Dashboard werden die Daten der Haushaltsbudgeterhebung des Bundesamts für Statistik im Zeitraum von 2018-2021 visualisiert. ',
                             html.Br(),
                             'Die Daten im Tab "Nach Jahr" zeigen die Jahre 2018-2021. ',
                             html.Br(), 
                             'Allen anderen Tabs liegen die kumulierten Daten von 2018 und 2019 vor. ' ,
                             html.Br(),
                             'Im Tab "Nach Kantonen" sind nur die bevölkerungsreichsten Kantone aufgeführt. ' ,
                             html.Br(), 
                             'Zu beachten ist ausserdem, dass es teilweise Lücken im Datensatz hat, wenn es für eine Kennzahl zu wenige Beobachtungen gibt. In den Balkendiagrammen wird dies mit dem Wert "NaN" markiert. Im Liniendiagramm ist dies lediglich an fehlenden Werten zu erkennen.',
                             html.Br(),
                             html.Br(),
                             'Der originale Datensatz ist unter folgendem Link zu finden:',
                             html.Br(),
                             html.A('Link zum Datensatz', href='https://www.bfs.admin.ch/bfs/de/home/statistiken/katalog.assetdetail.32288712.html', target='_blank')
                         ], style={'height': '400px'})
                     ])
                 ], id='modal', is_open=False)
        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}, width=1)
    ], style={'color': 'white', 'backgroundColor': '#6C53C8', 'margin': '0px 0px 5px'}),    
    dbc.Row([
        dbc.Col([
            html.H4("Auswahl der Daten", style={'padding': '0px 10px', 'color': '#6C53C8'}),
            dcc.Input(id='textsearch', placeholder='Suche nach Kategorie...', value=None, type='text', style={'margin': '5px'}),
            dbc.Button('Suchen', id='search-button', style={'backgroundColor': '#6C53C8', 'border': '0px', 'height': '35px'}),
            html.Br(),
            dbc.Button('Checkliste zurücksetzen', id='reset', style={'backgroundColor': '#6C53C8', 'border': '0px', 'margin': '5px'}),
            html.Div('', id='show_no_result', style={'padding': '0px 5px', 'font-weight': 'bold'}),
            html.Div(nested_checklist, id='nested_checklist')
        ], width=3),
        dbc.Col([
            dbc.Tabs(id='tabs', active_tab='tab_year', children=[
                dbc.Tab(label='Nach Jahr', tab_id='tab_year', label_style={'color': '#6C53C8'}, active_label_style={'backgroundColor': '#6C53C8', 'color': 'white'}),
                dbc.Tab(label='Nach Altersklasse', tab_id='tab_age', label_style={'color': '#6C53C8'}, active_label_style={'backgroundColor': '#6C53C8', 'color': 'white'}),
                dbc.Tab(label='Nach Einkommen', tab_id='tab_income', label_style={'color': '#6C53C8'}, active_label_style={'backgroundColor': '#6C53C8', 'color': 'white'}),
                dbc.Tab(label='Nach Haushaltstyp', tab_id='tab_type', label_style={'color': '#6C53C8'}, active_label_style={'backgroundColor': '#6C53C8', 'color': 'white'}),
                dbc.Tab(label='Nach Grossregion', tab_id='tab_region', label_style={'color': '#6C53C8'}, active_label_style={'backgroundColor': '#6C53C8', 'color': 'white'}),
                dbc.Tab(label='Nach Sprachregion', tab_id='tab_lang', label_style={'color': '#6C53C8'}, active_label_style={'backgroundColor': '#6C53C8', 'color': 'white'}),
                dbc.Tab(label='Nach Kantonen', tab_id='tab_canton', label_style={'color': '#6C53C8'}, active_label_style={'backgroundColor': '#6C53C8', 'color': 'white'})
            ]),
            dcc.Graph(id='graph-output')
        ], width=9)
    ])
])

@callback(Output('modal', 'is_open'),
          Input('info', 'n_clicks'),
          prevent_initial_call=True)

def manage_info_popup(n_clicks):
    is_open = True
    return is_open



@callback([Output('nested_checklist', 'children', allow_duplicate=True),
          Output('show_no_result', 'children', allow_duplicate=True)],
          Input('reset', 'n_clicks'),            
          prevent_initial_call=True)

def reset_checklist(n_clicks):   
      show_no_result = ''
      return nested_checklist, show_no_result    



@callback([Output('nested_checklist', 'children', allow_duplicate=True),
          Output('show_no_result', 'children', allow_duplicate=True)],
          Input('search-button', 'n_clicks'), 
          State({'type': 'checklist', 'key': ALL}, 'value'),           
          State('textsearch', 'value'),
          prevent_initial_call=True)


def text_search(n_clicks, all_checked_values, search_value):
    if search_value == None:
        show_no_result = 'Bitte einen Suchbegriff eingeben'
        return no_update, show_no_result
    else:
        checked_values = []
        for checklist in all_checked_values:
            if checklist: #Not empty
                for value in checklist:
                    checked_values.append(value) 
        return_values, no_result = search_checklist(categories_data, search_value)
        checklist = generate_checklist(categories_data, 0, return_values, checked_values)
        if no_result == True:
            show_no_result = 'Keine Resultate gefunden'
        else:
            show_no_result = ''  

        return checklist, show_no_result
                


@callback(
    [Output({'type': 'toggle-div', 'key': MATCH}, 'style', allow_duplicate=True),
     Output({'type': 'toggle-button', 'key': MATCH}, 'children', allow_duplicate=True)],
    Input({'type': 'toggle-button', 'key': MATCH}, 'n_clicks'),
    State({'type': 'toggle-div', 'key': MATCH}, 'style'),
    prevent_initial_call=True
)

def toggle_div_visibility(n_clicks, current_style):
    # Wenn der Button geklickt wurde, wird die Sichtbarkeit des darunterliegenden div geändert.
    if current_style.get('display') == 'none':
        return {'margin-left': '20px', 'display': 'block'}, '▾'
    else:
        return {'margin-left': '20px', 'display': 'none'}, '▸'



@callback(Output('graph-output', 'figure'), 
          Input({'type': 'checklist', 'key': ALL}, 'value'),
          Input('tabs', 'active_tab')
          )

def update_graphs(all_checked_values, active_tab):
    checked_values = []
    for checklist in all_checked_values:
        if checklist: #Not empty
            for value in checklist:
                checked_values.append(value)
    
    if active_tab == 'tab_year':
        df_graph = df_year_chf[df_year_chf['Kategorie'].isin(checked_values)]
        graph = px.line(df_graph, x='Jahr', y='CHF', color='Kategorie', text='CHF')
        graph.update_traces(textposition='top center')
    elif active_tab == 'tab_age':
        df_graph = df_age_chf[df_age_chf['Kategorie'].isin(checked_values)]
        graph = px.bar(df_graph, x='Altersklasse', y='CHF', color='Kategorie', barmode='group', text_auto=True) 
        graph.update_traces(textposition='outside')
    elif active_tab == 'tab_income':
        df_graph = df_income_chf[df_income_chf['Kategorie'].isin(checked_values)]
        graph = px.bar(df_graph, x='Einkommensklasse', y='CHF', color='Kategorie', barmode='group', text_auto=True)
        graph.update_traces(textposition='outside')
    elif active_tab == 'tab_type':
        df_graph = df_type_chf[df_type_chf['Kategorie'].isin(checked_values)]
        graph = px.bar(df_graph, x='Haushaltstyp', y='CHF', color='Kategorie', barmode='group', text_auto=True)
        graph.update_traces(textposition='outside')
        graph.update_layout(margin=dict(t=20, b=0, l=40, r=40), height=480) #Braucht sonst zu viel Platz wegen den langen Beschriftungen und Zahl auf Balken wird dann abgeschnitten.
    elif active_tab == 'tab_region':
        df_graph = df_region_chf[df_region_chf['Kategorie'].isin(checked_values)]
        graph = px.bar(df_graph, x='Grossregion', y='CHF', color='Kategorie', barmode='group', text_auto=True)
        graph.update_traces(textposition='outside')
    elif active_tab == 'tab_lang':
        df_graph = df_lang_chf[df_lang_chf['Kategorie'].isin(checked_values)]
        graph = px.bar(df_graph, x='Sprachregion', y='CHF', color='Kategorie', barmode='group', text_auto=True)
        graph.update_traces(textposition='outside')
    elif active_tab == 'tab_canton':
        df_graph = df_canton_chf[df_canton_chf['Kategorie'].isin(checked_values)]
        graph = px.bar(df_graph, x='Kanton', y='CHF', color='Kategorie', barmode='group', text_auto=True)
        graph.update_traces(textposition='outside')

    graph.update_layout(template='plotly_white')
    return graph


if __name__ == '__main__':
    app.run_server(debug=True)

import streamlit as st
import pandas as pd
import time
import os
from pathlib import Path

st.set_page_config(page_title="Càrrega de dades")
st.title("Càrrega de dades")

# ----- Funcions del programa -----

def carregar_dades(ciutat):
    # Població
    df_poblacio = pd.read_csv(f'dat/{ciutat}/poblacio.csv', skiprows=10, sep=";", decimal=",")
    df_poblacio.rename(columns={"Unnamed: 0":"Any", "Total":"Població"}, inplace=True)
    df_poblacio = df_poblacio.set_index("Any")
    df_poblacio = df_poblacio[['Població']]
    
    # Densitat
    df_densitat = pd.read_csv(f'dat/{ciutat}/densitat.csv', skiprows=6, sep=";", decimal=',')
    df_densitat.rename(columns={"Unnamed: 0":"Any", "Superfície (km²)":"Superfície", "Densitat (hab./km²)":"Densitat"}, inplace=True)
    df_densitat.set_index("Any", inplace=True)
    df_densitat = df_densitat[['Superfície', 'Densitat']]
    
    # Naixements
    df_naixements = pd.read_csv(f'dat/{ciutat}/naixements.csv', skiprows=8, sep=";")
    df_naixements.rename(columns={"Unnamed: 0":"Any", "Total":"Naixements"}, inplace=True)
    df_naixements.set_index("Any", inplace=True)
    df_naixements = df_naixements[['Naixements']]
    
    # Defuncions
    df_defuncions = pd.read_csv(f'dat/{ciutat}/defuncions.csv', skiprows=7, sep=";")
    df_defuncions.rename(columns={"Unnamed: 0":"Any", "Total":"Defuncions"}, inplace=True)
    df_defuncions.set_index("Any", inplace=True)
    df_defuncions = df_defuncions[['Defuncions']]

    # Aturats
    df_atur = pd.read_csv(f'dat/{ciutat}/atur.csv', skiprows=6, sep=";", decimal=',')
    df_atur.rename(columns={"Unnamed: 0":"Any", "Sexe. Total":"Aturats"}, inplace=True)
    df_atur = df_atur.set_index("Any")
    df_atur = df_atur[['Aturats']]

    # Pensionistes
    df_pensionistes = pd.read_csv(f'dat/{ciutat}/pensionistes.csv', skiprows=7, sep=";")
    df_pensionistes.rename(columns={'Unnamed: 0':'Any', 'Total':'Pensionistes'}, inplace=True)
    df_pensionistes = df_pensionistes.set_index("Any")
    df_pensionistes = df_pensionistes[['Pensionistes']]

    # Habitatges acabats
    df_habit = pd.read_csv(f'dat/{ciutat}/habitatges_construits.csv', skiprows=10, sep=";")
    noves_col = {
        'Unnamed: 0':'Any',
        'Habitatges iniciats amb protecció oficial':'HPO iniciats',
        'Habitatges acabats amb protecció oficial':'HPO acabats'
    }
    df_habit.rename(columns=noves_col, inplace=True)
    df_habit.set_index('Any', inplace=True)
    df_habit = df_habit[['HPO acabats', 'Habitatges acabats']]

    # Vehicles
    df_vehicles = pd.read_csv(f'dat/{ciutat}/vehicles.csv', skiprows=6, sep=";")
    df_vehicles.rename(columns={'Unnamed: 0':'Any'}, inplace=True)
    df_vehicles.set_index('Any', inplace=True)
    df_vehicles = df_vehicles[['Turismes', 'Motocicletes']]

    # Renta Familiar Disponible per Habitant
    df_rdf = pd.read_csv(f'dat/{ciutat}/rfd.csv', skiprows=6, sep=";")
    df_rdf.rename(columns={"Unnamed: 0":"Any",'Per habitant (€)':'RFDH' }, inplace=True)
    df_rdf = df_rdf.set_index("Any")
    df_rdf = df_rdf[['RFDH']]

    # Saldo de migracions internes
    df_migracionsint = pd.read_csv(f'dat/{ciutat}/migracions_internes.csv', skiprows=7, sep=";", decimal=",")
    df_migracionsint.rename(columns={"Unnamed: 0":"Any", 'Total':'Migracions internes'}, inplace=True)
    df_migracionsint = df_migracionsint.set_index("Any")
    df_migracionsint = df_migracionsint[['Migracions internes']]

    # Saldo de migracions externes
    df_migracionsext = pd.read_csv(f'dat/{ciutat}/migracions_externes.csv', skiprows=8, sep=";", decimal=",")
    df_migracionsext.rename(columns={"Unnamed: 0":"Any", 'Total':'Migracions externes'}, inplace=True)
    df_migracionsext = df_migracionsext.set_index("Any")
    df_migracionsext = df_migracionsext[['Migracions externes']]
    
    df = pd.concat([df_poblacio, df_densitat, df_naixements, df_defuncions, df_migracionsint, df_migracionsext,
                    df_atur, df_pensionistes, df_habit, df_vehicles, df_rdf], axis=1).sort_index(ascending=True)
    
    return df

def neteja_dades (df):
    df = df.drop(range(1975,2010))
    df.drop(2025, inplace=True)
    df['Població'] = df['Població'].fillna(round(df['Densitat']* df['Superfície'], 0))
    df.loc[2015, 'Pensionistes'] = round((df['Pensionistes'][2016]+df['Pensionistes'][2014])/2, 0)
    df.loc[2010, 'Pensionistes'] = round(2*df.loc[2011, 'Pensionistes'] - df.loc[2012, 'Pensionistes'], 0)
    df.loc[2023, 'RFDH'] = round(2*df.loc[2022, 'RFDH'] - df.loc[2021, 'RFDH'], 0)
    df.loc[2024, 'RFDH'] = round(2*df.loc[2023, 'RFDH'] - df.loc[2022, 'RFDH'], 0)
    df.loc[2024, 'Migracions internes'] = round(2*df.loc[2023, 'Migracions internes']
                                                - df.loc[2022, 'Migracions internes'], 0)
    df.loc[2024, 'Migracions externes'] = round(2*df.loc[2023, 'Migracions externes']
                                                - df.loc[2022, 'Migracions externes'], 0)
    df.drop(columns='Superfície', inplace=True)
    return df

def afegir_taxes (df):
    df['Taxa natalitat'] = round(df.Naixements * 100 / df.Població, 2)
    df['Taxa mortalitat'] = round(df.Defuncions * 100 / df.Població, 2)
    df['Taxa atur'] = round(df.Aturats * 100 / df.Població, 2)
    df['Taxa dependència'] = round(df.Pensionistes * 100 / df.Població, 2)
    df['Taxa HPO'] = round(df['HPO acabats'] * 1000 / df.Població, 2)
    df['Taxa habitatges'] = round(df['Habitatges acabats'] * 1000 / df.Població, 2)
    df['Taxa turismes'] = round(df.Turismes * 100 / df.Població, 2)
    df['Taxa motocicletes'] = round(df.Motocicletes * 100 / df.Població, 2)
    return df

# ----- INICI PROGRAMA -----

tab1, tab2 = st.tabs(['Carregar', 'Borrar'])

with tab1:
    ciutats = ['Sant Cugat', 'Terrassa', 'Sabadell', 'Barcelona']

    ciutat = st.selectbox('Selecciona una ciutat per estudiar les dades:', ciutats,
                          index=None, placeholder='Ciutat...', key='Carregar dades')

    if st.button('Carregar dades'):
        if ciutat:
            st.session_state.df_in = carregar_dades(ciutat)
            st.write(f"Dades de {ciutat}")
            st.dataframe(st.session_state.df_in)
        else:
            st.error('Has de seleccionar una ciutat')
            time.sleep(3)
            st.rerun()

    if st.button('Consolidar dades'):
        if st.session_state.df_in is not None:
            df = neteja_dades(st.session_state.df_in)
            df = afegir_taxes(df)
            st.write(f"Dades consolidades de {ciutat}")
            st.dataframe(df)
            df.to_csv(f'dat/temp/Dades {ciutat}.csv', sep=';')
            st.success('Dades consolidades correctament')
            st.session_state["df_in"] = None
            
        else:
            st.error('Les dades no existeixen')
            time.sleep(3)
            st.rerun()

with tab2:
    
    carpeta = Path("dat/temp")
    fitxers = list(carpeta.glob("*"))
    st.write("**Fitxers disponibles:**")
    for f in fitxers:
        st.write(f.name)

    st.space('small')
    ciutats = ['Sant Cugat', 'Terrassa', 'Sabadell', 'Barcelona']

    ciutat = st.selectbox('Selecciona una ciutat per estudiar les dades:', ciutats,
                          index=None, placeholder='Ciutat...', key='Borrar dades')

    if st.button('Borrar arxiu consolidat'):
        if ciutat:
            if os.path.exists(f'dat/temp/Dades {ciutat}.csv'):
                os.remove(f'dat/temp/Dades {ciutat}.csv')
                st.success(f"Fitxer Dades {ciutat}.csv eliminat correctament")
                time.sleep(3)
                st.rerun()
            else:
                st.error(f"El fitxer Dades {ciutat}.csv no existeix")
                time.sleep(3)
                st.rerun()
        
    



import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Anàlisi descriptiu")
st.title("Anàlisi descriptiu")

ciutats = ['Sant Cugat', 'Terrassa', 'Sabadell', 'Barcelona']
dfs = {}

carpeta = Path('dat/temp')
fitxers = list(carpeta.glob("*"))

ciutats_disp = []

for f in fitxers:
    for ciutat in ciutats:
        if ciutat in f.name:
            df = pd.read_csv(f'dat/temp/Dades {ciutat}.csv', sep=';', index_col='Any')
            df['Ciutat'] = ciutat
            dfs[ciutat] = df
            ciutats_disp.append(ciutat)

ciutats_sel = st.multiselect('Selecciona les ciutats a mostrar',
                             options=ciutats_disp,
                             default=ciutats_disp)

if ciutats_sel:
    df_total = pd.concat([dfs[c] for c in ciutats_sel])
    st.dataframe(df_total)
    
    fig = px.line(df_total, 
                  y='Població',
                  title=f'Evolució de la població',
                  color='Ciutat'
                 )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)

    fig = px.line(df_total, 
                  y='Migracions internes',
                  title=f'Evolució del saldo de migracions internes',
                  color='Ciutat'
                 )
    fig.update_xaxes(showgrid=True)
    fig2 = px.line(df_total,
                   y='Migracions externes',
                   title=f'Evolució del saldo de migracions externes',
                   color='Ciutat'
                  )
    fig2.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

    df_temp = df_total.reset_index()
    df_long = df_temp.melt(
        id_vars=["Any", "Ciutat"],
        value_vars=["Taxa natalitat", "Taxa mortalitat"],
        var_name="Taxa",
        value_name="Valor"
    )

    fig = px.line(df_long, 
                  x='Any',
                  y='Valor',
                  color='Ciutat',
                  line_dash='Taxa',
                  title=f'Evolució de les taxes de natalitat i mortalitat per cada 100 habitants',
                  labels={'Valor':'Taxa', 'Taxa':'Indicador'}
                 )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)

    fig = px.line(df_total, 
                  y='RFDH',
                  title=f'Evolució de la Renta Familiar Disponible per habitant',
                  color='Ciutat'
                 )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)

    fig = px.line(df_total, y='Taxa atur',
                  title=f"Evolució de la taxa d'atur per cada 100 habitants",
                  labels={'value':"Taxa d'atur"},
                  color='Ciutat'
                 )
    fig2 = px.line(df_total, y='Taxa dependència',
                   title=f"Evolució de la taxa de dependència per cada 100 habitants",
                   labels={'value':"Taxa de dependència"},
                   color='Ciutat'
                  )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    fig2.update_xaxes(showgrid=True)
    st.plotly_chart(fig2)

    df_temp = df_total.reset_index()
    df_long = df_temp.melt(
        id_vars=["Any", "Ciutat"],
        value_vars=["Taxa HPO", "Taxa habitatges"],
        var_name="Taxa",
        value_name="Valor"
    )

    fig = px.line(df_long,
                  x='Any',
                  y='Valor',
                  color='Ciutat',
                  line_dash='Taxa',
                  title=f"Taxes de construcció d'habitatges per cada 1000 habitants",
                  labels={'Valor':'Taxa', 'Taxa':'Indicador'}
                 )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)

    fig = px.line(df_total, 
                  y='Taxa turismes',
                  title=f'Taxa de turismes per cada 100 habitants',
                  color='Ciutat'
                 )
    fig2 = px.line(df_total, 
                   y='Taxa motocicletes',
                   title=f'Taxa de motocicletes per cada 100 habitants',
                   color='Ciutat'
                  )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    fig2.update_xaxes(showgrid=True)
    st.plotly_chart(fig2)
    
else:
    st.error('No hi ha cap ciutat seleccionada')

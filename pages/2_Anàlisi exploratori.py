import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Anàlisi exploratori")
st.title("Anàlisi exploratori")

ciutats = ['Sant Cugat', 'Terrassa', 'Sabadell', 'Barcelona']
dfs = {}

carpeta = Path('dat/temp')
fitxers = list(carpeta.glob("*"))

for f in fitxers:
    for ciutat in ciutats:
        if ciutat in f.name:
            dfs[ciutat] = pd.read_csv(f'dat/temp/Dades {ciutat}.csv', sep=';', index_col='Any')
            with st.expander(f'**Dades de {ciutat}**'):
                with st.expander(f'Taula de dades de {ciutat}'):
                    st.dataframe(dfs[ciutat])
                
                st.write(dfs[ciutat].describe())
                
                if st.button(f'Matriu de correlacions de {ciutat}'):
                    fig = sns.pairplot(dfs[ciutat])
                    st.pyplot(fig)
                
                corr = dfs[ciutat].corr()
                fig = px.imshow(
                    corr,
                    text_auto=True,
                    color_continuous_scale='RdBu_r',
                    aspect='auto'
                )
                fig.update_layout( title='Heatmap de correlacions', xaxis_title='Variables', yaxis_title='Variables')
                st.plotly_chart(fig)
                
                cols = [c for c in dfs[ciutat].columns if 'Taxa' in c]
                cols.append('RFDH')
                cols.append('Població')
                corr = dfs[ciutat][cols].corr()
                fig = px.imshow(
                    corr,
                    text_auto=True,
                    color_continuous_scale='RdBu_r',
                    aspect='auto'
                )
                fig.update_layout( title='Heatmap de correlacions entre taxes', xaxis_title='Variables', yaxis_title='Variables' )
                st.plotly_chart(fig)
                
                fig = px.scatter(dfs[ciutat], x='Població', y=['Taxa natalitat', 'Taxa atur', 'Taxa dependència', 'Taxa motocicletes'],
                                 trendline='ols', title='Correlació Població vs diferents taxes')
                fig.update_xaxes(showgrid=True)
                st.plotly_chart(fig)
                
                fig = px.scatter(dfs[ciutat], x='RFDH', y=['Taxa natalitat', 'Taxa atur', 'Taxa dependència', 'Taxa motocicletes'],
                                 trendline='ols', title='Correlació RFDH vs diferents taxes')
                fig.update_xaxes(showgrid=True)
                st.plotly_chart(fig)
                
                fig = px.scatter(dfs[ciutat], x='Població', y='RFDH',
                                 trendline='ols', title='Correlació Població vs RFDH')
                fig.update_xaxes(showgrid=True)
                st.plotly_chart(fig)
                
                fig = px.scatter(dfs[ciutat], x='Taxa atur', y='Taxa dependència',
                                 trendline='ols', title='Correlació Taxa atur vs Taxa dependència')
                fig.update_xaxes(showgrid=True)
                st.plotly_chart(fig)



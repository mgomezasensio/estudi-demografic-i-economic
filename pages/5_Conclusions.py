import streamlit as st


st.set_page_config(page_title="Conclusions")
st.title("Conclusions")

with st.container(border=True):
    st.write("""
L'estudi dóna una visió d'un Sant Cugat en creixement, liderant en diversos camps estudiats en aquest projecte. Destacar que el saldo de migracions internes negatiu
visualitza la quantitat de persones que viuen a Sant Cugat i han de marxar a viure a altres municipis, de la mateixa manera que passa a Barcelona.
""")

st.space('stretch')

with st.container(border=True):
    st.write("""
En gairebé totes les gràfiques de totes les ciutats estudiades s'aprecia la influència de la pandèmia del COVID19, amb pics pronunciats i empitjorament
dels indicadors estudiats.
""")
    
st.space('stretch')

with st.container(border=True):
    st.write("""
L'efecte de disposar d'una sèrie amb poques dades es veu reflectida en les prediccions. Per a alguns dels municipis estudiats,
les prediccions es podrien ajustar millor seleccionant altres indicadors amb més correlacions amb la variable objectiu.
""")

st.space('stretch')

with st.container(border=True):
    st.write("""
En les prediccions, es podria afegir un selector per seleccionar la variable objectiu. Per tal de fer prediccions a futur, també caldria afegir un form per omplir
els indicadors necessaris pel model de Regressió Multiple escollit.
""")
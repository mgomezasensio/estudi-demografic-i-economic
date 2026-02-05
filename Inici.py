from datetime import date
import streamlit as st
import sqlite3


st.set_page_config(
    page_title="Anàlisi de dades demogràfiques i econòmiques per a diferents ciutats",
)

st.write("# Anàlisi de dades demogràfiques i econòmiques per a diferents ciutats")
tab1, tab2 = st.tabs(['Resum', 'Descripció dades'])
with tab1:
    st.write("Aquesta aplicació té per objectiu estudiar diferents dades demogràfiques i econòmiques de diferents ciutats.")
    st.space('small')
    st.write("""Aquesta és la interfície principal, on es mostraran i s'introduïran les dades. A la barra lateral es pot seleccionar la secció on es vol treballar:
                \n - Càrrega de dades: Apartat des d'on es carregaran les dades guardades en els arxius .csv.
                \n - Anàlisi exploratori: Apartat on es fa un anàlisi exploratori de les dades.
                \n - Anàlisi descriptiu: Apartat on es fa un anàlisi descriptiu de les dades.
                \n - Anàlisi predictiu: Apartat on es fa un anàlisi predictiu de les dades
                \n - Conclusions: Apartat on es mostren les conclusions de l'estudi de les dades.""")
with tab2:
    st.write("**Descripció de les dades**")
    st.write("Les dades han estat obtingudes de la pàgina del Institut d'Estadística de Catalunya (https://www.idescat.cat/).")
    st.markdown("""
Les dades seleccionades comprenen un rang de 15 anys (2010-2024) amb les columnes descrites a continuació:
- Població: nombre d'habitants a la ciutat seleccionada
- Superfície: superfície compresa per la ciutat seleccionada en Km quadrats
- Densitat: densitat de població en habitants per Km quadrat
- Naixements: nombre de naixements per la ciutat seleccionada
- Defuncions: nombre de defuncions per la ciutat seleccionada
- Migracions internes: saldo de migracions internes a nivell estatal. Saldo positiu = guany d'habitants, saldo negatiu = pèrdua d'habitants
- Migracions externes: saldo de migracions externes a nivell internacional. Saldo positiu = guany d'habitants, saldo negatiu = pèrdua d'habitants
- Aturats: nombre de persones inscrites a l'atur per la ciutat seleccionada
- Pensionistes: nombre de persones que reben una pensió contributiva
- HPO acabats: nombre d'Habitatges de Protecció Oficial (HPO) construïts durant aquell any
- Habitatges acabats: nombre d'habitatges construïts durant aquell any
- Turismes: nombre de turismes registrats a la ciutat
- Motocicletes: nombre de motocicletes registrades a la ciutat
- RFDH: Renda Familiar Disponible per Habitant (RFDH), mesura dels ingressos de què disposen els residents a les ciutats seleccionades per destinar-los
        al consum o a l'estalvi.
- Taxa natalitat: taxa de natalitat per cada 100 habitants
- Taxa mortalitat: taxa de mortalitat per cada 100 habitants
- Taxa atur: taxa d'atur per cada 100 habitants
- Taxa dependència: taxa de pensionistes per cada 100 habitants
- Taxa HPO: taxa d'Habitatges de Protecció Oficial (HPO) construïts per cada 1000 habitants
- Taxa habitatges: taxa d'habitatges construïts per cada 1000 habitants
- Taxa turismes: taxa de turismes registrats per cada 100 habitants
- Taxa motocicletes: taxa de motocicletes registrades per cada 100 habitants
""")

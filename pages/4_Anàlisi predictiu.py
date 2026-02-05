import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.linear_model import LinearRegression
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="Anàlisi predictiu")
st.title("Anàlisi predictiu")

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

ciutat_sel = st.selectbox('Selecciona la ciutat a mostrar',
                              options=ciutats_disp,
                              index=None,
                              placeholder='Ciutat...'
                          )
st.space('small')

if ciutat_sel:
    df = dfs[ciutat_sel]
    col1, col2 = st.columns(2)
    with col1:
        # Predicció de Població segons Naixements, Defuncions i Migracions amb Regressió Múltiple
        
        st.write("**Model de Regressió Múltiple**")

        X = df[["Naixements", "Defuncions", "Migracions internes", "Migracions externes"]]
        y = df[["Població"]]

        model = LinearRegression().fit(X, y)
        pred = model.predict(X)

        coeficients = pd.DataFrame({
            "Variable": X.columns,
            "Coeficient": model.coef_[0]
        })
        intercept = model.intercept_
        r2 = model.score(X, y)

        files_extres = pd.DataFrame({
            "Variable":["Intercept", "R2"],
            "Coeficient":[intercept[0], r2]
        })
        df_final = pd.concat([coeficients, files_extres], ignore_index=True)
        
        st.dataframe(df_final, hide_index=True)

        df_plot = df[['Població']]
        df_plot['Predicció'] = pred

    fig = px.line(df_plot,
                  title="Predicció de Població amb model de Regressió Múltiple"
                  )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    
    with col2:
        # Predicció de Població segons Naixements, Defuncions i Migracions amb Random Forest
        
        st.write("**Model de Random Forest**")

        # 1. Seleccionar variables
        X = df[["Naixements", "Defuncions", "Migracions internes", "Migracions externes"]]
        y = df["Població"]

        # 2. Dividir en entrenament i test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # 3. Crear i entrenar el model
        model = RandomForestRegressor(
            n_estimators=500,
            max_depth=None,
            random_state=42
        )

        model.fit(X_train, y_train)

        # 4. Avaluació
        preds = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        
        files_extres = pd.DataFrame({
            "Variable":["RMSE", "R2"],
            "Importancia":[rmse, r2]
        })
        
        # 5. Importància de les variables
        importances = pd.DataFrame(model.feature_importances_, index=X.columns).reset_index()
        importances.rename(columns={"index":"Variable", 0:"Importancia"}, inplace=True)
        
        df_final = pd.concat([importances, files_extres], ignore_index=True)
        
        st.dataframe(df_final, hide_index=True)
    
    st.space('small')
    
    # Predicció de Població segons Naixements, Defuncions, Aturats, Pensionistes, RFDH i Migracions

    st.write("**Model de Regressió Múltiple de Població segons Naixements, Defuncions, Aturats, Pensionistes, RFDH i Migracions**")
    
    X = df[["Naixements", "Defuncions", "Aturats", "Pensionistes", "RFDH", "Migracions internes", "Migracions externes"]]
    y = df[["Població"]]

    model = LinearRegression().fit(X, y)
    pred = model.predict(X)

    coeficients = pd.DataFrame({
        "Variable": X.columns,
        "Coeficient": model.coef_[0]
    })
    intercept = model.intercept_

    r2 = model.score(X, y)

    files_extres = pd.DataFrame({
            "Variable":["Intercept", "R2"],
            "Coeficient":[intercept[0], r2]
    })
    df_final = pd.concat([coeficients, files_extres], ignore_index=True)
    
    st.dataframe(df_final, hide_index=True)

    df_plot = df[['Població']]
    df_plot['Predicció'] = pred

    fig = px.line(df_plot,
                  title="Predicció de Població amb model de Regressió Múltiple"
                  )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    
    st.space('small')
    
    # Predicció del nombre d'Aturats segons Població, RFDH, Pensionistes, Naixements, Defuncions i Migracions

    st.write("**Model de Regressió Múltiple de Aturats segons Població, RFDH, Pensionistes, Naixements, Defuncions i Migracions**")

    X = df[["Població", "RFDH", "Naixements", "Defuncions", "Migracions internes", "Migracions externes", "Pensionistes"]]
    y = df[["Aturats"]]

    model = LinearRegression().fit(X, y)
    pred = model.predict(X)

    coeficients = pd.DataFrame({
        "Variable": X.columns,
        "Coeficient": model.coef_[0]
    })
    intercept = model.intercept_

    r2 = model.score(X, y)

    files_extres = pd.DataFrame({
            "Variable":["Intercept", "R2"],
            "Coeficient":[intercept[0], r2]
    })
    df_final = pd.concat([coeficients, files_extres], ignore_index=True)
    
    st.dataframe(df_final, hide_index=True)

    df_plot = df[['Aturats']]
    df_plot['Predicció'] = pred

    fig = px.line(df_plot,
                  title="Predicció de Aturats amb model de Regressió Múltiple"
                  )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    
    st.space('small')
    
    # Predicció del nombre de RFDH segons Població, Naixements, Defuncions, Migracions, Aturats i Pensionistes
    
    st.write("**Model de Regressió Múltiple de RFDH segons Població, Aturats, Pensionistes, Naixements, Defuncions i Migracions**")

    
    X = df[["Població", "Naixements", "Defuncions", "Migracions internes", "Migracions externes", "Aturats", "Pensionistes"]]
    y = df[["RFDH"]]

    model = LinearRegression().fit(X, y)
    pred = model.predict(X)

    coeficients = pd.DataFrame({
        "Variable": X.columns,
        "Coeficient": model.coef_[0]
    })
    intercept = model.intercept_

    r2 = model.score(X, y)

    files_extres = pd.DataFrame({
            "Variable":["Intercept", "R2"],
            "Coeficient":[intercept[0], r2]
    })
    df_final = pd.concat([coeficients, files_extres], ignore_index=True)
    
    st.dataframe(df_final, hide_index=True)

    df_plot = df[['RFDH']]
    df_plot['Predicció'] = pred

    fig = px.line(df_plot,
                  title="Predicció de RFDH amb model de Regressió Múltiple"
                  )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    
    st.space('small')
    
    # Prediccions amb ARIMA
    
    st.subheader("Prediccions amb ARIMA")
    
    # Prediccions de Població al futur amb ARIMA
    
    st.write("**Predicció de la Població fins al 2030 amb ARIMA**")
    
    s = df["Població"]        # variable a predir
    s.index = pd.to_datetime(s.index, format="%Y")   # convertir anys a dates

    model = ARIMA(s, order=(1,1,1))   # ARIMA(p,d,q)
    fit = model.fit()
    st.write(fit.summary())

    pred = fit.forecast(steps=6)
    
    s_real = s.rename("Real")
    s_pred = pred.rename("Predicció")
    df_plot = pd.concat([s_real, s_pred], axis=1)

    fig = px.line(df_plot, title="Predicció ARIMA de la població")
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    
    st.space('small')
    
    # Prediccions de RFDH al futur amb ARIMA
    
    st.write("**Predicció de RFDH fins al 2030 amb ARIMA**")
    
    s = df["RFDH"]        # variable a predir
    s.index = pd.to_datetime(s.index, format="%Y")   # convertir anys a dates

    model = ARIMA(s, order=(1,1,1))   # ARIMA(p,d,q)
    fit = model.fit()
    st.write(fit.summary())

    pred = fit.forecast(steps=6)

    s_real = s.rename("Real")
    s_pred = pred.rename("Predicció")
    df_plot = pd.concat([s_real, s_pred], axis=1)

    fig = px.line(df_plot, title="Predicció ARIMA de RFDH")
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)
    
    st.space('small')
    
    # Prediccions de Naixements acabats al futur amb ARIMA
    
    st.write("**Predicció de Naixements fins al 2030 amb ARIMA**")
    
    s = df["Naixements"]        # variable a predir
    s.index = pd.to_datetime(s.index, format="%Y")   # convertir anys a dates

    model = ARIMA(s, order=(1,1,1))   # ARIMA(p,d,q)
    fit = model.fit()
    st.write(fit.summary())

    pred = fit.forecast(steps=6)

    s_real = s.rename("Real")
    s_pred = pred.rename("Predicció")
    df_plot = pd.concat([s_real, s_pred], axis=1)

    fig = px.line(df_plot, title="Predicció ARIMA de naixements")
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig)

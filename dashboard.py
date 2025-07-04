import streamlit as st
import quantstats as qs
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Tracking Fundos",
    layout="wide",        # <-- aqui faz a mágica!
    initial_sidebar_state="auto"
)

st.title("Tracking Fundos")

# Carrega o CSV com todas as colunas de fundos
df = pd.read_csv("funds_return.csv", index_col=0)
df.index = pd.to_datetime(df.index)
cdi = pd.read_csv("cdi_return.csv", index_col=0, parse_dates=True).sort_index()

# Seleção do fundo via dropdown
fundos = df.columns.tolist()
fundo_escolhido = st.selectbox("Selecione o fundo para análise:", fundos)

# Prepara a série de retornos do fundo escolhido
serie = df[fundo_escolhido].replace("#VALUE!",np.nan).dropna().astype(float)
serie = serie.sort_index()
serie = serie[~serie.index.duplicated(keep='first')]

st.subheader(f"Métricas: {fundo_escolhido}")

qs.reports.html(serie, cdi.loc[serie.index], rf=((1+cdi.loc[serie.index]).cumprod()-1)['CDI'][-1],output="relatorio.html",periods_per_year=len(serie.index), title=f"Relatório - {fundo_escolhido}")
with open("relatorio.html", "r", encoding="utf-8") as f:
    html = f.read()
st.components.v1.html(html, height=900, scrolling=True)
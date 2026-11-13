import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Dashboard du trafic aérien")


@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
    df = pd.read_csv(url)
    
    ordre = {m: i + 1 for i, m in enumerate(df["month"].unique())}
    df["date"] = pd.to_datetime(
        {"year": df["year"], "month": df["month"].map(ordre), "day": 1}
    )
    return df


df = load_data()
mois_ordonnes = df["month"].unique().tolist()

annee_min, annee_max = int(df["year"].min()), int(df["year"].max())
plage = st.slider("Plage d'années :", annee_min, annee_max, (annee_min, annee_max))
mois = st.selectbox("Mois :", ["Tous les mois"] + mois_ordonnes)

df_filtre = df[df["year"].between(plage[0], plage[1])]
if mois != "Tous les mois":
    df_filtre = df_filtre[df_filtre["month"] == mois]


total = int(df_filtre["passengers"].sum())
st.metric("Total de passagers sur la période", f"{total:,}".replace(",", " "))

st.subheader("Aperçu des données")
st.dataframe(df_filtre[["year", "month", "passengers"]])

st.subheader("Évolution du nombre de passagers")
fig_line = px.line(df_filtre, x="date", y="passengers", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# --- Heatmap (Seaborn) ---
if st.checkbox("Afficher la heatmap année / mois"):
    pivot = df_filtre.pivot(index="month", columns="year", values="passengers")
    pivot = pivot.reindex([m for m in mois_ordonnes if m in pivot.index])

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    st.pyplot(fig)
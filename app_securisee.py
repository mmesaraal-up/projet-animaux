import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="App sécurisée", page_icon="🔒")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

@st.cache_data
def load_accounts():
    return pd.read_csv("accounts.csv")


def authenticate(username_input, password_input):
    accounts_df = load_accounts()
    match = accounts_df[
        (accounts_df["name"] == username_input)
        & (accounts_df["password"].astype(str) == password_input)
    ]
    return not match.empty



if not st.session_state["logged_in"]:
    st.title("🔒 Connexion à l'Application")
    st.subheader("Veuillez vous identifier pour accéder au contenu")

    username_input = st.text_input("Nom d'utilisateur")
    password_input = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if authenticate(username_input, password_input):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
else:
    with st.sidebar:
        st.write(f"👋 Bienvenue, **{st.session_state['username']}** !")
        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()
        st.divider()
        selected_page = option_menu(
            menu_title="Menu principal",
            options=["Accueil", "Galerie Photos"],
            icons=["house", "images"],
            default_index=0,
        )

    if selected_page == "Accueil":
        st.title("🏠 Page d'Accueil Réservée")
        st.write("Ce contenu est uniquement accessible aux utilisateurs authentifiés.")

   elif selected_page == "Galerie Photos":
        st.title("🐾 Galerie Photos")
        st.write("Voici la galerie avec mes animaux :")

        photos = [
            {"fichier": "images/90025a2f483f1f4230464b03a61b5d77.jpg", "legende": "Mon chien développeur"},
            {"fichier": "images/chat-mangeant-du-poisson-griffonne_79603-534.avif", "legende": "Le chat et le poisson"},
            {"fichier": "images/husky.jpg", "legende": "Husky de Noël"},
            {"fichier": "images/quokka.jpg", "legende": "Quokka"},
            {"fichier": "images/Rock'n Roll.jpg", "legende": "Rock'n Roll"},
        ]

        cols = st.columns(3)
        for idx, photo in enumerate(photos):
            with cols[idx % 3]:
                st.image(photo["fichier"], caption=photo.get("legende"), use_container_width=True)

import streamlit as st
from pages_st.login import login
from pages_st.registration import cadastro
from pages_st.home import home
from pages_st.enter_data import Inserir_novos_dados
from pages_st.reports import relatorios
from pages_st.support import suporte
from pages_st.settings import configuracoes

#   Página de login inicialmente
if "page" not in st.session_state:
        st.session_state.page = "login"

 #   Se o usuário não estiver logado, exibe a tela de login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
        if st.session_state.page == "login":
            login() 
        elif st.session_state.page == "cadastro":
            cadastro()

#   Caso esteja logado:
else:
    st.set_page_config(page_title="Waste Track", layout="wide")

        #   Barra lateral de menu
    with st.sidebar:
        st.image("utils\logo_wastetrack.png", width=150)

        st.title("Menu")

        if st.button("Home"):
                st.session_state.page = "home"

        if st.button("Inserir Novos Dados"):
                st.session_state.page = "dashboard"

        if st.button("Relatórios"):
                st.session_state.page = "relatorios"

        if st.button("Suporte ao Usuário"):
                st.session_state.page = "suporte"
                
        if st.button("Configurações"):
                st.session_state.page = "configuracoes"

        #   Redirecionamentos
    if st.session_state.page == "home":
            home()
    elif st.session_state.page == "dashboard":
            Inserir_novos_dados()
    elif st.session_state.page == "relatorios":
            relatorios()
    elif st.session_state.page == "suporte":
            suporte()
    elif st.session_state.page == "configuracoes":
            configuracoes()
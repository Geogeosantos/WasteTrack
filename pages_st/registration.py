import streamlit as st

def cadastro():
        st.title("Cadastro")
        
        st.write("Por favor, preencha os campos abaixo para criar uma nova conta.")
        
        username_new = st.text_input("Nome da empresa", key="cadastro_username")
        email_new = st.text_input("E-mail", key="cadastro_email")
        password_new = st.text_input("Senha", type="password", key="cadastro_password")
        confirm_password = st.text_input("Confirmar Senha", type="password", key="cadastro_confirm_password")

        if password_new != confirm_password:
            st.error("As senhas não coincidem. Tente novamente.")
        
        if st.button("Cadastrar"):
            if username_new and password_new and password_new == confirm_password:
                st.success("Cadastro realizado com sucesso!")
                st.session_state.page = "login"  
                st.error("Preencha todos os campos corretamente.")


        if st.button("Voltar para Login"):
            st.session_state.page = "login"  
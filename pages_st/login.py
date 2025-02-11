import streamlit as st



def login():
        st.image("utils\logo_wastetrack.png", width=150)
        st.title("Login")
        
        st.write("Por favor, insira suas credenciais para acessar o sistema.")
        
        email = st.text_input("E-mail", key="login_email")
        password = st.text_input("Senha", type="password", key="login_password")

        if st.button("Entrar"):
            if email == "celsaobrabo" and password == "Celsomeda10":  
                st.session_state.logged_in = True
                st.success("Login realizado com sucesso!")
                st.session_state.page = "home"
                
            else:
                st.error("Usuário ou senha incorretos. Tente novamente.")
        
        if st.button("Cadastrar-se"):
            st.session_state.page = "cadastro"

import streamlit as st
import time

def configuracoes():
    
    def alterar_nome_usuario():
        nome_usuario = st.text_input("Novo nome de usuário", value=st.session_state.get("nome_usuario", ""))
        if st.button("Salvar nome de usuário"):
            st.session_state["nome_usuario"] = nome_usuario
            st.success("Nome de usuário alterado com sucesso!")

    def alterar_foto_perfil():
        foto_perfil = st.file_uploader("Escolha uma nova foto de perfil", type=["jpg", "jpeg", "png"])
        if foto_perfil is not None:
            st.image(foto_perfil, width=100)
            if st.button("Salvar foto de perfil"):
                st.session_state["foto_perfil"] = foto_perfil
                st.success("Foto de perfil alterada com sucesso!")

    def alterar_email():
        email = st.text_input("Novo e-mail", value=st.session_state.get("email", ""))
        if st.button("Salvar e-mail"):
            st.session_state["email"] = email
            st.success("Email alterado com sucesso!")

    def alterar_senha():
        nova_senha = st.text_input("Nova senha", type="password")
        confirmar_senha = st.text_input("Confirme a nova senha", type="password")
        if nova_senha == confirmar_senha:
            if st.button("Alterar senha"):
                st.session_state["senha"] = nova_senha
                st.success("Senha alterada com sucesso!")
        else:
            st.warning("As senhas não coincidem!")

    def confirmar_identidade():
        senha_confirmacao = st.text_input("Digite sua senha para confirmar", type="password")
        if senha_confirmacao == st.session_state.get("senha", ""):
            st.success("Identidade confirmada com sucesso!")
        else:
            st.warning("Senha incorreta!")

    def excluir_conta():
        if st.button("Excluir minha conta"):
            with st.spinner("Excluindo sua conta..."):
                    time.sleep(2)  
                    st.session_state.clear()
                    st.success("Conta excluída com sucesso!")

    def ativar_2fa():
        ativar_2fa = st.checkbox("Ativar autenticação de dois fatores")
        if st.button("Salvar configuração de 2FA"):
            st.session_state["2fa"] = ativar_2fa
            st.success("Autenticação de dois fatores ativada!" if ativar_2fa else "Autenticação de dois fatores desativada.")

    def alterar_pergunta_seguranca():
        pergunta = st.text_input("Pergunta de segurança", value=st.session_state.get("pergunta_seguranca", ""))
        resposta = st.text_input("Resposta de segurança", type="password", value=st.session_state.get("resposta_seguranca", ""))
        if st.button("Salvar pergunta de segurança"):
            st.session_state["pergunta_seguranca"] = pergunta
            st.session_state["resposta_seguranca"] = resposta
            st.success("Pergunta e resposta de segurança alteradas com sucesso!")

    def alterar_senha_seguranca():
        nova_senha = st.text_input("Nova senha de segurança", type="password")
        confirmar_senha = st.text_input("Confirme a nova senha de segurança", type="password")
        if nova_senha == confirmar_senha:
            if st.button("Alterar senha de segurança"):
                st.session_state["senha_seg"] = nova_senha
                st.success("Senha de segurança alterada com sucesso!")
        else:
            st.warning("As senhas não coincidem!")
            
    st.title("Configurações Gerais")
    
    st.subheader("Configurações de Usuário")
    configuracao_geral = st.selectbox(
        "Escolha uma ação", 
        ["Alterar nome de usuário", "Alterar foto de perfil", "Alterar email vinculado", "Confirmar identidade", "Excluir conta"]
    )
    
    if configuracao_geral == "Alterar nome de usuário":
        alterar_nome_usuario()
    elif configuracao_geral == "Alterar foto de perfil":
        alterar_foto_perfil()
    elif configuracao_geral == "Alterar email vinculado":
        alterar_email()
    elif configuracao_geral == "Confirmar identidade":
        confirmar_identidade()
    elif configuracao_geral == "Excluir conta":
        excluir_conta()

    st.subheader("Privacidade e Segurança")
    privacidade_seg = st.selectbox(
        "Escolha uma opção", 
        ["Ativar 2FA", "Alterar pergunta de segurança", "Alterar senha de segurança"]
    )
    
    if privacidade_seg == "Ativar 2FA":
        ativar_2fa()
    elif privacidade_seg == "Alterar pergunta de segurança":
        alterar_pergunta_seguranca()
    elif privacidade_seg == "Alterar senha de segurança":
        alterar_senha_seguranca()

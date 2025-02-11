import streamlit as st
import time
import pandas as pd

def suporte():

    def exibir_feedback(status):
        if status == "Enviado":
            return "🔵", "blue"
        elif status == "Respondido":
            return "✅", "green"
        elif status == "Em Progresso":
            return "🕑", "orange"
        return "❓", "gray"
    
    st.title("Suporte ao Usuário")
    st.write("Descreva seu problema ou solicite ajuda.")

    if "chamados" not in st.session_state:
        st.session_state.chamados = [] 

    with st.container():
        col1, col2 = st.columns([3, 2])  

        with col1:
            st.subheader("Criar Chamado")
            relato = st.text_area("Descreva seu problema", placeholder="Digite seu relato aqui...", height=150)
            email = st.text_input("Email para contato", placeholder="exemplo@dominio.com")

            if st.button("Enviar"):
                if relato and email:
                    with st.spinner('Enviando chamado...'):
                        time.sleep(2) 
                    
                    chamado = {
                        "Descrição": relato,
                        "Email": email,
                        "Status": "Enviado"
                    }
                    st.session_state.chamados.append(chamado)
                    st.success("Chamado enviado com sucesso!")
                else:
                    st.error("Por favor, preencha todos os campos antes de enviar.")

        with col2:
            st.subheader("Gerenciar Chamados")
            options = ["Todos", "Rascunho", "Enviados", "Respondidos"]
            selected_option = st.selectbox("Selecione uma categoria", options, index=2)

            if selected_option == "Todos":
                filtered_chamados = st.session_state.chamados
            else:
                filtered_chamados = [
                    chamado for chamado in st.session_state.chamados if chamado["Status"] == selected_option
                ]

            if filtered_chamados:
                st.write(f"Exibindo chamados da categoria: **{selected_option}**")
                df_chamados = pd.DataFrame(filtered_chamados)

                for index, row in df_chamados.iterrows():
                    icon, color = exibir_feedback(row["Status"])
                    st.markdown(f"<p style='color:{color};'>{icon} {row['Descrição']} ({row['Status']})</p>", unsafe_allow_html=True)

                st.dataframe(df_chamados, use_container_width=True)

                st.download_button(
                    label="Baixar Chamados",
                    data=df_chamados.to_csv(index=False),
                    file_name="chamados.csv",
                    mime="text/csv"
                )
            else:
                st.write(f"Não há chamados na categoria **{selected_option}**.")

import streamlit as st

def home():
    st.title("Waste Track")
    st.subheader("Gerenciador de Resíduos Sólidos")
    st.write("Bem-vindo ao sistema Waste Track. Use o menu lateral para navegar pelas funcionalidades.")
    

    st.markdown("""
        <style>
            video {
                width: 200px;
                height: 800px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    #   Vídeo sobre o descarte de lixo e reciclagem
    st.video("utils\\video_inicia.mp4")
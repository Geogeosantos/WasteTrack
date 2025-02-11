import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector


def relatorios():
    st.title("Relatórios")

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Geovany321alves!",
            database="wastetrack"
        )
        cursor = conexao.cursor()

        cursor.execute("SHOW TABLES")
        tabelas = [tabela[0] for tabela in cursor.fetchall()]

        if not tabelas:
            st.warning("Nenhum relatório disponível no banco de dados.")

            return

        st.write("Seleção de Relatórios")
        tabela_selecionada = st.selectbox("Escolha uma tabela:", tabelas)

        if tabela_selecionada:
            query = f"SELECT * FROM `{tabela_selecionada}`"
            df = pd.read_sql(query, conexao)

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"Dados do Relatório: {tabela_selecionada}")
                st.dataframe(df)

            with col2:
                st.write("Resumo Estatístico")
                st.write(df.describe())

            st.write("Gráficos")
            gerar_graficos(df)

        cursor.close()
        conexao.close()

    except mysql.connector.Error as e:
        st.error(f"Erro ao interagir com o banco de dados: {e}")


def gerar_graficos(df):
    st.write("### Gráficos Gerados com os Dados")

    numeric_columns = df.select_dtypes(include=["number"]).columns
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns


    col1, col3, col5 = st.columns(3)

    with col1:
        if len(numeric_columns) >= 1:
            st.write("Histograma")
            fig = px.histogram(df, x=numeric_columns[0])
            st.plotly_chart(fig, use_container_width=True)

    with col3:
        if len(categorical_columns) >= 1 and len(numeric_columns) >= 1:
            st.write("Barras")
            fig = px.bar(df, x=categorical_columns[0], y=numeric_columns[0])
            st.plotly_chart(fig, use_container_width=True)
    with col5:
            if len(categorical_columns) >= 1:
                st.write("Boxplot")
                fig = px.box(df, x=categorical_columns[0], y=numeric_columns[0])
                st.plotly_chart(fig, use_container_width=True)


    col7, col8 = st.columns(2)

    with col7:
        if len(categorical_columns) >= 2:
            st.write("Gráfico de Torta")
            fig = px.pie(df, names=categorical_columns[0], values=numeric_columns[0])
            st.plotly_chart(fig, use_container_width=True)

    with col8:
        if len(numeric_columns) >= 1:
            st.write("Violin Plot")
            fig = px.violin(df, y=numeric_columns[0])
            st.plotly_chart(fig, use_container_width=True)

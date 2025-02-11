import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd


#   Conectar o banco d
#  dados
def conectar_banco():

    load_dotenv()

    try:
        conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )

        cursor = conexao.cursor()
        return conexao, cursor
    except mysql.connector.Error as e:
        return None, None, f"Erro ao conectar com o banco de dados: {e}"

#   Adiciona o aquivo CSV no banco de dados
def adicionar_dados(nome_tabela, df):

    try:
        conexao, cursor, erro = conectar_banco()
        if erro:
            return erro

        #   Cria uma query para a tabela que em que vai salvar o arquivo
        colunas_query = ", ".join([f"{col} VARCHAR(255)" for col in df.columns])
        query_criar_tabela = f"""
                             CREATE TABLE IF NOT EXISTS {nome_tabela} 
                             (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                {colunas_query}
                             )
                              """
        #   Roda a query para criar a tabela
        cursor.execute(query_criar_tabela)

        #   Insere os dados na tabela criada
        for _, row in df.iterrows():
            valores = tuple(row)
            placeholders = ", ".join(["%s"] * len(valores))
            query_inserir = f"INSERT INTO {nome_tabela} ({', '.join(df.columns)}) VALUES ({placeholders})"
            cursor.execute(query_inserir, valores)

        conexao.commit()

        #   Fecga a conexao
        conexao.close()

        return True
    except Exception as e:
        return f"Erro ao conectar com o banco de dados: {e}"



# Obtêm os arquivos csv do banco
def obter_relatorios_do_banco():

    try:
        conexao, cursor, erro = conectar_banco()
        if erro:
            return erro
        
        #   Cria uma query para buscar o nome do arquivo no banco
        query = "SELECT nome_arquivo FROM relatorios"  
        cursor.execute(query)
        
        arquivos = cursor.fetchall()
        conexao.close()

        # Retorna os nomes dosarquivos
        return [arquivo[0] for arquivo in arquivos] if arquivos else []
    
    except mysql.connector.Error as e:
        return f"Erro ao buscar relatórios no banco de dados: {e}"


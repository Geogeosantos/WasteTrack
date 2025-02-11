import streamlit as st
import supervision as sv
import pandas as pd
import cv2
from datetime import datetime
from ultralytics import YOLO
import mysql.connector

from pages_st.database import adicionar_dados


def Inserir_novos_dados():

    #   Função que inicia a detecção pela câmera
    def run_yolov8(stop_flag, placeholder, detections_log, detection_count):
        model = YOLO("utils\\yolov8l.pt")
        box_annotator = sv.BoxAnnotator(
            thickness=2,        
            text_thickness=2,   
            text_scale=1,       
        )

        
        cap = cv2.VideoCapture(0) #Obs: Caso esteja usando uma câmera externa, coloque o valor 1, 
                                  #mas caso esteja usando a própria câmera do notebook, mantenha com o valor 0

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, agnostic_nms=True)[0]
            detections = sv.Detections.from_yolov8(results)

            for i, confidence, class_id, i in detections:
                class_name = model.model.names[class_id]
                detection_count[class_name] = detection_count.get(class_name, 0) + 1

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                detections_log.append({
                    "Item": class_name,
                    "Confiança": confidence,
                    "Tempo": timestamp,
                    "Classe": class_id
                })

            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for i, confidence, class_id, i in detections
            ]
            
            frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized_frame = cv2.resize(frame_rgb, (960, 540)) 
            placeholder.image(resized_frame, channels="RGB", use_container_width=False)

            if stop_flag():
                break

        cap.release()

    st.title("Inserir Novos Dados")

    detection_active = st.session_state.get("detection_active", False)

    if "detections_log" not in st.session_state:
        st.session_state.detections_log = []

    if "detection_count" not in st.session_state:
        st.session_state.detection_count = {}

    st.write("### Visualização de Detecção")
    with st.container():
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            placeholder = st.empty()

            if detection_active:
                if st.button("Parar Detecção", use_container_width=True):
                    st.session_state.detection_active = False
                run_yolov8(lambda: not st.session_state.detection_active, placeholder, st.session_state.detections_log, st.session_state.detection_count)
            else:
                placeholder.markdown(
                    """
                    <div style="background-color: black; width: 960px; height: 540px; margin: auto; border-radius: 8px;">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Iniciar Detecção", use_container_width=True):
                    st.session_state.detection_active = True

    st.write("### Log de Detecções")
    if st.session_state.detections_log:
        detection_data = pd.DataFrame(st.session_state.detections_log)

        detection_data['Quantidade'] = detection_data.groupby('Item')['Item'].transform('count')

        st.dataframe(detection_data)

        csv = detection_data.to_csv(index=False)
        st.download_button("Baixar Relatório", csv, "relatorio_detecoes.csv", "text/csv")
    else:
        st.write("Nenhuma detecção reali_zada ainda.")

    st.write("### Gráfico de Itens Detectados ao Longo do Tempo")
    if st.session_state.detections_log:
        df = pd.DataFrame(st.session_state.detections_log)
        df['Tempo'] = pd.to_datetime(df['Tempo'])
        
        item_count_over_time = df.groupby([df['Tempo'], 'Item']).size().reset_index(name='Quantidade')

        chart_data = item_count_over_time.pivot_table(index='Tempo', columns='Item', values='Quantidade', aggfunc='sum').fillna(0)
        st.line_chart(chart_data)

    st.title("Inserir Dados através de um Arquivo CSV")

    st.title("Inserir Novos Dados")

    st.write("### Inserção de Dados via Arquivo CSV")
    arquivo_csv = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if arquivo_csv:
        df = pd.read_csv(arquivo_csv)
        st.write("Dados carregados:")
        st.dataframe(df)

        nome_tabela = st.text_input("Nome da Tabela:", value="nova_tabela")

        if st.button("Inserir Dados no Banco"):
            try:
                conexao = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Geovany321alves!",
                    database="wastetrack"
                )
                cursor = conexao.cursor()

                colunas_query = ", ".join([f"`{col}` VARCHAR(255)" for col in df.columns])
                query_criar_tabela = f"""
                CREATE TABLE IF NOT EXISTS `{nome_tabela}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    {colunas_query}
                )
                """
                cursor.execute(query_criar_tabela)

                for i, row in df.iterrows():
                    valores = tuple(row)
                    placeholders = ", ".join(["%s"] * len(valores))
                    query_inserir = f"INSERT INTO `{nome_tabela}` ({', '.join(df.columns)}) VALUES ({placeholders})"
                    cursor.execute(query_inserir, valores)

                conexao.commit()
                cursor.close()
                conexao.close()
                st.success(f"Tabela '{nome_tabela}' criada e preenchida com sucesso!")

            except mysql.connector.Error as e:
                st.error(f"Erro ao interagir com o banco de dados: {e}")


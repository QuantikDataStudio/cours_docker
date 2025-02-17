import streamlit as st
import psycopg2
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from datetime import datetime
import pathlib
import os

DATABASE_URL = os.getenv('DATABASE_URL')

def init_connection():
        return psycopg2.connect(DATABASE_URL)

def save_analysis(filename, report_path):
    with init_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO analyses (filename, timestamp, report_path) VALUES (%s, %s, %s) RETURNING id",
                (filename, datetime.now(), report_path)
            )
            conn.commit()
            return cur.fetchone()[0]

def get_analyses():
     return run_query("SELECT id, filename, timestamp, report_path FROM analyses ORDER BY timestamp DESC")

def run_query(query):
    with init_connection() as conn:
        return pd.read_sql_query(query, conn)
    
menu = st.sidebar.radio(
    "Navigation",
    ["Upload et Analyse", "Analyses Historiques", "Info Base de données"]
)

if menu == "Upload et Analyse":
    st.header("Upload et Analyse")
    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])
    
    if uploaded_file is not None:
        try:
            encodings = ["utf-8", "latin1", "iso-8859-1", "cp1252"]
            df = None
            for encoding in encodings:
                try:
                    df = pd.read_csv(uploaded_file, encoding=encoding)
                    st.success("l'encoding est trouvé")
                    break
                except UnicodeDecodeError:
                    continue
            if df is None:
                st.write("le df n'a pas pu être lu")
                st.stop()

            st.write(df.head())
            # Generation du rapport
            with st.spinner("generation du rapport en cours ..."):
                filename = uploaded_file.name
                profile = ProfileReport(df, title=f"Rapport d'analyse - {filename}", minimal=True)
                st_profile_report(profile)

                #sauvarge du rapport
                timestamp = datetime.now().strftime('%Y%m%d_%H%m%S_%f')
                report_dir = pathlib.Path("analyses") / timestamp
                report_dir.mkdir(parents=True, exist_ok=True)
                report_path = report_dir / "report.html"

                profile.to_file(str(report_path))

                # enregistrement dans la bdd
                
                analysis_id = save_analysis(filename, str(report_path))
                st.success(f"Analyse complete et enregistré id : ‘{analysis_id}")
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

elif menu == "Analyses Historiques":
    st.header("Analyses Historiques")
    try:
        analyses_df = get_analyses()
        if not analyses_df.empty:
            for _, row in analyses_df.iterrows():
                with st.expander(f"Analyse de { row['filename']} - {row['timestamp']}"):
                    st.write(f"ID: {row['id']}")
                    st.write(f"PATH: {row['report_path']}")
                    if os.path.exists(row['report_path']):
                        with open(row['report_path'], 'r', encoding='utf-8') as f:
                            html_content = f.read()
                            # afficher le rapport
                            st.components.v1.html(html_content, height=500, scrolling=True )
                            st.download_button(label="Telecharge le rapport", data=html_content, file_name=f"rapport_analyse_{row['id']}.html",mime="text/html" )
                    else:
                        st.warning("Document introuvable")

        else: 
            st.write('Aucun historique de rapport')
    except Exception as e:
         st.error(f"Une erreur de chargement est survenue : {e}")

else:
    st.header("Info Base de données")
    try:
        df = run_query('SELECT version();')
        st.write("Version de Postgres : ")
        st.write(df.iloc[0,0])
    except Exception as e:
        st.error(f"Une erreur c'est produite : {e}")
import streamlit as st
import pandas as pd
from app.confronto import confronta_clienti
import io

def carica_interfaccia():
    st.set_page_config(page_title="Comparatore SogeMI", layout="wide")

    st.title("🔍 Comparatore SogeMI")
    st.markdown("Confronta due elenchi anche se i nomi non sono identici.")

    # Caricamento file Excel
    file = st.file_uploader("📁 Carica un file Excel contenente entrambe le tabelle", type=["xlsx"])

    if file:
        with pd.ExcelFile(file) as xls:
            sheet_names = xls.sheet_names

        # Selezione dei fogli
        col1, col2 = st.columns(2)
        with col1:
            sheet1 = st.selectbox("📄 Seleziona foglio di calcolo 1", options=sheet_names)
        with col2:
            sheet2 = st.selectbox("📄 Seleziona foglio di calcolo 2", options=sheet_names)

        # Caricamento dati
        df1 = pd.read_excel(file, sheet_name=sheet1)
        df2 = pd.read_excel(file, sheet_name=sheet2)

        st.success("✅ Fogli caricati correttamente!")

        # Slider per la soglia
        soglia = st.slider("🎯 Soglia di similarità (%)", min_value=60, max_value=100, value=90, step=1)

        if st.button("🚀 Avvia confronto"):
            with st.spinner("Confronto in corso..."):
                risultati = confronta_clienti(df1, df2, soglia_similarita=soglia)

                def evidenzia(riga):
                    colore = "background-color: yellow" if riga["STATO"] == "NON TROVATO" else ""
                    return [colore] * len(riga)

                st.markdown("### 📊 Risultati del confronto")
                st.dataframe(risultati.style.apply(evidenzia, axis=1), use_container_width=True)

                st.markdown("### 💾 Esporta in Excel")
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    risultati.to_excel(writer, index=False)
                buffer.seek(0)

                st.download_button(
                    label="⬇️ Scarica risultati",
                    data=buffer,
                    file_name="risultati_confronto.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.info("📌 Carica un file per iniziare.")

# Debug
print("✅ interfaccia.py caricato correttamente")

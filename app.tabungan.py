import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Tabungan UTS", layout="centered")
st.title("💰 Tabungan Target (Google Drive)")

URL_SHEET = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet=URL_SHEET, ttl="0")

with st.sidebar:
    st.header("Tambah Data")
    with st.form("form_input"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target (Rp)", min_value=0)
        dana = st.number_input("Terkumpul (Rp)", min_value=0)
        submit = st.form_submit_button("Simpan ke Cloud")

        if submit and nama:
            new_row = pd.DataFrame([{"nama_barang": nama, "harga_target": harga, "nominal_terkumpul": dana}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("Berhasil Masuk Google Drive!")
            st.rerun()

st.subheader("Progres Tabungan Anda")
st.dataframe(df, use_container_width=True)

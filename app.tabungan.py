import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Tabungan UTS", layout="centered")
st.title("💰 Tabungan Target (Google Drive)")

# Link Google Sheets kamu
url = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

# Koneksi Gratis ke Drive
conn = st.connection("gsheets", type=GSheetsConnection)

# Baca data awal
df = conn.read(spreadsheet=url, ttl="0")

with st.sidebar:
    st.header("Tambah Data Baru")
    with st.form("input_form"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target (Rp)", min_value=0)
        dana = st.number_input("Terkumpul (Rp)", min_value=0)
        tgl = st.date_input("Deadline")
        submit = st.form_submit_button("Simpan ke Google Drive")

        if submit and nama:
            # Gabungkan data lama dengan data baru
            new_row = pd.DataFrame([{
                "nama_barang": nama, 
                "harga_target": harga, 
                "nominal_terkumpul": dana,
                "deadline": str(tgl)
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # Kirim balik ke Google Drive
            conn.update(spreadsheet=url, data=updated_df)
            st.success("Berhasil Masuk Drive!")
            st.rerun()

# Tampilkan daftar tabungan
st.subheader("Daftar Progres di Google Drive")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada data di Drive. Silakan tambah di samping.")

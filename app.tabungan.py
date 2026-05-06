import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Judul Aplikasi
st.title("💰 Tabungan UTS (Simpan ke Drive)")

# Link Google Sheets Anda (Pastikan sudah Akses: Editor)
url = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

# Koneksi Gratis
conn = st.connection("gsheets", type=GSheetsConnection)

# Baca Data
df = conn.read(spreadsheet=url, ttl="0")

with st.sidebar:
    st.header("Tambah Tabungan")
    with st.form("input_form"):
        nama = st.text_input("Barang")
        harga = st.number_input("Target Harga", min_value=0)
        dana = st.number_input("Dana Terkumpul", min_value=0)
        submit = st.form_submit_button("Simpan ke Google Drive")

        if submit and nama:
            # Masukkan data ke tabel
            new_data = pd.DataFrame([{"nama_barang": nama, "harga_target": harga, "nominal_terkumpul": dana}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            
            # Update ke Google Sheets
            conn.update(spreadsheet=url, data=updated_df)
            st.success("Tersimpan di Drive!")
            st.rerun()

# Tampilkan Daftar
st.write("### Daftar Progres di Drive")
st.dataframe(df)

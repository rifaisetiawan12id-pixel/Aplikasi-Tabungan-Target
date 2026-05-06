import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfigurasi Tampilan
st.set_page_config(page_title="Tabungan UTS - Mohammad", layout="centered")
st.title("💰 Aplikasi Tabungan Target")
st.write("Data ini tersimpan otomatis di Google Drive (Google Sheets).")

# URL Google Sheets kamu (Sudah benar dari gambar sebelumnya)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

# Inisialisasi Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fungsi Membaca Data
def load_data():
    return conn.read(spreadsheet=URL_SHEET, ttl="0")

df = load_data()

# --- INPUT DATA DI SIDEBAR ---
with st.sidebar:
    st.header("Tambah Tabungan Baru")
    with st.form("input_form"):
        nama_barang = st.text_input("Nama Barang/Tujuan")
        harga_target = st.number_input("Target Harga (Rp)", min_value=0, step=1000)
        nominal_sekarang = st.number_input("Uang Terkumpul (Rp)", min_value=0, step=1000)
        
        submit_button = st.form_submit_button("Simpan ke Cloud")

        if submit_button and nama_barang:
            # Membuat baris data baru
            new_data = pd.DataFrame([{
                "nama_barang": nama_barang,
                "harga_target": harga_target,
                "nominal_terkumpul": nominal_sekarang
            }])
            
            # Menggabungkan data lama dengan yang baru
            updated_df = pd.concat([df, new_data], ignore_index=True)
            
            # Update ke Google Sheets
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("Data berhasil disimpan ke Drive!")
            st.rerun()

# --- TAMPILAN UTAMA ---
st.subheader("Daftar Target Tabungan")
if not df.empty:
    # Menampilkan tabel data
    st.dataframe(df, use_container_width=True)
    
    # Tambahan: Hitung Total
    total_tabungan = df['nominal_terkumpul'].sum()
    st.metric("Total Semua Tabungan", f"Rp {total_tabungan:,}")
else:
    st.info("Belum ada data. Silakan isi di menu sebelah kiri.")

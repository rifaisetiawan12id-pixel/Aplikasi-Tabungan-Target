import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Tabungan Target", layout="centered")
st.title("💰 Tabungan Target (Saving Goals)")

# URL Spreadsheet kamu
URL_SHEET = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- READ DATA ---
try:
    # Membaca data berdasarkan header yang kamu buat di gambar
    df = conn.read(spreadsheet=URL_SHEET)
except:
    df = pd.DataFrame(columns=["nama_barang", "harga_target", "nominal_terkumpul", "deadline"])

# --- CREATE DATA (Input) ---
with st.sidebar:
    st.header("Tambah Target")
    with st.form("tambah_form"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target (Rp)", min_value=0)
        terkumpul = st.number_input("Nominal Terkumpul (Rp)", min_value=0)
        tgl_deadline = st.date_input("Deadline")
        submit = st.form_submit_button("Simpan ke Drive")

        if submit and nama:
            # Membuat baris baru
            new_row = pd.DataFrame([{
                "nama_barang": nama, 
                "harga_target": harga, 
                "nominal_terkumpul": terkumpul, 
                "deadline": str(tgl_deadline)
            }])
            # Menggabungkan data
            updated_df = pd.concat([df, new_row], ignore_index=True)
            # Update ke Google Sheets
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("Data tersimpan!")
            st.rerun()

# --- DISPLAY DATA ---
st.subheader("Progres Tabungan")
if not df.empty:
    for index, row in df.iterrows():
        # Logika Persentase
        target = float(row["harga_target"])
        dana = float(row["nominal_terkumpul"])
        persen = (dana / target) if target > 0 else 0
        
        st.write(f"**{row['nama_barang']}**")
        st.progress(min(persen, 1.0))
        st.caption(f"Tercapai: {persen*100:.1f}% | Sisa: Rp {target - dana:,.0f}")
        st.divider()
else:
    st.info("Belum ada data di Google Sheets.")

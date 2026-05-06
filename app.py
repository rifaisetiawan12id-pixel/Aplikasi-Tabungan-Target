import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Saving Goals", layout="centered")
st.title("💰 Tabungan Target (Saving Goals)")

# Link Spreadsheet kamu
URL_SHEET = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fungsi untuk membaca data
def load_data():
    try:
        return conn.read(spreadsheet=URL_SHEET)
    except:
        return pd.DataFrame(columns=["Barang", "Target", "Terkumpul", "Deadline"])

df = load_data()

# --- INPUT DATA (CREATE) ---
with st.sidebar:
    st.header("Tambah Target Baru")
    with st.form("input_form"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target (Rp)", min_value=0)
        dana = st.number_input("Nominal Terkumpul (Rp)", min_value=0)
        deadline = st.date_input("Tenggat Waktu")
        submit = st.form_submit_button("Simpan Target")

        if submit and nama:
            new_row = pd.DataFrame([{"Barang": nama, "Target": harga, "Terkumpul": dana, "Deadline": str(deadline)}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("Berhasil disimpan!")
            st.rerun()

# --- TAMPILAN PROGRES (READ) ---
st.subheader("Daftar Pencapaian")
if not df.empty:
    for index, row in df.iterrows():
        # Logika Persentase
        target = float(row["Target"])
        terkumpul = float(row["Terkumpul"])
        persen = (terkumpul / target) if target > 0 else 0
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{row['Barang']}**")
            st.progress(min(persen, 1.0))
        with col2:
            st.write(f"{persen*100:.1f}%")
        
        # Logika Sisa Hari
        tgl_target = datetime.strptime(row["Deadline"], "%Y-%m-%d")
        sisa_hari = (tgl_target - datetime.now()).days
        if sisa_hari > 0:
            sisa_uang = target - terkumpul
            per_hari = sisa_uang / sisa_hari
            st.caption(f"Sisa waktu: {sisa_hari} hari. Nabung Rp {per_hari:,.0f}/hari untuk capai target.")
        st.divider()
else:
    st.info("Belum ada data. Silakan tambah di sidebar.")

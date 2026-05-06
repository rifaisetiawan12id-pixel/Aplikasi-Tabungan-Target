import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfigurasi Judul
st.title("💰 Tabungan Target (Saving Goals)")

# URL Spreadsheet dari Google Drive kamu
URL_SHEET = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- READ DATA ---
try:
    # Membaca data berdasarkan header di image_adea9a.png
    df = conn.read(spreadsheet=URL_SHEET)
except:
    df = pd.DataFrame(columns=["nama_barang", "harga_target", "nominal_terkumpul", "deadline"])

# --- CREATE DATA (Input) ---
with st.sidebar:
    st.header("Input Target Baru")
    with st.form("tambah_target"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target (Rp)", min_value=0)
        dana = st.number_input("Dana Terkumpul (Rp)", min_value=0)
        tgl = st.date_input("Deadline")
        submit = st.form_submit_button("Simpan ke Cloud Drive")

        if submit and nama:
            new_row = pd.DataFrame([{
                "nama_barang": nama, 
                "harga_target": harga, 
                "nominal_terkumpul": dana, 
                "deadline": str(tgl)
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("Data Berhasil Disimpan!")
            st.rerun()

# --- TAMPILAN PROGRES ---
st.subheader("Daftar Progres")
if not df.empty:
    for index, row in df.iterrows():
        target = float(row["harga_target"])
        terkumpul = float(row["nominal_terkumpul"])
        persen = (terkumpul / target) if target > 0 else 0
        
        st.write(f"**{row['nama_barang']}**")
        st.progress(min(persen, 1.0))
        st.caption(f"Progres: {persen*100:.1f}% | Sisa: Rp {target - terkumpul:,.0f}")
        st.divider()
else:
    st.info("Belum ada data di Google Sheets.")

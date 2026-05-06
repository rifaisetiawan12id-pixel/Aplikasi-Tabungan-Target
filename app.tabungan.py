import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfigurasi Tampilan
st.set_page_config(page_title="Tabungan Cloud UTS", layout="centered")
st.title("💰 Tabungan Target (API Cloud)")

# URL Spreadsheet (Database kamu)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

# Inisialisasi Koneksi API
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNGSI READ (Baca Data) ---
def ambil_data():
    try:
        return conn.read(spreadsheet=URL_SHEET)
    except:
        return pd.DataFrame(columns=["nama_barang", "harga_target", "nominal_terkumpul", "deadline"])

df = ambil_data()

# --- FUNGSI CREATE (Tambah Data via Sidebar) ---
with st.sidebar:
    st.header("Tambah Data Baru")
    with st.form("form_input"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target (Rp)", min_value=0)
        dana = st.number_input("Terkumpul (Rp)", min_value=0)
        tgl = st.date_input("Deadline")
        submit = st.form_submit_button("Simpan ke Cloud")

        if submit and nama:
            # Data baru dalam bentuk baris
            baris_baru = pd.DataFrame([{
                "nama_barang": nama, 
                "harga_target": harga, 
                "nominal_terkumpul": dana, 
                "deadline": str(tgl)
            }])
            # Gabungkan dengan data lama
            df_update = pd.concat([df, baris_baru], ignore_index=True)
            # Kirim data ke API Google Sheets
            conn.update(spreadsheet=URL_SHEET, data=df_update)
            st.success("Data Berhasil Masuk Cloud!")
            st.rerun()

# --- TAMPILAN PROGRES ---
st.subheader("📊 Daftar Progres Tabungan")
if not df.empty:
    for index, row in df.iterrows():
        target = float(row["harga_target"])
        terkumpul = float(row["nominal_terkumpul"])
        persen = (terkumpul / target) if target > 0 else 0
        
        st.write(f"**{row['nama_barang']}**")
        st.progress(min(persen, 1.0))
        st.caption(f"Tercapai: {persen*100:.1f}% | Sisa: Rp {max(target - terkumpul, 0):,.0f}")
        st.divider()
else:
    st.info("Aplikasi sudah terhubung API, silakan isi data di samping.")

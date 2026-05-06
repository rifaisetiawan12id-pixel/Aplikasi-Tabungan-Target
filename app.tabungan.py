import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Tabungan Target", layout="centered")
st.title("💰 Aplikasi Tabungan Target")

# Link Spreadsheet kamu
URL_SHEET = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

# Koneksi Database Cloud
conn = st.connection("gsheets", type=GSheetsConnection)

# --- READ DATA ---
def load_data():
    try:
        # Membaca data dari link sheet kamu
        return conn.read(spreadsheet=URL_SHEET)
    except:
        # Jika sheet kosong, buat kolom sesuai gambar image_adea9a.png
        return pd.DataFrame(columns=["nama_barang", "harga_target", "nominal_terkumpul", "deadline"])

df = load_data()

# --- INPUT DATA (CRUD: Create) ---
with st.sidebar:
    st.header("Tambah Target Baru")
    with st.form("input_form"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target (Rp)", min_value=0)
        terkumpul = st.number_input("Terkumpul (Rp)", min_value=0)
        deadline = st.date_input("Deadline")
        submit = st.form_submit_button("Simpan ke Cloud")

        if submit and nama:
            # Buat baris baru sesuai kolom di Google Sheets kamu
            new_row = pd.DataFrame([{
                "nama_barang": nama, 
                "harga_target": harga, 
                "nominal_terkumpul": terkumpul, 
                "deadline": str(deadline)
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            # Kirim data ke Cloud (Google Sheets)
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("Berhasil tersimpan di Google Sheets!")
            st.rerun()

# --- TAMPILAN PROGRES (CRUD: Read) ---
st.subheader("Daftar Progres Tabungan")
if not df.empty:
    for index, row in df.iterrows():
        try:
            target = float(row["harga_target"])
            dana = float(row["nominal_terkumpul"])
            persen = (dana / target) if target > 0 else 0
            
            with st.container():
                st.write(f"**{row['nama_barang']}**")
                st.progress(min(persen, 1.0))
                st.caption(f"Tercapai: {persen*100:.1f}% | Target: Rp {target:,.0f} | Sisa: Rp {max(target - dana, 0):,.0f}")
                st.divider()
        except:
            continue
else:
    st.info("Belum ada data. Silakan tambah target di menu samping.")

import streamlit as st
import pandas as pd
import os

# Nama file penyimpan data
FILE_DATA = "data_tabungan.csv"

st.set_page_config(page_title="Tabungan UTS", layout="centered")
st.title("💰 Tabungan Target (Local Data)")

# Fungsi Load Data
def load_data():
    if os.path.exists(FILE_DATA):
        return pd.read_csv(FILE_DATA)
    else:
        return pd.DataFrame(columns=["nama_barang", "harga_target", "nominal_terkumpul", "deadline"])

# Fungsi Simpan Data
def save_data(dataframe):
    dataframe.to_csv(FILE_DATA, index=False)

df = load_data()

# --- INPUT DATA (SIDEBAR) ---
with st.sidebar:
    st.header("Tambah Data")
    with st.form("form_input"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target (Rp)", min_value=0)
        dana = st.number_input("Terkumpul (Rp)", min_value=0)
        tgl = st.date_input("Deadline")
        submit = st.form_submit_button("Simpan Data")

        if submit and nama:
            new_row = pd.DataFrame([{
                "nama_barang": nama, 
                "harga_target": harga, 
                "nominal_terkumpul": dana, 
                "deadline": str(tgl)
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Berhasil Disimpan!")
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
        st.caption(f"Tercapai: {persen*100:.1f}% | Sisa: Rp {max(target - terkumpul, 0):,.0f}")
        st.divider()
else:
    st.info("Belum ada data. Silakan isi di menu samping.")

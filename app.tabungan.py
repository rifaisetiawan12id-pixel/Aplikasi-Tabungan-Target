import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Tabungan UTS", layout="centered")
st.title("💰 Tabungan Target - Cloud")

# URL Spreadsheet kamu
URL_SHEET = "https://docs.google.com/spreadsheets/d/1AiKDFHzCU9VnKwZnoaF-0cnUCBOuyYpOAc-C4vOfw2I/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        return conn.read(spreadsheet=URL_SHEET)
    except:
        return pd.DataFrame(columns=["nama_barang", "harga_target", "nominal_terkumpul", "deadline"])

df = load_data()

with st.sidebar:
    st.header("Input Target")
    with st.form("add_form"):
        nama = st.text_input("Nama Barang")
        harga = st.number_input("Harga Target", min_value=0)
        dana = st.number_input("Terkumpul", min_value=0)
        tgl = st.date_input("Deadline")
        submit = st.form_submit_button("Simpan ke Cloud")
        if submit and nama:
            new_row = pd.DataFrame([{"nama_barang": nama, "harga_target": harga, "nominal_terkumpul": dana, "deadline": str(tgl)}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("Tersimpan!")
            st.rerun()

st.subheader("Daftar Progres")
if not df.empty:
    for index, row in df.iterrows():
        target = float(row["harga_target"])
        terkumpul = float(row["nominal_terkumpul"])
        persen = (terkumpul / target) if target > 0 else 0
        st.write(f"**{row['nama_barang']}**")
        st.progress(min(persen, 1.0))
        st.caption(f"{persen*100:.1f}% | Sisa: Rp {max(target - terkumpul, 0):,.0f}")
        st.divider()

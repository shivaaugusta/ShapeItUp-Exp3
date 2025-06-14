# --- Streamlit App: Eksperimen 3 (Preferensi Visual Shapes) ---
import streamlit as st
import random
import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Inisialisasi Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["google_sheets"], scopes=scope)
client = gspread.authorize(creds)

# --- Akses worksheet Eksperimen_3 ---
try:
    spreadsheet = client.open_by_key("1aZ0LjvdZs1WHGphqb_nYrvPma8xEG9mxfM-O1_fsi3g")
    worksheet = spreadsheet.worksheet("Eksperimen_3")
except Exception as e:
    st.error(f"Gagal membuka spreadsheet: {e}")
    st.stop()

# --- Konfigurasi ---
st.set_page_config(page_title="Eksperimen 3 - Preferensi Visual", layout="centered")
st.title("🎨 Eksperimen 3: Pilih Shape yang Paling Kamu Sukai")

st.write("""
Lihat 6 bentuk shape di bawah ini. Urutkan berdasarkan preferensimu dari **paling disukai** (1) hingga **paling tidak disukai** (6).
""")

# --- Load 6 acak shape dari folder ---
all_shapes = os.listdir("shapes")
if "selected_shapes" not in st.session_state:
    st.session_state.selected_shapes = random.sample(all_shapes, 6)

selected_shapes = st.session_state.selected_shapes

shape_labels = [shape.replace(".png", "").replace("-", " ").title() for shape in selected_shapes]

# --- Tampilkan bentuk dan input ranking ---
st.subheader("🔢 Urutkan Preferensimu")
user_rankings = {}

cols = st.columns(3)
for i, shape in enumerate(selected_shapes):
    with cols[i % 3]:
        st.image(f"shapes/{shape}", width=100)
        user_rankings[shape] = st.selectbox(f"Peringkat untuk {shape_labels[i]}", list(range(1, 7)), key=shape)

# --- Validasi dan Simpan ---
if st.button("📩 Submit Preferensi"):
    if len(set(user_rankings.values())) != 6:
        st.error("Pastikan setiap shape memiliki peringkat unik dari 1 hingga 6!")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ordered_shapes = sorted(user_rankings.items(), key=lambda x: x[1])
        row = [timestamp] + [s for s, _ in ordered_shapes]

        try:
            worksheet.append_row(row)
            st.success("✅ Preferensi kamu berhasil dikirim. Terima kasih!")
            del st.session_state.selected_shapes
        except Exception as e:
            st.error(f"❌ Gagal menyimpan ke Google Sheets: {e}")

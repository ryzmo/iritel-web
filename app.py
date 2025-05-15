import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import os

st.set_page_config(page_title="Dashboard Interaksi Rak", layout="wide")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("interaksi_log.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['durasi_detik'] = df['durasi_detik'].astype(float)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["timestamp", "rak", "durasi_detik"])

df = load_data()

# Header
st.markdown("""
    <h1 style='text-align: center;'>Dashboard Interaksi Pelanggan di Rak Minimarket</h1>
    <p style='text-align: center; color: gray;'>Data real-time dari sistem deteksi kamera</p>
    <hr>
""", unsafe_allow_html=True)

# Statistik Umum
st.subheader("📈 Statistik Umum")
col1, col2 = st.columns(2)
with col1:
    st.metric("🧍 Jumlah Interaksi", len(df))
with col2:
    rata2 = f"{df['durasi_detik'].mean():.2f}" if not df.empty else "-"
    st.metric("⏱️ Rata-rata Durasi (detik)", rata2)

st.markdown("---")

# Insight dari AI
st.subheader("🤖 Insight dari Gemini AI")
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "AIzaSyCsaRx6DBvrFQfFC80rnkmv9dwZporDbbY")

if st.button("🔍 Analisis Otomatis oleh Gemini AI"):
    if df.empty:
        st.warning("Data masih kosong.")
    else:
        data_str = df.tail(10).to_csv(index=False)
        prompt = f"Berdasarkan data interaksi pelanggan di rak berikut:\n\n{data_str}\n\nBerikan ringkasan insight, pola perilaku, dan saran display produk."

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.success("📌 Insight dari Gemini:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Gagal mengambil insight dari Gemini: {e}")

st.markdown("---")

# Visualisasi Data
st.subheader("🗂️ Visualisasi Interaksi")

if not df.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📦 Jumlah Interaksi per Rak")
        count_by_rak = df['rak'].value_counts()
        st.bar_chart(count_by_rak)

    with col2:
        st.markdown("### ⏳ Rata-rata Durasi per Rak (detik)")
        mean_by_rak = df.groupby('rak')['durasi_detik'].mean()
        st.bar_chart(mean_by_rak)
else:
    st.info("Belum ada data interaksi untuk divisualisasikan.")

st.markdown("---")

# Data Lengkap
st.subheader("📋 Data Interaksi Lengkap")
st.dataframe(df.sort_values(by="timestamp", ascending=False), use_container_width=True)

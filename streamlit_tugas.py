import streamlit as st
import pandas as pd

# ======================
# TITLE
# ======================
st.title("🍪 Dashboard Penjualan Toko Kue")

# ======================
# HEADER
# ======================
st.header("Ringkasan Penjualan")

st.write(
    """
    Dashboard ini digunakan untuk memantau data penjualan kue kering selama satu bulan.
    Informasi yang ditampilkan meliputi jenis kue, jumlah terjual, harga, serta total 
    pendapatan. 
    """
)

# ======================
# SUBHEADER
# ======================
st.subheader("Data Penjualan Kue")

# ======================
# DATAFRAME
# ======================
data = {
    "Nama Kue": [
        "Nastar", "Kastengel", "Putri Salju",
        "Chocolate Cookies", "Cheese Cookies", "Palm Cheese Cookies"
    ],
    "Jumlah Terjual (pack)": [120, 95, 80, 150, 110, 130],
    "Harga per pack (Rp)": [70000, 60000, 50000, 45000, 45000, 50000]
}

df = pd.DataFrame(data)
df["Total Pendapatan (Rp)"] = df["Jumlah Terjual (pack)"] * df["Harga per pack (Rp)"]

st.dataframe(df)

# ======================
# TEXT PENJELASAN
# ======================
st.write(
    """
    Tabel di atas menunjukkan data penjualan berbagai jenis kue kering dalam satu bulan. Kolom 
    total pendapatan dihitung dari hasil perkalian jumlah terjual dengan harga per pack.
    """
)

# ======================
# CODE (POTONGAN KODE)
# ======================
st.subheader("Perhitungan Pendapatan")

st.code(
    """
df["Total Pendapatan (Rp)"] = (
    df["Jumlah Terjual (pack)"] * df["Harga per pack (Rp)"]
)
    """,
    language="python"
)

# ======================
# CHART
# ======================
st.subheader("Visualisasi Total Pendapatan per Jenis Kue")

st.bar_chart(
    df.set_index("Nama Kue")["Total Pendapatan (Rp)"]
)

# ======================
# CAPTION
# ======================
st.caption(
    "Grafik menunjukkan perbandingan total pendapatan dari masing-masing jenis kue."
)

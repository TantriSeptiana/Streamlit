import streamlit as st
import pandas as pd

# TITLE
st.title("🍪 Dashboard Penjualan Toko Kue")

# RINGKASAN PENJUALAN
st.header("Ringkasan Penjualan")

st.text(
    """
    Dashboard ini digunakan untuk memantau data penjualan kue kering selama satu bulan.
    Informasi yang ditampilkan meliputi jenis kue, jumlah terjual, harga, serta total 
    pendapatan. 
    """
)

# DATAFRAME
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

# FILTER
st.sidebar.header("Filter Data")

selected_kue = st.sidebar.multiselect(
    "Pilih Jenis Kue:",
    options=df["Nama Kue"].unique(),
    default=df["Nama Kue"].unique()
)

filtered_df = df[df["Nama Kue"].isin(selected_kue)]

# METRIC
total_terjual = filtered_df["Jumlah Terjual (pack)"].sum()
total_pendapatan = filtered_df["Total Pendapatan (Rp)"].sum()
rata_harga = filtered_df["Harga per pack (Rp)"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Terjual (pack)", total_terjual)
col2.metric("Total Pendapatan (Rp)", f"{total_pendapatan:,.0f}")
col3.metric("Rata-rata Harga (Rp)", f"{rata_harga:,.0f}")

# TABEL PENJUALAN
st.subheader("Data Penjualan Kue")
st.dataframe(df)

# TEXT PENJELASAN
st.text(
    """
    Tabel di atas menunjukkan data penjualan berbagai jenis kue kering dalam satu bulan. Kolom 
    total pendapatan dihitung dari hasil perkalian jumlah terjual dengan harga per pack.
    """
)

# CODE (POTONGAN KODE)
st.subheader("Perhitungan Pendapatan")

st.code(
    """
df["Total Pendapatan (Rp)"] = (
    df["Jumlah Terjual (pack)"] * df["Harga per pack (Rp)"]
)
    """,
    language="python"
)

# CHART
st.subheader("Visualisasi Data Penjualan")

col4, col5 = st.columns(2)

with col4:
    st.text("Jumlah Terjual per Jenis Kue")
    st.bar_chart(
        filtered_df.set_index("Nama Kue")["Jumlah Terjual (pack)"]
    )

with col5:
    st.text("Total Pendapatan per Jenis Kue")
    st.bar_chart(
        filtered_df.set_index("Nama Kue")["Total Pendapatan (Rp)"]
    )

# CAPTION
st.caption(
    "Grafik menunjukkan perbandingan jumlah penjualan kue dan total pendapatan dari masing-masing jenis kue."
)

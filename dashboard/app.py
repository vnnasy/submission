import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components
import pandas as pd
import pad as pad  # Mengimpor file pad.py

# Markdown pengantar dashboard
st.markdown("""
    # Proyek Analisis Data: E-Commerce Public Dataset

    - *Nama:* Vina Nasyi Atul Lailiyah  
    - *Email:* m327b4kx4420@bangkit.academy  
    - *ID Dicoding:* vinanasyi  

    **Dashboard ini menyajikan hasil analisis mengenai pola pengeluaran pelanggan berdasarkan metode pembayaran, 
    penjualan produk per kategori, dan visualisasi geospasial untuk distribusi pelanggan di berbagai wilayah.**

    ### Catatan Penting:
    Mengingat ukuran data yang besar dan limitasi memori dari Streamlit, maka saya memutuskan untuk mengurangi jumlah baris data yang diolah pada Streamlit
    yang nantinya akan divisualisasikan di sini. Untuk hasil lengkapnya ada di file ekstensi .ipynb di dalam folder project.
""")

# Membuat selectbox untuk memilih visualisasi
option = st.selectbox(
    "Pilih Visualisasi",
    ("Distribusi Metode Pembayaran", "Distribusi Total Pembayaran", "Distribusi Kategori Produk", 
     "Heatmap Korelasi", "Pengeluaran Berdasarkan Metode Pembayaran", "Penjualan per Kategori Produk", "Peta Pembayaran")
)
if option == "Distribusi Metode Pembayaran":
    st.write("### Distribusi Metode Pembayaran")
    pad.plot_payment_distribution(pad.merged_data)
    fig = plt.gcf()
    st.pyplot(fig)

elif option == "Distribusi Total Pembayaran":
    st.write("### Distribusi Total Pembayaran")
    pad.plot_payment_value_distribution(pad.merged_data)
    fig = plt.gcf()
    st.pyplot(fig)

elif option == "Distribusi Kategori Produk":
    st.write("### Distribusi Kategori Produk")
    pad.plot_product_category_distribution(pad.merged_data)
    fig = plt.gcf()
    st.pyplot(fig)

elif option == "Heatmap Korelasi":
    columns = st.multiselect("Pilih Kolom untuk Korelasi", pad.merged_data.select_dtypes(include=['float64', 'int64']).columns)
    if columns:
        pad.plot_correlation_heatmap(pad.merged_data, columns, "Heatmap Korelasi")
        fig = plt.gcf()
        st.pyplot(fig)

elif option == "Pengeluaran Berdasarkan Metode Pembayaran":
    st.write("### Total Pengeluaran Berdasarkan Metode Pembayaran dan Wilayah")
    pad.plot_expenditure_by_payment_method_and_region(pad.payment_analysis)
    fig = plt.gcf()
    st.pyplot(fig)

elif option == "Penjualan per Kategori Produk":
    st.write("### Total Penjualan per Kategori Produk dan Metode Pembayaran")
    pad.plot_sales_by_product_category(pad.product_analysis)
    fig = plt.gcf()
    st.pyplot(fig)

elif option == "Peta Pembayaran":
    st.write("### Peta Transaksi Berdasarkan Pembayaran")
    if not pad.merged_data.empty:  # Validasi jika data tidak kosong
        map_object = pad.create_folium_map(pad.merged_data)
        components.html(map_object._repr_html_(), height=600)
    else:
        st.error("Data tidak tersedia untuk peta visualisasi.")

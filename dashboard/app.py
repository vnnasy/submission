import os
import sys
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components
import pandas as pd

# Mengimpor pad.py secara langsung
import pad as pad


# Markdown awal untuk pengantar dashboard
st.markdown("""
    # Proyek Analisis Data: E-Commerce Public Dataset

    - *Nama:* Vina Nasyi Atul Lailiyah  
    - *Email:* m327b4kx4420@bangkit.academy  
    - *ID Dicoding:* vinanasyi  

    **Dashboard ini menyajikan hasil analisis mengenai pola pengeluaran pelanggan berdasarkan metode pembayaran, 
    penjualan produk per kategori, dan visualisasi geospasial untuk distribusi pelanggan di berbagai wilayah.**

    ### Catatan Penting:
    Mengingat ukuran dataset yang sangat besar, saya tidak dapat memuat dataset secara langsung. Oleh karena itu, 
    dashboard ini hanya menampilkan hasil analisis dalam bentuk gambar statis yang telah dihasilkan sebelumnya 
    dari analisis data.
""")

# Membuat selectbox untuk memilih visualisasi
option = st.selectbox(
    "Pilih Visualisasi",
    ("Pengeluaran Berdasarkan Metode Pembayaran", "Penjualan per Kategori Produk", "Peta Pembayaran")
)

# Menampilkan grafik sesuai pilihan pengguna
if option == "Pengeluaran Berdasarkan Metode Pembayaran":
    st.write("### Total Pengeluaran Berdasarkan Metode Pembayaran dan Wilayah")
    
    # Memanggil fungsi visualisasi dari pad.py
    if not pad.payment_analysis.empty:  # Validasi jika data tidak kosong
        pad.plot_expenditure_by_payment_method_and_region(pad.payment_analysis)
        fig = plt.gcf()  # Mengambil figure yang sedang aktif
        st.pyplot(fig)
    else:
        st.error("Data tidak tersedia untuk visualisasi.")

    st.markdown("""
    - Grafik ini memvisualisasikan total pengeluaran berdasarkan metode pembayaran (kartu kredit, kartu debit, boleto, dll.) di berbagai wilayah di Brasil.
    - Penggunaan kartu kredit mendominasi di semua wilayah, terutama di São Paulo (SP), yang memiliki pengeluaran tertinggi.
    """)

elif option == "Penjualan per Kategori Produk":
    st.write("### Total Penjualan per Kategori Produk dan Metode Pembayaran")
    
    # Memanggil fungsi visualisasi dari pad.py
    if not pad.product_analysis.empty:  # Validasi jika data tidak kosong
        pad.plot_sales_per_category(pad.product_analysis)
        fig = plt.gcf()
        st.pyplot(fig)
    else:
        st.error("Data tidak tersedia untuk visualisasi.")

    st.markdown("""
    - Grafik ini menunjukkan total penjualan berdasarkan kategori produk (misalnya, cama_mesa_banho, esporte_lazer) dan metode pembayaran.
    - Kategori produk seperti "cama_mesa_banho" dan "esporte_lazer" menunjukkan volume penjualan yang tinggi. Kartu kredit adalah metode pembayaran yang paling sering digunakan di sebagian besar kategori produk, sedangkan penggunaan voucher dan kartu debit relatif lebih rendah.
    """)

elif option == "Peta Pembayaran":
    st.write("### Peta Transaksi Berdasarkan Pembayaran")
    
    # Memanggil fungsi create_payment_map dari pad.py
    if not pad.merged_data.empty:  # Validasi jika data tidak kosong
        map_object = pad.create_payment_map(pad.merged_data)
        components.html(map_object._repr_html_(), height=600)
    else:
        st.error("Data tidak tersedia untuk peta visualisasi.")

    st.header("Kesimpulan")
    st.markdown("""
    ### 1. Pola Pengeluaran Pelanggan Berdasarkan Metode Pembayaran dan Wilayah:
    - São Paulo (SP) memiliki total pengeluaran tertinggi, terutama melalui kartu kredit.
    - Wilayah lain juga menunjukkan preferensi penggunaan kartu kredit, tetapi ada penggunaan boleto dan voucher yang signifikan di beberapa daerah.

    ### 2. Penjualan Kategori Produk dan Preferensi Pembayaran:
    - Kategori produk yang memiliki permintaan tinggi (misalnya, dekorasi rumah, elektronik, dan kecantikan) sebagian besar melibatkan pembayaran dengan kartu kredit.
    - Kategori seperti olahraga dan fashion juga menunjukkan penjualan signifikan dengan sedikit ketergantungan pada metode pembayaran alternatif seperti boleto dan voucher.
    """)

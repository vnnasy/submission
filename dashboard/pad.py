# %% [markdown]
# # Proyek Analisis Data : E-Commerce Public Dataset
# 
# - **Nama:** Vina Nasyi Atul Lailiyah
# - **Email:** m327b4kx4420@bangkit.academy
# - **ID Dicoding:** vinanasyi

# %% [markdown]
# ## Menentukan Pertanyaan Bisnis

# %% [markdown]
# - Bagaimana pola pengeluaran pelanggan berdasarkan metode pembayaran yang digunakan, dan bagaimana distribusi ini berubah menurut wilayah?
# - Kategori produk mana yang memiliki penjualan terbanyak, bagaimana keterkaitannya dengan metode pembayaran, dan bagaimana distribusinya di berbagai wilayah?

# %% [markdown]
# ## Import Semua Packages/Library yang Digunakan

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd
import folium
from datetime import datetime
import streamlit as st
from scipy import stats

# %% [markdown]
# ## Data Wrangling

# %% [markdown]
# ### Gathering Data

# %%
orders = pd.read_csv('dataset/orders_dataset.csv', nrows=50000)
order_items = pd.read_csv('dataset/order_items_dataset.csv', nrows=50000)
order_payments = pd.read_csv('dataset/order_payments_dataset.csv', nrows=50000)
geolocation = pd.read_csv('dataset/geolocation_dataset.csv', nrows=50000)
products = pd.read_csv('dataset/products_dataset.csv', nrows=50000)
customers = pd.read_csv('dataset/customers_dataset.csv', nrows=50000)


# %% [markdown]
# **Insight:**
# - Memuat hanya dataset yang relevan untuk analisis sehingga fokus pada informasi yang akan membantu menjawab pertanyaan bisnis.
# - Penggabungan beberapa dataset ini penting untuk memahami berbagai aspek bisnis, seperti pesanan, pembayaran, pelanggan, produk, dan wilayah.

# %% [markdown]
# ### Assessing Data
# %%
orders.head()

# %%
order_items.head()

# %%
order_payments.head()

# %%
geolocation.head()

# %%
products.head()

# %%
customers.head()

# %%
orders.info()

# %%
order_items.info()

# %%
order_payments.info()

# %%
geolocation.info()

# %%
products.info()

# %%
customers.info()

# %%
orders.describe()

# %%
order_items.describe()

# %%
order_payments.describe()

# %%
geolocation.describe()

# %%
products.describe()

# %%
customers.describe()

# %%
orders.isnull().sum()

# %%
order_items.isnull().sum()

# %%
order_payments.isnull().sum()

# %%
geolocation.isnull().sum()

# %%
products.isnull().sum()

# %%
customers.isnull().sum()

# %%
orders.duplicated().sum()

# %%
order_items.duplicated().sum()

# %%
order_payments.duplicated().sum()

# %%
geolocation.duplicated().sum()

# %%
products.duplicated().sum()

# %%
customers.duplicated().sum()

# %%
invalid_weights = products[products['product_weight_g'] < 0]
print(invalid_weights)

# %% [markdown]
# **Insight:**
# - Data dari setiap dataset ditinjau melalui head, info, dan describe untuk memahami struktur, informasi, dan statistik deskriptif dari setiap dataset. Pengecekan dilakukan terhadap nilai yang hilang, duplikat, dan data yang tidak valid (seperti berat produk negatif).
# - Menilai data membantu mengidentifikasi masalah seperti data yang hilang, duplikasi, atau outlier yang dapat mempengaruhi hasil analisis.

# %% [markdown]
# ### Cleaning Data

# %%
orders['order_approved_at'] = orders['order_approved_at'].fillna(pd.Timestamp(datetime.now()))
orders['order_delivered_carrier_date'] = orders['order_delivered_carrier_date'].fillna(pd.Timestamp(datetime.now()))
orders['order_delivered_customer_date'] = orders['order_delivered_customer_date'].fillna(pd.Timestamp(datetime.now()))

# %%
products['product_category_name'] = products['product_category_name'].fillna(products['product_category_name'].mode()[0])
products['product_name_lenght'] = products['product_name_lenght'].fillna(products['product_name_lenght'].mean())
products['product_description_lenght'] = products['product_description_lenght'].fillna(products['product_description_lenght'].mean())
products['product_photos_qty'] = products['product_photos_qty'].fillna(products['product_photos_qty'].mean())
products['product_weight_g'] = products['product_weight_g'].fillna(products['product_weight_g'].mean())
products['product_length_cm'] = products['product_length_cm'].fillna(products['product_length_cm'].mean())
products['product_height_cm'] = products['product_height_cm'].fillna(products['product_height_cm'].mean())
products['product_width_cm'] = products['product_width_cm'].fillna(products['product_width_cm'].mean())

# %%
orders.isnull().sum()

# %%
products.isnull().sum()

# %%
geolocation.drop_duplicates(inplace=True)

# %%
geolocation.duplicated().sum()

# %%
plt.figure(figsize=(10, 6))
sns.boxplot(x=order_payments['payment_value'])
plt.show()

# %%
plt.figure(figsize=(10, 6))
sns.boxplot(x=order_items['freight_value'])
plt.show()

# %%
plt.figure(figsize=(10, 6))
sns.boxplot(x=order_items['price'])
plt.show()

# %%
Q1 = order_items['price'].quantile(0.25)
Q3 = order_items['price'].quantile(0.75)
IQR = Q3 - Q1
order_items = order_items[~((order_items['price'] < (Q1 - 1.5 * IQR)) | (order_items['price'] > (Q3 + 1.5 * IQR)))]

# %%
Q1 = order_items['freight_value'].quantile(0.25)
Q3 = order_items['freight_value'].quantile(0.75)
IQR = Q3 - Q1
order_items = order_items[~((order_items['freight_value'] < (Q1 - 1.5 * IQR)) | (order_items['freight_value'] > (Q3 + 1.5 * IQR)))]

# %%
Q1 = order_payments['payment_value'].quantile(0.25)
Q3 = order_payments['payment_value'].quantile(0.75)
IQR = Q3 - Q1
order_payments = order_payments[~((order_payments['payment_value'] < (Q1 - 1.5 * IQR)) | (order_payments['payment_value'] > (Q3 + 1.5 * IQR)))]

# %% [markdown]
# **Insight:**
# - Nilai yang hilang diisi dengan pengganti yang sesuai (misalnya mode, rata-rata, atau timestamp saat ini untuk data waktu).
# - Data duplikat dihapus dari data geolocation.
# - Outlier di beberapa metrik penting, seperti nilai pembayaran, nilai pengiriman, dan harga barang, dihilangkan menggunakan metode IQR (Interquartile Range).
# - Pembersihan data memastikan bahwa analisis dilakukan berdasarkan data yang akurat dan dapat dipercaya. Menghapus outliers penting untuk mencegah distorsi hasil.

# %% [markdown]
# ## Exploratory Data Analysis (EDA)

# %%
merged_data = orders.merge(order_items, on='order_id', how='inner')

# %%
merged_data = merged_data.merge(order_payments, on='order_id', how='inner')

# %%
merged_data = merged_data.merge(products, on='product_id', how='inner')

# %%
merged_data = merged_data.merge(customers, on='customer_id', how='inner')

# %%
merged_data = merged_data.merge(geolocation, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='inner')

# %%
payment_analysis = merged_data.groupby(['geolocation_state', 'payment_type'])['payment_value'].sum().reset_index()

# %%
payment_analysis = payment_analysis.sort_values(by='payment_value', ascending=False)

# %%
product_analysis = merged_data.groupby(['product_category_name', 'payment_type'])['price'].sum().reset_index()

# %%
product_analysis = product_analysis.sort_values(by='price', ascending=False)

# %% [markdown]
# **Insight:**
# - Dataset Gabungan: Semua dataset digabungkan ke dalam satu dataset menggunakan key yang relevan seperti order_id, product_id, customer_id, dan kode pos di geolocation.
# - Dataset gabungan ini memberikan pengetahuan yang memungkinkan analisis mendalam antara berbagai variabel seperti metode pembayaran, kategori produk, informasi geografis, dan lainnya.
# - Analisis pembayaran dan produk dilakukan untuk memahami perilaku dan preferensi pelanggan.

# %% [markdown]
# ## Visualization & Explanatory Analysis

# %% [markdown]
# ### Bagaimana pola pengeluaran pelanggan berdasarkan metode pembayaran yang digunakan, dan bagaimana distribusi ini berubah menurut wilayah?

# %%
def plot_expenditure_by_payment_method_and_region(payment_analysis):
    """Create a bar plot of total expenditure based on payment method and region."""
    plt.figure(figsize=(14, 14))
    
    sns.barplot(data=payment_analysis, x='payment_value', y='payment_type', hue='geolocation_state')
    
    plt.title('Total Pengeluaran Berdasarkan Metode Pembayaran dan Wilayah')
    plt.xlabel('Total Pengeluaran')
    plt.ylabel('Metode Pembayaran')
    plt.legend(title='Wilayah')

# %% [markdown]
# ### Kategori produk mana yang memiliki penjualan terbanyak, bagaimana keterkaitannya dengan metode pembayaran, dan bagaimana distribusinya di berbagai wilayah?

# %%
def plot_sales_per_category(product_analysis):
    """Create a bar plot of total sales per product category and payment type."""
    plt.figure(figsize=(14, 14))
    
    sns.barplot(data=product_analysis, x='price', y='product_category_name', hue='payment_type')
    
    plt.title('Total Penjualan per Kategori Produk dan Metode Pembayaran')
    plt.xlabel('Total Penjualan')
    plt.ylabel('Kategori Produk')
    plt.legend(title='Metode Pembayaran')
    


# %% [markdown]
# **Insight:**
# 
# Metode Pembayaran Berdasarkan Wilayah:
# - Grafik pertama memvisualisasikan total pengeluaran berdasarkan metode pembayaran (kartu kredit, kartu debit, boleto, dll.) di berbagai wilayah di Brasil.
# - Penggunaan kartu kredit mendominasi di semua wilayah, terutama di São Paulo (SP), yang memiliki pengeluaran tertinggi.
# 
# Penjualan Kategori Produk:
# - Grafik kedua menunjukkan total penjualan berdasarkan kategori produk (misalnya cama_mesa_banho, esporte_lazer) dan metode pembayaran.
# - Kategori produk seperti "cama_mesa_banho" dan "esporte_lazer" menunjukkan volume penjualan yang tinggi. Kartu kredit adalah metode pembayaran yang paling sering digunakan di sebagian besar kategori produk, sedangkan penggunaan voucher dan kartu debit relatif lebih rendah.

# %% [markdown]
# ## Geospatial Analysis

# %% [markdown]
# - Karena keterbatasan device, saya hanya mampu menampilkan dalam data sampel sebanyak 70.000 untuk memetakan aktivitas pembayaran di berbagai lokasi geografis.
# - Langkah ini menambahkan dimensi spasial pada analisis, membantu memvisualisasikan distribusi pelanggan dan jenis pembayaran yang digunakan di berbagai wilayah.

# %%


def create_payment_map(merged_data, sample_size=7000, map_file='map.html'):
    sample_data = merged_data.sample(n=sample_size, random_state=42)

    map_center = [sample_data['geolocation_lat'].mean(), sample_data['geolocation_lng'].mean()]
    m = folium.Map(location=map_center, zoom_start=6)

    def get_color(payment_type):
        """Assign a color based on the payment type."""
        if payment_type == 'credit_card':
            return 'blue'
        elif payment_type == 'boleto':
            return 'green'
        elif payment_type == 'voucher':
            return 'purple'
        elif payment_type == 'debit_card':
            return 'orange'
        else:
            return 'red'

    def add_circle_marker(row):
        """Add a circle marker to the map based on payment data."""
        color = get_color(row['payment_type'])
        radius = max(min(row['payment_value'] / 1000, 10), 1)
        
        folium.CircleMarker(
            location=(row['geolocation_lat'], row['geolocation_lng']),
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=f"Payment Type: {row['payment_type']}, Value: {row['payment_value']:.2f}"
        ).add_to(m)

    sample_data.apply(add_circle_marker, axis=1)

    m.save(map_file)
    return m  



# %% [markdown]
# ## Conclusion

# %% [markdown]
# Pola Pengeluaran Pelanggan Berdasarkan Metode Pembayaran dan Wilayah:
# - São Paulo (SP) memiliki total pengeluaran tertinggi, terutama melalui kartu kredit.
# - Wilayah lain juga menunjukkan preferensi penggunaan kartu kredit, tetapi ada penggunaan boleto dan voucher yang signifikan di beberapa daerah.
# 
# Penjualan Kategori Produk dan Preferensi Pembayaran:
# - Kategori produk yang memiliki permintaan tinggi (misalnya, dekorasi rumah, elektronik, dan kecantikan) sebagian besar melibatkan pembayaran dengan kartu kredit.
# - Kategori seperti olahraga dan fashion juga menunjukkan penjualan signifikan dengan sedikit ketergantungan pada metode pembayaran alternatif seperti boleto dan voucher.



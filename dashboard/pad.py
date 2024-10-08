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

orders = pd.read_csv('dataset/orders_dataset.csv', nrows=50000)
order_items = pd.read_csv('dataset/order_items_dataset.csv', nrows=50000)
order_payments = pd.read_csv('dataset/order_payments_dataset.csv', nrows=50000)
geolocation = pd.read_csv('dataset/geolocation_dataset.csv', nrows=50000)
products = pd.read_csv('dataset/products_dataset.csv', nrows=50000)
customers = pd.read_csv('dataset/customers_dataset.csv', nrows=50000)

orders.head()

order_items.head()

order_payments.head()

geolocation.head()

products.head()

customers.head()

orders.info()

order_items.info()

order_payments.info()

geolocation.info()

products.info()

customers.info()

orders.describe()

order_items.describe()

order_payments.describe()

geolocation.describe()

products.describe()

customers.describe()

orders.isnull().sum()

order_items.isnull().sum()

order_payments.isnull().sum()

geolocation.isnull().sum()

products.isnull().sum()

customers.isnull().sum()

orders.duplicated().sum()

order_items.duplicated().sum()

order_payments.duplicated().sum()

geolocation.duplicated().sum()

products.duplicated().sum()

customers.duplicated().sum()

invalid_weights = products[products['product_weight_g'] < 0]
print(invalid_weights)

orders['order_approved_at'] = orders['order_approved_at'].fillna(pd.Timestamp(datetime.now()))
orders['order_delivered_carrier_date'] = orders['order_delivered_carrier_date'].fillna(pd.Timestamp(datetime.now()))
orders['order_delivered_customer_date'] = orders['order_delivered_customer_date'].fillna(pd.Timestamp(datetime.now()))

products['product_category_name'] = products['product_category_name'].fillna(products['product_category_name'].mode()[0])
products['product_name_lenght'] = products['product_name_lenght'].fillna(products['product_name_lenght'].mean())
products['product_description_lenght'] = products['product_description_lenght'].fillna(products['product_description_lenght'].mean())
products['product_photos_qty'] = products['product_photos_qty'].fillna(products['product_photos_qty'].mean())
products['product_weight_g'] = products['product_weight_g'].fillna(products['product_weight_g'].mean())
products['product_length_cm'] = products['product_length_cm'].fillna(products['product_length_cm'].mean())
products['product_height_cm'] = products['product_height_cm'].fillna(products['product_height_cm'].mean())
products['product_width_cm'] = products['product_width_cm'].fillna(products['product_width_cm'].mean())

orders.isnull().sum()

products.isnull().sum()

geolocation.drop_duplicates(inplace=True)

geolocation.duplicated().sum()

plt.figure(figsize=(10, 6))
sns.boxplot(x=order_payments['payment_value'])
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x=order_items['freight_value'])
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x=order_items['price'])
plt.show()

Q1 = order_items['price'].quantile(0.25)
Q3 = order_items['price'].quantile(0.75)
IQR = Q3 - Q1
order_items = order_items[~((order_items['price'] < (Q1 - 1.5 * IQR)) | (order_items['price'] > (Q3 + 1.5 * IQR)))]

Q1 = order_items['freight_value'].quantile(0.25)
Q3 = order_items['freight_value'].quantile(0.75)
IQR = Q3 - Q1
order_items = order_items[~((order_items['freight_value'] < (Q1 - 1.5 * IQR)) | (order_items['freight_value'] > (Q3 + 1.5 * IQR)))]

Q1 = order_payments['payment_value'].quantile(0.25)
Q3 = order_payments['payment_value'].quantile(0.75)
IQR = Q3 - Q1
order_payments = order_payments[~((order_payments['payment_value'] < (Q1 - 1.5 * IQR)) | (order_payments['payment_value'] > (Q3 + 1.5 * IQR)))]

merged_data = orders.merge(order_items, on='order_id', how='inner')

merged_data = merged_data.merge(order_payments, on='order_id', how='inner')

merged_data = merged_data.merge(products, on='product_id', how='inner')

merged_data = merged_data.merge(customers, on='customer_id', how='inner')

merged_data = merged_data.merge(geolocation, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='inner')

payment_analysis = merged_data.groupby(['geolocation_state', 'payment_type'])['payment_value'].sum().reset_index()

payment_analysis = payment_analysis.sort_values(by='payment_value', ascending=False)

product_analysis = merged_data.groupby(['product_category_name', 'payment_type'])['price'].sum().reset_index()

product_analysis = product_analysis.sort_values(by='price', ascending=False)

merged_data.isnull().sum()

# Visualisasi distribusi metode pembayaran
def plot_payment_distribution(data):
    """Membuat visualisasi distribusi metode pembayaran"""
    plt.figure(figsize=(10, 6))
    sns.countplot(data=data, x='payment_type', order=data['payment_type'].value_counts().index)
    plt.title('Distribusi Metode Pembayaran')
    plt.show()

# Menggunakan fungsi distribusi metode pembayaran
plot_payment_distribution(merged_data)

# Visualisasi distribusi total pembayaran
def plot_payment_value_distribution(data):
    """Membuat visualisasi distribusi total pembayaran"""
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='payment_value', bins=50, kde=True)
    plt.title('Distribusi Total Pembayaran')
    plt.show()

# Menggunakan fungsi distribusi total pembayaran
plot_payment_value_distribution(merged_data)

# Visualisasi distribusi kategori produk
def plot_product_category_distribution(data):
    """Membuat visualisasi distribusi kategori produk"""
    plt.figure(figsize=(10, 14))
    sns.countplot(data=data, y='product_category_name', order=data['product_category_name'].value_counts().index)
    plt.title('Distribusi Kategori Produk')
    plt.show()

# Menggunakan fungsi distribusi kategori produk
plot_product_category_distribution(merged_data)

# Visualisasi heatmap korelasi
def plot_correlation_heatmap(data, columns, title):
    """Membuat heatmap korelasi antar variabel numerik"""
    plt.figure(figsize=(10, 6))
    sns.heatmap(data[columns].corr(), annot=True, cmap='coolwarm')
    plt.title(title)
    plt.show()


# Fungsi untuk memvisualisasikan total pengeluaran berdasarkan metode pembayaran dan wilayah
def plot_expenditure_by_payment_method_and_region(payment_analysis):
    """Membuat visualisasi total pengeluaran berdasarkan metode pembayaran dan wilayah"""
    plt.figure(figsize=(12, 12))
    color_palette = sns.color_palette("Blues", n_colors=4)
    sns.barplot(data=payment_analysis, x='payment_value', y='payment_type', hue='geolocation_state', palette=color_palette)
    plt.title('Total Pengeluaran Berdasarkan Metode Pembayaran dan Wilayah', fontsize=16)
    plt.xlabel('Total Pengeluaran (dalam unit)', fontsize=14)
    plt.ylabel('Metode Pembayaran', fontsize=14)
    plt.legend(title='Wilayah', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Visualisasi total penjualan per kategori produk
def plot_sales_by_product_category(product_analysis):
    """Membuat visualisasi total penjualan per kategori produk"""
    plt.figure(figsize=(12, 10))
    color_palette = sns.color_palette("Blues", n_colors=4)
    sns.barplot(data=product_analysis, x='price', y='product_category_name', hue='payment_type', palette=color_palette)
    plt.title('Total Penjualan per Kategori Produk dan Metode Pembayaran', fontsize=16)
    plt.xlabel('Total Penjualan (dalam unit)', fontsize=14)
    plt.ylabel('Kategori Produk', fontsize=14)
    plt.legend(title='Metode Pembayaran', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Fungsi untuk membuat peta dengan folium
def create_folium_map(sample_data):
    """Membuat peta berdasarkan geolokasi dan tipe pembayaran"""
    map_center = [sample_data['geolocation_lat'].mean(), sample_data['geolocation_lng'].mean()]
    m = folium.Map(location=map_center, zoom_start=6)
    
    def get_color(payment_type):
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
    m.save('map.html')
    return m


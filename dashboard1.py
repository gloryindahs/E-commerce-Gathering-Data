import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

#requirements
matplotlib==3.8.0
numpy==1.25.2
pandas==2.1.4
seaborn==0.13.0
streamlit==1.26.0


# Gathering Data
customers_df = pd.read_csv("https://raw.githubusercontent.com/gloryindahs/E-commerce-Gathering-Data/main/customers_dataset.csv")
orders_df = pd.read_csv("https://raw.githubusercontent.com/gloryindahs/E-commerce-Gathering-Data/main/orders_dataset.csv")
order_payments_df = pd.read_csv("https://raw.githubusercontent.com/gloryindahs/E-commerce-Gathering-Data/main/order_payments_dataset.csv")
order_items_df = pd.read_csv("https://raw.githubusercontent.com/gloryindahs/E-commerce-Gathering-Data/main/order_items_dataset.csv")

# Title
st.title('E-commerce Data Analysis Dashboard')

# Introduction
st.write("""
This dashboard provides insights into the e-commerce dataset.
""")

# Sidebar
st.sidebar.subheader('Explore Data')

# Show raw data
if st.sidebar.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(customers_df)
    st.write(orders_df)
    st.write(order_payments_df)
    st.write(order_items_df)

# Assessment
st.sidebar.subheader('Assessment')

# Assessing Data
if st.sidebar.checkbox('Assessing Data'):
    st.subheader('Data Assessment')
    st.write("Customers DataFrame Info:")
    st.write(customers_df.info())
    st.write("Number of duplicates in Customers DataFrame:", customers_df.duplicated().sum())
    st.write("Orders DataFrame Info:")
    st.write(orders_df.info())
    st.write("Number of duplicates in Orders DataFrame:", orders_df.duplicated().sum())
    st.write("Order Payments DataFrame Info:")
    st.write(order_payments_df.info())
    st.write("Number of duplicates in Order Payments DataFrame:", order_payments_df.duplicated().sum())

# Visualization & Explanatory Analysis

# Pertanyaan 1:
st.subheader('Number of Customers by State')
bystate_df = customers_df.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
plt.figure(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="customer_count", y="customer_state", data=bystate_df, palette=colors_)
plt.title("Number of Customers by State", loc="center", fontsize=15)
plt.ylabel("State")
plt.xlabel("Number of Customers")
plt.tick_params(axis='y', labelsize=12)
st.pyplot()

# Pertanyaan 2:
st.subheader('Recency, Frequency, and Monetary Analysis')
merged_df = pd.merge(order_items_df, orders_df, on="order_id", how="left")
merged_df = pd.merge(merged_df, order_payments_df, on="order_id", how="left")
rfm_df = merged_df.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max",
    "order_id": "nunique",
    "price": "sum"
})
rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"]).dt.date
recent_date = rfm_df["max_order_timestamp"].max()
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
rfm_df.drop(["max_order_timestamp"], axis=1, inplace=True)
st.subheader('Recency')
st.write(sns.histplot(rfm_df['recency'], bins=20, color='skyblue'))
st.subheader('Frequency')
st.write(sns.histplot(rfm_df['frequency'], bins=20, color='salmon'))
st.subheader('Monetary')
st.write(sns.histplot(rfm_df['monetary'], bins=20, color='green'))

# Pertanyaan 3:
st.subheader('Distribution of Payments by Payment Type')
payment_type_counts = order_payments_df['payment_type'].value_counts()
plt.figure(figsize=(8, 8))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
plt.pie(payment_type_counts, labels=payment_type_counts.index, autopct='%1.1f%%', colors=colors_)
plt.title("Distribution of Payments by Payment Type", fontsize=15)
st.pyplot()

# Save to CSV
if st.sidebar.checkbox('Save to CSV'):
    st.subheader('Save Data to CSV')
    all_df = pd.concat([customers_df, orders_df, order_payments_df], axis=1)
    all_df.to_csv("all_data.csv", index=False)
    st.write('Data saved to all_data.csv')


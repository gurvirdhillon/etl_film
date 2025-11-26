import streamlit as st
import pandas as pd
from pathlib import Path

# 🔹 Dynamically set correct path (no more "../../")
base = Path(__file__).resolve().parents[2] / "data" / "output"

df_customer = pd.read_csv(base / "customer.csv")
df_store = pd.read_csv(base / "store.csv")
df_payment = pd.read_csv(base / "payment.csv")

st.title("Revenue per store brought in")

payments_customer = df_payment.merge(df_customer, on='customer_id', how='left')
full_data = payments_customer.merge(df_store, on='store_id', how='left')

full_data['store_id'] = full_data['store_id'].replace({1: 'Canada', 2: 'Australia'})

revenue_by_store = full_data.groupby('store_id')['amount'].sum().reset_index()
st.bar_chart(revenue_by_store.set_index('store_id'))

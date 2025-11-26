import streamlit as st
import pandas as pd

df_customer = pd.read_csv("../../data/output/customer.csv")
df_store = pd.read_csv("../../data/output/store.csv")
df_payment = pd.read_csv("../../data/output/payment.csv")

st.title("Revenue per store brought in")

payments_customer = df_payment.merge(df_customer, on='customer_id', how='left')
full_data = payments_customer.merge(df_store, on='store_id', how='left')

full_data['store_id'] = full_data['store_id'].replace({1: 'Canada', 2: 'Australia'})

revenue_by_store = full_data.groupby('store_id')['amount'].sum().reset_index()
st.bar_chart(revenue_by_store.set_index('store_id'))


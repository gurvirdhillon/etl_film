import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt

base = Path(__file__).resolve().parents[2] / "data" / "output"

df_payment = pd.read_csv(base / "payment.csv")
df_customer = pd.read_csv(base /"customer.csv")
df_store = pd.read_csv(base / "store.csv")
df_address = pd.read_csv(base / "address.csv")
df_city = pd.read_csv(base / "city.csv")
df_country = pd.read_csv(base / "country.csv")

df = df_payment.merge(df_customer[['customer_id', 'address_id']], on='customer_id', how='left')
df = df.merge(df_address[['address_id', 'city_id']], on='address_id', how='left')
df = df.merge(df_city[['city_id', 'country_id']], on='city_id', how='left')
df = df.merge(df_country[['country_id', 'country']], on='country_id', how='left')

revenue_by_country = (
    df.groupby('country')['amount']
    .sum()
    .reset_index()
    .sort_values(by='amount', ascending=False)
)

print(revenue_by_country)

st.title("Revenue Analysis by Customer Country")

st.write("### Total Revenue by Country")
st.dataframe(revenue_by_country)

chart = alt.Chart(revenue_by_country).mark_bar().encode(
    x=alt.X('country:N', title='Customer Country'),
    y=alt.Y('amount:Q', title='Total Revenue'),
    tooltip=['country', 'amount']
).properties(
    title='Revenue by Customer Country',
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)

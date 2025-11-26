import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

base = Path(__file__).resolve().parents[2] / "data" / "output"

film = pd.read_csv(base / "film.csv")
inventory = pd.read_csv(base / "inventory.csv")
rental = pd.read_csv(base / "rental.csv")
payment = pd.read_csv(base / "payment.csv")

film_inventory = pd.merge(inventory, film, on="film_id", how="left")
film_inventory_rentals = pd.merge(film_inventory, rental, on="inventory_id", how="left")
df = pd.merge(film_inventory_rentals, payment, on="rental_id", how="left")

st.header("Profit per movie rating")

agg_choice = st.radio("Select an aggregation",
                      ["Total profit","Mean profit"]
                      )

if agg_choice == "Total profit":
    profit_per_rating = (df.groupby("rating")["amount"].sum()
                         .reset_index()
                         .sort_values("amount",ascending=False))
    label = "Total Profit"
else:
    profit_per_rating = (df.groupby("rating")["amount"].mean()
                         .reset_index()
                         .sort_values("amount",ascending=False))
    label = "Mean Profit"

fig = px.bar(
    profit_per_rating,
    x="rating",
    y="amount",
    title=f"{agg_choice} per Movie Rating",
    labels={"amount": label},
    color="rating"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Number of movies per rating")

fig2 = px.bar(
    df.groupby("rating")["film_id"].nunique()
    .reset_index(),
    x="rating",
    y="film_id",
    title="Number of movies per rating",
    labels={"film_id":"Number of movies"},
    color="rating",
    category_orders={"rating": ["G", "PG", "PG-13", "R", "NC-17"]}
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

df['rental_date'] = pd.to_datetime(df['rental_date'])
df['return_date'] = pd.to_datetime(df['return_date'])
df['rental_duration_days'] = (df['return_date'] - df['rental_date']).dt.days
avg_duration_per_rating = df.groupby('rating')['rental_duration_days'].mean().reset_index()

st.header("Average Rental Duration per Rating")

fig = px.bar(
    avg_duration_per_rating,
    x='rating',
    y='rental_duration_days',
    title='Average Rental Duration (Days) by Rating',
    color='rating',
    category_orders={"rating": ["G", "PG", "PG-13", "R", "NC-17"]},
    text='rental_duration_days'
)

fig.update_traces(texttemplate='%{text:.2f} days', textposition='outside')
st.plotly_chart(fig)
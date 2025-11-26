import streamlit as st
import pandas as pd
from pathlib import Path

import streamlit as st
import pandas as pd

# BLOCKBUSTER THEME 
st.markdown(
    """
    <style>
        /* White background everywhere */
        .main, body, html {
            background-color: white !important;
        }

        /* Headings = Blockbuster Yellow */
        h1, h2, h3 {
            color: #FFD200 !important;
            font-weight: 700 !important;
        }

        /* Normal text = Blockbuster Blue */
        p, div, span, label, .stMetric, .stText, .stMarkdown {
            color: #0046AD !important;
        }

        /* Sidebar background white */
        section[data-testid="stSidebar"] {
            background-color: white !important;
        }

        /* Sidebar text blue */
        section[data-testid="stSidebar"] * {
            color: #0046AD !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    base = Path(__file__).resolve().parents[2] / "data" / "output"

    film = pd.read_csv(base / "film.csv")
    category = pd.read_csv(base / "category.csv")
    film_cat = pd.read_csv(base / "film_category.csv")
    inventory = pd.read_csv(base / "inventory.csv")
    rental = pd.read_csv(base / "rental.csv")
    payment = pd.read_csv(base / "payment.csv")
    customer = pd.read_csv(base / "customer.csv")
    store = pd.read_csv(base / "store.csv")
    address = pd.read_csv(base / "address.csv")
    city = pd.read_csv(base / "city.csv")
    country = pd.read_csv(base / "country.csv")

    # ---- address + city + country: keep ONLY what we need ----
    addr = (
        address[["address_id", "city_id"]]
        .merge(city[["city_id", "country_id"]], on="city_id", how="left")
        .merge(
            country[["country_id", "country"]], on="country_id", how="left"
        )[
            ["address_id", "country"]
        ]  # only address_id + country
    )

    # store country
    store_geo = (
        store[["store_id", "address_id"]]
        .merge(addr, on="address_id", how="left")
        .rename(columns={"country": "store_country"})
    )

    # customer country
    cust_geo = (
        customer[["customer_id", "address_id"]]
        .merge(addr, on="address_id", how="left")
        .rename(columns={"country": "customer_country"})
    )

    # film + category
    film_full = (
        film[["film_id", "title", "rating"]]
        .merge(film_cat[["film_id", "category_id"]], on="film_id", how="left")
        .merge(category[["category_id", "name"]], on="category_id", how="left")
        .rename(columns={"name": "category_name"})
    )

    #  main fact table
    # IMPORTANT CHANGE: we do NOT bring customer_id from rental,
    # so the customer_id from payment stays as 'customer_id'
    df = (
        payment.merge(
            rental[["rental_id", "inventory_id", "rental_date"]],
            on="rental_id",
            how="left",
        )
        .merge(
            inventory[["inventory_id", "film_id", "store_id"]],
            on="inventory_id",
            how="left",
        )
        .merge(film_full, on="film_id", how="left")
        .merge(cust_geo, on="customer_id", how="left")
        .merge(store_geo, on="store_id", how="left")
        .rename(columns={"amount": "payment_amount"})
    )

    # parse dates if present
    if "payment_date" in df.columns:
        df["payment_date"] = pd.to_datetime(df["payment_date"])

    return df


df = load_data()

df = load_data()


st.title("Film Rental Insights")

# ---------- REVENUE BY CATEGORY ----------
st.header("1. Revenue by Category")

cat_rev = (
    df.groupby("category_name")["payment_amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(cat_rev)

st.dataframe(
    cat_rev.reset_index().rename(columns={"payment_amount": "total_revenue"}),
    hide_index=True,
    use_container_width=True,
)

# Insight message
total_rev = cat_rev.sum()
top_cat = cat_rev.idxmax()
top_cat_value = cat_rev.max()
top_cat_pct = (top_cat_value / total_rev * 100) if total_rev else 0

st.markdown(
    f"""
**Insight:**  
The highest-grossing category is **{top_cat}**, generating **£{top_cat_value:,.2f}**,  
which is about **{top_cat_pct:.1f}%** of all recorded revenue across categories.
"""
)
st.caption(
    "Use this to identify your 'cash cow' genres and where to prioritise stock/marketing."
)


# ---------- REVENUE PER COUNTRY (WITH STORE FILTER) ----------
st.header("2. Revenue per Country (with Store Filter)")

stores = sorted(df["store_id"].dropna().unique())
selected_stores = st.multiselect(
    "Select store(s):",
    options=stores,
    default=stores,
)

filtered = df[df["store_id"].isin(selected_stores)].copy()

country_rev = (
    filtered.groupby("customer_country")["payment_amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(country_rev)

st.dataframe(
    country_rev.reset_index().rename(
        columns={"payment_amount": "total_revenue"}
    ),
    hide_index=True,
    use_container_width=True,
)

if not filtered.empty and not country_rev.empty:
    top_country = country_rev.idxmax()
    top_country_value = country_rev.max()
    st.markdown(
        f"""
**Insight:**  
For the selected store(s) **{', '.join(map(str, selected_stores))}**,  
the top customer country is **{top_country}** with **£{top_country_value:,.2f}** in revenue.
"""
    )
else:
    st.info("No data for the selected store(s). Try adjusting the filters.")

# ---------- REVENUE / PAYMENTS BY RATING ----------
st.header("3. Revenue & Payments by Film Rating")

rating_group = df.groupby("rating").agg(
    total_revenue=("payment_amount", "sum"),
    num_payments=("payment_id", "nunique"),
)

rating_group["avg_revenue_per_payment"] = (
    rating_group["total_revenue"] / rating_group["num_payments"]
)

metric_choice = st.radio(
    "Metric:",
    ["Total revenue", "Average revenue per payment", "Number of payments"],
    horizontal=True,
)

if metric_choice == "Total revenue":
    series = rating_group["total_revenue"].sort_values(ascending=False)
elif metric_choice == "Average revenue per payment":
    series = rating_group["avg_revenue_per_payment"].sort_values(
        ascending=False
    )
else:
    series = rating_group["num_payments"].sort_values(ascending=False)

st.bar_chart(series)
st.dataframe(
    rating_group.sort_values("total_revenue", ascending=False),
    use_container_width=True,
)

# Insight
if not rating_group.empty:
    if metric_choice == "Total revenue":
        top_rating = rating_group["total_revenue"].idxmax()
        val = rating_group["total_revenue"].max()
        st.markdown(
            f"**Insight:** Rating **{top_rating}** delivers the **highest total revenue** at **£{val:,.2f}**."
        )
    elif metric_choice == "Average revenue per payment":
        top_rating = rating_group["avg_revenue_per_payment"].idxmax()
        val = rating_group["avg_revenue_per_payment"].max()
        st.markdown(
            f"**Insight:** Rating **{top_rating}** has the **highest revenue per payment**, "
            f"averaging **£{val:,.2f}** per transaction."
        )
    else:
        top_rating = rating_group["num_payments"].idxmax()
        val = rating_group["num_payments"].max()
        st.markdown(
            f"**Insight:** Rating **{top_rating}** is **rented the most often**, with **{val:,} payments**."
        )
st.caption(
    "This helps decide which rating bands bring in volume vs high-value transactions."
)

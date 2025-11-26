import streamlit as st
import pandas as pd
import os

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
# Title

st.title("Revenue and Customer Analysis Dashboard")


# Paths

# Calculate the correct base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # etl_film folder
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

# Define CSV paths
CSV_FILES = {
    "Revenue": "SV_revenue_by_category.csv",
    "Payment": "payment.csv",
    "Rental": "rental.csv",
    "Customer": "customer.csv",
    "Film": "film.csv",
    "Film_Actor": "film_actor.csv"
}


# Load CSVs

data = {}

for key, file in CSV_FILES.items():
    path = os.path.join(OUTPUT_DIR, file)
    if os.path.exists(path):
        try:
            data[key] = pd.read_csv(path)
           # st.write(f"{key} CSV loaded successfully.")
        except Exception as e:
            st.error(f"Error loading {key} CSV: {e}")
            data[key] = None
    else:
        st.warning(f"{key} CSV NOT found at path: {path}")
        data[key] = None


# Revenue by Category

if data["Revenue"] is not None:
    st.subheader("Revenue by Film Category")
    df_rev = data["Revenue"]
    st.dataframe(df_rev)
    st.bar_chart(df_rev.set_index("category_name")["amount"])
else:
    st.info("Revenue data not available.")

# Payment Dates Filter

if data["Payment"] is not None:
    df_pay = data["Payment"]
    
    # Convert date column
    if 'payment_date' in df_pay.columns:
        df_pay['payment_date'] = pd.to_datetime(df_pay['payment_date'], errors='coerce')
        min_date = df_pay['payment_date'].min()
        max_date = df_pay['payment_date'].max()
        
        st.subheader("Filter Payments by Date")
        start_date, end_date = st.date_input(
            "Select date range:",
            [min_date, max_date]
        )
        df_pay_filtered = df_pay[
            (df_pay['payment_date'] >= pd.Timestamp(start_date)) &
            (df_pay['payment_date'] <= pd.Timestamp(end_date))
        ]
        st.dataframe(df_pay_filtered)
    else:
        st.warning("Payment CSV does not contain 'payment_date' column.")
else:
    st.info("Payment data not available for date filtering.")


# Top 10 Customers

if data["Customer"] is not None and data["Payment"] is not None:
    st.subheader("Top 10 Customers by Payment Amount")
    df_cust = data["Customer"]
    df_cust_pay = pd.merge(df_pay, df_cust, left_on="customer_id", right_on="customer_id", how="inner")
    top_customers = df_cust_pay.groupby(["customer_id", "first_name", "last_name"])["amount"].sum().reset_index()
    top_customers = top_customers.sort_values("amount", ascending=False)
    st.dataframe(top_customers.head(10))
else:
    st.info("Customer data not available.")


# Most Rented Films

if data["Rental"] is not None and data["Film"] is not None and data["Film_Actor"] is not None:
    st.subheader("Most Rented Films")
    df_rental = data["Rental"]
    df_film = data["Film"]
    
    # Count rentals per film_id
    rentals_count = df_rental.groupby("inventory_id").size().reset_index(name="rental_count")
    
    # Join with film (need inventory -> film mapping)
    if "inventory_id" in df_rental.columns and "film_id" in df_film.columns:
        df_inventory_film = df_rental.merge(df_film, left_on="inventory_id", right_on="film_id", how="left")
        most_rented = df_inventory_film.groupby("title").size().reset_index(name="rental_count").sort_values("rental_count", ascending=False)
        st.dataframe(most_rented.head(10))
    else:
        st.warning("Cannot calculate most rented films: missing required columns.")
else:
    st.info("Film rental data not available.")



# Interactive Revenue Filter (Multiple Categories)

if data["Revenue"] is not None and data["Payment"] is not None:
    st.subheader("Interactive Revenue Filter by Category and Month")
    
    # Ensure payment_date exists and is datetime
    df_pay['payment_date'] = pd.to_datetime(df_pay['payment_date'], errors='coerce')
    
    # Month selection
    df_pay['month'] = df_pay['payment_date'].dt.to_period('M')
    months = df_pay['month'].dropna().sort_values().unique()
    selected_month = st.selectbox("Select Month", months)
    
    # Multi-category selection
    categories = df_rev['category_name'].unique()
    selected_categories = st.multiselect("Select Film Categories", categories, default=categories[:1])
    
    # Filter revenue by selected categories
    df_filtered = df_rev[df_rev['category_name'].isin(selected_categories)]
    
    # Show filtered data
    st.write(f"Revenue for {', '.join(selected_categories)} in {selected_month}:")
    st.dataframe(df_filtered)
    
    # Sum revenue if multiple categories selected
    st.bar_chart(df_filtered.groupby("category_name")["amount"].sum())
else:
    st.info("Revenue or Payment data not available for interactive filtering.")

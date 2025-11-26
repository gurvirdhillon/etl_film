import os
import pandas as pd

# Build absolute, safe path to /data/output
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
output_path = os.path.join(BASE_DIR, "data", "output")

# Load files
payments = pd.read_csv(os.path.join(output_path, "payment.csv"))
rentals = pd.read_csv(os.path.join(output_path, "rental.csv"))
inventory = pd.read_csv(os.path.join(output_path, "inventory.csv"))
film = pd.read_csv(os.path.join(output_path, "film.csv"))
film_category = pd.read_csv(os.path.join(output_path, "film_category.csv"))
category = pd.read_csv(os.path.join(output_path, "category.csv"))

print("All CSVs loaded successfully!")

print("Starting revenue-by-category EDA...")

# --- Merge tables to reach category + payment amount ---

# 1. payment → rental
merged = payments.merge(
    rentals[["rental_id", "inventory_id"]],
    on="rental_id",
    how="left"
)

# 2. add inventory → film_id
merged = merged.merge(
    inventory[["inventory_id", "film_id"]],
    on="inventory_id",
    how="left"
)

# 3. add film_category → category
merged = merged.merge(
    film_category[["film_id", "category_id"]],
    on="film_id",
    how="left"
)

# 4. add category name
merged = merged.merge(
    category[["category_id", "name"]],
    on="category_id",
    how="left"
)

# Rename column for clarity
merged.rename(columns={"name": "category_name"}, inplace=True)

# --- Group and calculate revenue ---
revenue_by_category = (
    merged.groupby("category_name")["amount"]
    .sum()
    .reset_index()
    .sort_values("amount", ascending=False)
)

print("\nRevenue by film category (top results):\n")
print(revenue_by_category)

# Save as CSV for Streamlit
output_csv = os.path.join(output_path, "SV_revenue_by_category.csv")
revenue_by_category.to_csv(output_csv, index=False)

print(f"\nRevenue file saved to:\n{output_csv}")


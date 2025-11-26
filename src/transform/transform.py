import pandas as pd


def clean_actor(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}actor.csv")

    if df is None:
        return False

    # No cleaning was necessary
    df.to_csv(f"{write_dir}actor_cleaned.csv")

    return True


def clean_address(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}address.csv")
    
    if df is None:
        return False
    
    df.drop('address2', axis=1)  # address2 is empty
    df.dropna()  # evaluated as reasonable

    df.to_csv(f"{write_dir}address_cleaned.csv")

    return True


def clean_app_id(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}app_id.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}app_id_cleaned.csv")

    return True


def clean_category(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}category.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}category_cleaned.csv")

    return True


def clean_city(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}city.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}city_cleaned.csv")

    return True


def clean_country(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}country.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}country_cleaned.csv")

    return True


def clean_customer(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}customer.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}customer_cleaned.csv")

    return True


def clean_film_actor(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}film_actor.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}film_actor_cleaned.csv")

    return True


def clean_film_category(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}film_category.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}film_category_cleaned.csv")

    return True


def clean_film(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}film.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}film_cleaned.csv")

    return True


def clean_inventory(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}inventory.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}inventory_cleaned.csv")

    return True


def clean_language(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}language.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}language_cleaned.csv")

    return True


def clean_payment(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}payment.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}payment_cleaned.csv")

    return True


def clean_rental(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}rental.csv")
    
    if df is None:
        return False
    
    df["rental_date"] = pd.to_datetime(df["rental_date"])
    df["return_date"] = pd.to_datetime(df["return_date"])
    df["last_update"] = pd.to_datetime(df["last_update"])
    
    newest_record = df['last_update'].max()
    
    df['return_date'] = df['return_date'].fillna(newest_record)  # replace seemingly unreturned rentals with the longest possible time

    df.to_csv(f"{write_dir}rental_cleaned.csv")

    return True


def clean_staff(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}staff.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}staff_cleaned.csv")

    return True


def clean_store(write_dir, read_dir):

    df = pd.read_csv(f"{read_dir}store.csv")
    
    if df is None:
        return False
    
    # No cleaning was necessary
    df.to_csv(f"{write_dir}store_cleaned.csv")
    return True


def run_cleaners():

    count = 0
    write_dir = "../data/processed/"
    read_dir = "../data/output/"

    cleaners = [clean_actor, clean_address, clean_app_id, clean_category, clean_city, clean_country, clean_customer, clean_film_actor, clean_film, clean_inventory, clean_language, clean_payment, clean_rental, clean_staff, clean_store]  

    for cleaner in cleaners:

        success = cleaner(write_dir, read_dir)
 
        if not success:
            print(f"{cleaner.__name__} failed")
            count += 1
            
    print(f"Cleaning process complete with {count} failures")



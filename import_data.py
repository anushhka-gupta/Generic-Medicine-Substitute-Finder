import pandas as pd
from db import get_connection

def import_csv_to_db(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]

    df = df.rename(columns={'price(₹)': 'price'})

    columns = ['id', 'name', 'price', 'Is_discontinued', 'manufacturer_name',
               'type', 'pack_size_label', 'short_composition1', 'short_composition2']

    df = df[columns]

    # Force object dtype so NaN -> None conversion actually sticks
    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO medicines
                (id, name, price, is_discontinued, manufacturer_name, type, pack_size_label, short_composition1, short_composition2)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            records = df.values.tolist()
            cur.executemany(insert_query, records)
        print(f"Inserted {len(records)} rows successfully.")
    except Exception as e:
        print(f"Error during import: {e}")
    finally:
        conn.close()


if __name__ == '__main__':
    import_csv_to_db('./dataset/A_Z_medicines_dataset_of_India.csv')
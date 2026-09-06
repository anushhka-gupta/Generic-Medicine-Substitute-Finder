import pymysql
import pymysql.cursors

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='Substitute_Finder_App',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def get_medicines_data():
    try:
        conn = get_connection()
    except Exception as e:
        print(f'Exception in connecting to the database: ', e)
        return {"rows": None, "error": str(e)}

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM medicines
                """
            )
            rows = cur.fetchall()
            return {"rows": rows, "error": None}
    except Exception as e:
        print(f'Exception in SELECT Operation: ', e)
        return {"rows": None, "error": str(e)}
    finally:
        conn.close()
import psycopg2
import config

def get_connection():
    """Create a new Postgres connection using config.py values."""
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

def list_tables():
    """Fetch all tables in the public schema."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return tables

def list_columns(table_name):
    """Fetch all columns and their data types for a given table."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s;
    """, (table_name,))
    columns = cur.fetchall()
    cur.close()
    conn.close()
    return columns

if __name__ == "__main__":
    tables = list_tables()
    print("Tables in DB:", tables)
    for t in tables:
        print(f"\nColumns in {t}:")
        for col, dtype in list_columns(t):
            print(f"  - {col} ({dtype})")

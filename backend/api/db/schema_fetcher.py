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

def list_foreign_keys(table_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            tc.constraint_name, kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s;
    """, (table_name,))
    fkeys = cur.fetchall()
    cur.close()
    conn.close()
    return fkeys

def get_schema_snapshot():
    schema = {}
    for t in list_tables():
        schema[t] = list_columns(t)
    return schema

if __name__ == "__main__":
    snapshot = get_schema_snapshot()
    print("Schema Snapshot:")
    for table, columns in snapshot.items():
        print(f"\n{table}:")
        for col, dtype in columns:
            print(f"  - {col} ({dtype})")

        fkeys = list_foreign_keys(table)
        if fkeys:
            print("  Foreign Keys:")
            for fk in fkeys:
                print(f"    {fk}")

import psycopg2
import backend.core.config as config

def get_connection():
    """Create a new Postgres connection using config.py values."""
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

def execute_sql(sql: str):
    """
    Execute a SQL SELECT query and return results.
    Restrict to SELECT for safety.
    """
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        return {"columns": colnames, "rows": rows}
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Example run
    query = "SELECT id, name, department FROM employees WHERE salary > 70000;"
    result = execute_sql(query)

    print("Columns:", result["columns"])
    for row in result["rows"]:
        print(row)

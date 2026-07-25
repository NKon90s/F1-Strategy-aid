import psycopg2

def connect_to_db():
    print("Connecting to PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            host = "localhost",
            port = 5432,
            dbname = "db",
            user = "db_user",
            password = "db_password"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed {e}")
        raise  
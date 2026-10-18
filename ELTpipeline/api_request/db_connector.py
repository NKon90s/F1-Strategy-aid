import psycopg2
import os 

###################################################################
#  The connector is environment-aware.     
#  It can be run from the code-editor but the airflow DAG 
#  can run it as well.
###################################################################

def connect_to_db():
    print("Connecting to PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            host = os.getenv("DB_HOST", "localhost"),
            port = int(os.getenv("DB_PORT", 5000)),
            dbname = os.getenv("DB_NAME", "db"),
            user = os.getenv("DB_USER", "db_user"),
            password = os.getenv("DB_PASSWORD", "db_password")
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed {e}")
        raise  
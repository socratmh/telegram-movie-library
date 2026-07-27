import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def run_migration():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("Error: DATABASE_URL not found in .env")
        return
        
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    if "sslmode=" not in db_url:
        separator = "&" if "?" in db_url else "?"
        db_url = f"{db_url}{separator}sslmode=require"
    
    # Fix Supabase pooler port if they mistakenly used 5432
    if ".pooler.supabase.com:5432" in db_url:
        db_url = db_url.replace(".pooler.supabase.com:5432", ".pooler.supabase.com:6543")
        
    print(f"Connecting to Supabase PostgreSQL: {db_url.split('@')[-1]}")
    engine = create_engine(db_url, pool_pre_ping=True, isolation_level="AUTOCOMMIT")
    
    with engine.connect() as conn:
        tables = ["libraries", "tv_libraries"]
        
        for table in tables:
            print(f"--- Migrating table: {table} ---")
            
            # Add name_en
            try:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN name_en VARCHAR;"))
                print(f"[{table}] Added column name_en")
            except Exception as e:
                print(f"[{table}] name_en might already exist: {e}")
                
            # Add is_active
            try:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN is_active BOOLEAN DEFAULT true;"))
                print(f"[{table}] Added column is_active")
            except Exception as e:
                print(f"[{table}] is_active might already exist: {e}")

if __name__ == "__main__":
    run_migration()

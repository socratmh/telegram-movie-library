from database.models import get_db_url, init_db
from sqlalchemy import text
from backend.config import get_database_url, get_database_path
import traceback

def run_migration():
    db_url = get_db_url(get_database_url(), get_database_path())
    Session = init_db(db_url)
    print(f"Migrating database: {db_url}")
    
    with Session() as db:
        try:
            db.execute(text("ALTER TABLE libraries ADD COLUMN name_en VARCHAR"))
            print("Successfully added name_en to libraries.")
        except Exception as e:
            print(f"Skipping libraries (column might already exist): {e}")
            db.rollback()

        try:
            db.execute(text("ALTER TABLE tv_libraries ADD COLUMN name_en VARCHAR"))
            print("Successfully added name_en to tv_libraries.")
        except Exception as e:
            print(f"Skipping tv_libraries (column might already exist): {e}")
            db.rollback()

        db.commit()

if __name__ == "__main__":
    run_migration()

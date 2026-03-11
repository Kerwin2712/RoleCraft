import sqlite3

def migrate():
    conn = sqlite3.connect("rolecraft.sqlite3")
    cursor = conn.cursor()
    
    # Migrar users
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN skill_backend INTEGER DEFAULT 0;")
        cursor.execute("ALTER TABLE users ADD COLUMN skill_frontend INTEGER DEFAULT 0;")
        cursor.execute("ALTER TABLE users ADD COLUMN skill_git INTEGER DEFAULT 0;")
        cursor.execute("ALTER TABLE users ADD COLUMN skill_ia INTEGER DEFAULT 0;")
        cursor.execute("ALTER TABLE users ADD COLUMN skill_pm INTEGER DEFAULT 0;")
        print("Migración de users exitosa.")
    except sqlite3.OperationalError as e:
        print(f"Error o ya migrado en users: {e}")

    # Migrar groups
    try:
        cursor.execute("ALTER TABLE groups ADD COLUMN phase INTEGER DEFAULT 1;")
        cursor.execute("ALTER TABLE groups ADD COLUMN vacant_roles VARCHAR(255) DEFAULT '';")
        print("Migración de groups exitosa.")
    except sqlite3.OperationalError as e:
        print(f"Error o ya migrado en groups: {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()

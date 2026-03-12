import sqlite3

def migrate():
    conn = sqlite3.connect("rolecraft.sqlite3")
    cursor = conn.cursor()
    
    # Migrar users
    columns_users = [
        ("skill_backend", "INTEGER DEFAULT 0"),
        ("skill_frontend", "INTEGER DEFAULT 0"),
        ("skill_git", "INTEGER DEFAULT 0"),
        ("skill_ia", "INTEGER DEFAULT 0"),
        ("skill_pm", "INTEGER DEFAULT 0"),
        ("skill_sql", "INTEGER DEFAULT 0")
    ]
    
    for col_name, col_type in columns_users:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};")
            print(f"Columna {col_name} añadida a users.")
        except sqlite3.OperationalError:
            print(f"Columna {col_name} ya existe en users.")

    # Migrar groups
    columns_groups = [
        ("phase", "INTEGER DEFAULT 1"),
        ("vacant_roles", "VARCHAR(255) DEFAULT ''")
    ]
    
    for col_name, col_type in columns_groups:
        try:
            cursor.execute(f"ALTER TABLE groups ADD COLUMN {col_name} {col_type};")
            print(f"Columna {col_name} añadida a groups.")
        except sqlite3.OperationalError:
            print(f"Columna {col_name} ya existe en groups.")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()

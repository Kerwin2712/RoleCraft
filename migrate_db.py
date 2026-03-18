import sqlite3

def migrate():
    conn = sqlite3.connect('rolecraft.sqlite3')
    cursor = conn.cursor()
    
    # Agregar columnas a users si no existen
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN coins INTEGER DEFAULT 0")
        print("Añadida columna 'coins' a 'users'")
    except sqlite3.OperationalError:
        print("Columna 'coins' ya existe")

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN question_stock INTEGER DEFAULT 20")
        print("Añadida columna 'question_stock' a 'users'")
    except sqlite3.OperationalError:
        print("Columna 'question_stock' ya existe")

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN last_stock_recharge DATETIME")
        print("Añadida columna 'last_stock_recharge' a 'users'")
    except sqlite3.OperationalError:
        print("Columna 'last_stock_recharge' ya existe")

    # Agregar columnas a user_module_progress
    try:
        cursor.execute("ALTER TABLE user_module_progress ADD COLUMN evaluation_queue TEXT")
        print("Añadida columna 'evaluation_queue' a 'user_module_progress'")
    except sqlite3.OperationalError:
        print("Columna 'evaluation_queue' ya existe")

    try:
        cursor.execute("ALTER TABLE user_module_progress ADD COLUMN current_streak INTEGER DEFAULT 0")
        print("Añadida columna 'current_streak' a 'user_module_progress'")
    except sqlite3.OperationalError:
        print("Columna 'current_streak' ya existe")

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_polyglot INTEGER DEFAULT 0")
        print("Añadida columna 'is_polyglot' a 'users'")
    except sqlite3.OperationalError:
        print("Columna 'is_polyglot' ya existe")

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN last_exam_attempt DATETIME")
        print("Añadida columna 'last_exam_attempt' a 'users'")
    except sqlite3.OperationalError:
        print("Columna 'last_exam_attempt' ya existe")

    conn.commit()
    conn.close()
    print("Migración completada con éxito.")

if __name__ == "__main__":
    migrate()

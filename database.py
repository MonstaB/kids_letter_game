import sqlite3


def setup_database():
    print("Setting up database...")
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
                        group_id INTEGER PRIMARY KEY,
                        group_name TEXT NOT NULL,
                        is_active INTEGER DEFAULT 1
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        group_id INTEGER,
                        is_admin INTEGER DEFAULT 0,
                        find_the_letter_rounds INTEGER DEFAULT 4,
                        find_the_letter_attempts INTEGER DEFAULT 0,
                        FOREIGN KEY(group_id) REFERENCES groups(group_id)
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                        game_id INTEGER PRIMARY KEY,
                        game_name TEXT NOT NULL,
                        default_rounds INTEGER
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS attempts (
                        attempt_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        game_id INTEGER,
                        letter TEXT,
                        attempts INTEGER,
                        FOREIGN KEY(user_id) REFERENCES users(user_id),
                        FOREIGN KEY(game_id) REFERENCES games(game_id)
                    )''')
    cursor.execute('''INSERT OR IGNORE INTO games (game_id, game_name, default_rounds)
                      VALUES (1, "find the letter", 4)''')
    conn.commit()
    conn.close()
    print("Database setup complete.")


def add_admin(username, password, group_name):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groups (group_name) VALUES (?)", (group_name,))
    group_id = cursor.lastrowid
    cursor.execute("INSERT INTO users (username, password, group_id, is_admin) VALUES (?, ?, ?, 1)",
                   (username, password, group_id))
    conn.commit()
    conn.close()


def check_admin_exists():
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE is_admin = 1")
    admin_exists = cursor.fetchone() is not None
    conn.close()
    return admin_exists


def record_attempt(user_id, game_id, letter, attempts):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attempts (user_id, game_id, letter, attempts) VALUES (?, ?, ?, ?)",
                   (user_id, game_id, letter, attempts))
    conn.commit()
    conn.close()


def increment_games_played(user_id):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET find_the_letter_attempts = find_the_letter_attempts + 1 WHERE user_id = ?",
                   (user_id,))
    cursor.execute("SELECT find_the_letter_attempts FROM users WHERE user_id = ?", (user_id,))
    attempts = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return attempts


def record_game(user_id, score):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO games (user_id, score) VALUES (?, ?)", (user_id, score))
    game_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return game_id


def add_new_group(group_name):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groups (group_name) VALUES (?)", (group_name,))
    conn.commit()
    conn.close()


def get_all_groups():
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT group_id, group_name, is_active FROM groups")
    groups = cursor.fetchall()
    conn.close()
    return groups


def disable_group(group_id, status):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE groups SET is_active = ? WHERE group_id = ?", (status, group_id))
    conn.commit()
    conn.close()


def get_admin(username, password):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ? AND is_admin = 1",
                   (username, password))
    admin = cursor.fetchone()
    conn.close()
    return admin


def create_user(username, password, group_id):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, group_id) VALUES (?, ?, ?)",
                       (username, password, group_id))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()
    return True


def validate_user(username, password):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


# Add these functions to database.py

def get_user_id(username):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]  # Return user_id only
    else:
        return None


def get_games_played(user_id):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT games_played FROM users WHERE user_id = ?", (user_id,))
    games_played = cursor.fetchone()
    conn.close()
    if games_played:
        return games_played[0]
    else:
        return 0


setup_database()

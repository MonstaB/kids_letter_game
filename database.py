import sqlite3

def setup_database():
    print("Setting up database...")
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        games_played INTEGER DEFAULT 0
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                        game_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        score INTEGER,
                        FOREIGN KEY(user_id) REFERENCES user_data(user_id)
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS attempts (
                        attempt_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        game_id INTEGER,
                        letter TEXT,
                        attempts INTEGER,
                        FOREIGN KEY(user_id) REFERENCES user_data(user_id),
                        FOREIGN KEY(game_id) REFERENCES games(game_id)
                    )''')
    conn.commit()
    conn.close()
    print("Database setup complete.")

def get_user_id(username):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, games_played FROM user_data WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    if user_data is None:
        cursor.execute("INSERT INTO user_data (username) VALUES (?)", (username,))
        conn.commit()
        user_id = cursor.lastrowid
        games_played = 0
    else:
        user_id, games_played = user_data
    conn.close()
    return user_id, games_played

def increment_games_played(user_id):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user_data SET games_played = games_played + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    cursor.execute("SELECT games_played FROM user_data WHERE user_id = ?", (user_id,))
    games_played = cursor.fetchone()[0]
    conn.close()
    return games_played

def record_game(user_id, score):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO games (user_id, score) VALUES (?, ?)", (user_id, score))
    conn.commit()
    game_id = cursor.lastrowid
    conn.close()
    return game_id

def record_attempt(user_id, game_id, letter, attempts):
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attempts (user_id, game_id, letter, attempts) VALUES (?, ?, ?, ?)",
                   (user_id, game_id, letter, attempts))
    conn.commit()
    conn.close()

# Ensure the database is set up when the module is imported
setup_database()

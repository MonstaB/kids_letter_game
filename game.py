import random
import sqlite3

import pygame
import pyttsx3
from database import get_user_id, record_attempt, increment_games_played, record_game


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_random_letter():
    return chr(random.randint(65, 90))  # ASCII values for A-Z


def get_user_input():
    running = True
    user_input = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                user_input = pygame.key.name(event.key)
                running = False
    return user_input.upper()


def play_game(username, screen, font):
    custom_font_path = 'assets/fonts/212Keyboard.otf'
    custom_font = pygame.font.Font(custom_font_path, 36)

    user_id = get_user_id(username)
    games_played = increment_games_played(user_id)
    score = 0
    total_attempts = 0
    game_id = record_game(user_id, score)

    for _ in range(10):
        target_letter = get_random_letter()
        speak(f"Find the {target_letter} key")
        attempts = 0
        while True:
            screen.fill((255, 255, 255))
            display_text(screen, font, f"Find the '{target_letter}' key", 100, 100)
            display_text(screen, font, f"Score: {score}", 100, 200)
            display_text(screen, font, f"Current user: {username}", 100, 250)
            pygame.display.flip()
            user_input = get_user_input()
            attempts += 1
            if user_input == target_letter:
                screen.fill((0, 255, 0))
                display_text(screen, font, f"Congratulations! You found the", 100, 300)
                display_text(screen, custom_font, f"'{target_letter}'", 500, 300)
                pygame.display.flip()
                pygame.time.delay(1000)
                speak("Correct")
                score += 1
                break
            else:
                speak(f"Try again, Find the {target_letter} key")
        record_attempt(user_id, game_id, target_letter, attempts)
        total_attempts += attempts

    speak(f"Your score is {score}")
    conn = sqlite3.connect('letter_game.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE games SET score = ? WHERE game_id = ?", (score, game_id))
    conn.commit()
    conn.close()


def display_text(screen, font, text, x, y):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))

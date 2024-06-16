import pygame
from game import play_game


def display_text(screen, font, text, x, y):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))


def game_menu(screen, font, username, user_id):
    running = True
    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, f"Welcome, {username}", 100, 50)
        display_text(screen, font, "1. Find the Letter", 100, 150)
        display_text(screen, font, "2. Exit", 100, 200)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_game(username, screen, font)
                elif event.key == pygame.K_2:
                    running = False
    return True

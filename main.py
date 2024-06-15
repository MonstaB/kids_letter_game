import pygame
from game import play_game, display_text


def main_menu(screen, font):
    running = True
    username = None
    input_active = False
    user_input_text = ''
    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, "1. New User", 100, 100)
        display_text(screen, font, "2. Existing User", 100, 150)
        display_text(screen, font, "3. Exit", 100, 200)
        if username:
            display_text(screen, font, f"Current user: {username}", 100, 250)
        if input_active:
            display_text(screen, font, f"Enter username: {user_input_text}", 100, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        username = user_input_text
                        user_input_text = ''
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input_text = user_input_text[:-1]
                    else:
                        user_input_text += event.unicode
                else:
                    if event.key == pygame.K_1 or event.key == pygame.K_2:
                        input_active = True
                        user_input_text = ''
                    elif event.key == pygame.K_3:
                        running = False
                    elif event.key == pygame.K_RETURN and username:
                        play_game(username, screen, font)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Letter Game')
    font = pygame.font.Font(None, 36)
    main_menu(screen, font)
    pygame.quit()

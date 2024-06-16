import pygame
from game_menu import game_menu
from admin_menu import admin_menu
from database import get_user_id, create_user, validate_user, get_all_groups


def display_text(screen, font, text, x, y):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))


def main_menu(screen, font):
    running = True
    option = None

    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, "Main Menu", 100, 50)
        display_text(screen, font, "1. Create Account", 100, 150)
        display_text(screen, font, "2. Sign In", 100, 200)
        display_text(screen, font, "3. Admin", 100, 250)
        display_text(screen, font, "4. Exit", 100, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    option = "create_account"
                elif event.key == pygame.K_2:
                    option = "sign_in"
                elif event.key == pygame.K_3:
                    admin_menu(screen, font)
                elif event.key == pygame.K_4:
                    running = False

        if option == "create_account":
            create_account(screen, font)
            option = None
        elif option == "sign_in":
            sign_in(screen, font)
            option = None

    return True


def create_account(screen, font):
    username = ''
    password = ''
    group_id = None
    input_field = 0
    error_message = None

    groups = get_all_groups()
    group_names = [group[1] for group in groups]

    running = True
    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, "Create Account", 100, 50)
        display_text(screen, font, "Enter Username:", 100, 150)
        display_text(screen, font, username if input_field != 1 else username + "|", 300, 150)
        display_text(screen, font, "Enter Password:", 100, 200)
        display_text(screen, font, "*" * len(password) if input_field != 2 else "*" * len(password) + "|", 300, 200)
        display_text(screen, font, "Select Group:", 100, 250)
        for i, group_name in enumerate(group_names):
            display_text(screen, font, f"{i + 1}. {group_name}", 300, 250 + i * 30)
        display_text(screen, font, "Press Enter to submit", 100, 400)
        if error_message:
            display_text(screen, font, error_message, 100, 450)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_field == 3:
                        if not group_id:
                            error_message = "Please select a group."
                        else:
                            if create_user(username, password, group_id):
                                running = False
                            else:
                                error_message = "Username already exists."
                    else:
                        input_field += 1
                elif event.key == pygame.K_BACKSPACE:
                    if input_field == 1:
                        username = username[:-1]
                    elif input_field == 2:
                        password = password[:-1]
                elif event.key in range(pygame.K_1, pygame.K_1 + len(group_names)):
                    group_id = groups[event.key - pygame.K_1][0]
                else:
                    if input_field == 1:
                        username += event.unicode
                    elif input_field == 2:
                        password += event.unicode


def sign_in(screen, font):
    username = ''
    password = ''
    input_field = 0
    error_message = None

    running = True
    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, "Sign In", 100, 50)
        display_text(screen, font, "Enter Username:", 100, 150)
        display_text(screen, font, username if input_field != 1 else username + "|", 300, 150)
        display_text(screen, font, "Enter Password:", 100, 200)
        display_text(screen, font, "*" * len(password) if input_field != 2 else "*" * len(password) + "|", 300, 200)
        display_text(screen, font, "Press Enter to submit", 100, 250)
        if error_message:
            display_text(screen, font, error_message, 100, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_field == 2:
                        user = validate_user(username, password)
                        if user:
                            game_menu(screen, font, username, user[0])
                            running = False
                        else:
                            error_message = "Incorrect username or password."
                    else:
                        input_field += 1
                elif event.key == pygame.K_BACKSPACE:
                    if input_field == 1:
                        username = username[:-1]
                    elif input_field == 2:
                        password = password[:-1]
                else:
                    if input_field == 1:
                        username += event.unicode
                    elif input_field == 2:
                        password += event.unicode

    return True

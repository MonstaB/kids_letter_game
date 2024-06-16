import pygame
from database import add_admin, disable_group, add_new_group, get_all_groups, get_admin


def display_text(screen, font, text, x, y):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))


def admin_menu(screen, font):
    running = True
    username = ''
    password = ''
    input_field = 0
    error_message = None

    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, "Admin Login", 100, 50)
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
                        admin = get_admin(username, password)
                        if admin:
                            admin_options(screen, font)
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


def admin_options(screen, font):
    running = True
    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, "Admin Options", 100, 50)
        display_text(screen, font, "1. View Users", 100, 150)
        display_text(screen, font, "2. Add New Group", 100, 200)
        display_text(screen, font, "3. Disable Groups", 100, 250)
        display_text(screen, font, "4. Exit", 100, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    view_users(screen, font)
                elif event.key == pygame.K_2:
                    add_group(screen, font)
                elif event.key == pygame.K_3:
                    disable_groups(screen, font)
                elif event.key == pygame.K_4:
                    running = False
    return True


def view_users(screen, font):
    pass  # Implement view users functionality here


def add_group(screen, font):
    running = True
    group_name = ''
    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, "Enter new group name:", 100, 150)
        display_text(screen, font, group_name if group_name else "|", 300, 200)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    add_new_group(group_name)
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    group_name = group_name[:-1]
                else:
                    group_name += event.unicode


def disable_groups(screen, font):
    running = True
    while running:
        screen.fill((255, 255, 255))
        display_text(screen, font, "Disable Groups", 100, 50)
        groups = get_all_groups()
        y = 150
        for group in groups:
            group_id, group_name, is_active = group
            display_text(screen, font, f"{group_name} {'(Active)' if is_active else '(Inactive)'}", 100, y)
            y += 50
        display_text(screen, font, "Press Enter to toggle status", 100, y)
        display_text(screen, font, "Press ESC to exit", 100, y + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for group in groups:
                        group_id, group_name, is_active = group
                        disable_group(group_id, not is_active)
                    groups = get_all_groups()  # Refresh the groups
                elif event.key == pygame.K_ESCAPE:
                    running = False

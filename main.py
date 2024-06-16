import pygame
from main_menu import main_menu
from admin_menu import admin_menu
from database import check_admin_exists, add_admin

def display_text(screen, font, text, x, y):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))

def admin_creation(screen, font):
    input_active = False
    username = ''
    password = ''
    group_name = ''
    input_field = 0

    while True:
        screen.fill((255, 255, 255))
        display_text(screen, font, "Admin Creation", 100, 50)
        display_text(screen, font, "Enter Admin Username:", 100, 150)
        display_text(screen, font, username if input_field != 1 else username + "|", 400, 150)
        display_text(screen, font, "Enter Admin Password:", 100, 200)
        display_text(screen, font, "*" * len(password) if input_field != 2 else "*" * len(password) + "|", 400, 200)
        display_text(screen, font, "Enter Initial Group Name:", 100, 250)
        display_text(screen, font, group_name if input_field != 3 else group_name + "|", 400, 250)
        display_text(screen, font, "Press Enter to submit", 100, 350)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_field == 3:
                        add_admin(username, password, group_name)
                        display_text(screen, font, "Admin created. Please restart to continue.", 100, 400)
                        pygame.display.flip()
                        pygame.time.delay(3000)
                        return False
                    else:
                        input_field += 1
                elif event.key == pygame.K_BACKSPACE:
                    if input_field == 1:
                        username = username[:-1]
                    elif input_field == 2:
                        password = password[:-1]
                    elif input_field == 3:
                        group_name = group_name[:-1]
                else:
                    if input_field == 1:
                        username += event.unicode
                    elif input_field == 2:
                        password += event.unicode
                    elif input_field == 3:
                        group_name += event.unicode
    return True

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Letter Game')
    font = pygame.font.Font(None, 36)

    if not check_admin_exists():
        if admin_creation(screen, font):
            main_menu(screen, font)
    else:
        main_menu(screen, font)

    pygame.quit()

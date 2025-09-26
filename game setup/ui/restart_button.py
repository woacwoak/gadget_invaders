import pygame
from settings import spaceship_img, laser_sound

def draw_restart_button(screen, screen_width, screen_height):
    button_width = 300
    button_height = 60
    button_x = screen_width // 2 - button_width // 2
    button_y = screen_height // 2 - button_height // 2 + 100

    font = pygame.font.SysFont("arial", 40)
    restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Check mouse hover
    mouse_pos = pygame.mouse.get_pos()
    if restart_button_rect.collidepoint(mouse_pos):
        color = (0, 255, 0)
        draw_rect = restart_button_rect.inflate(1, 1)  # hover effect
    else:
        color = (0, 200, 0)
        draw_rect = restart_button_rect

    # Draw button
    pygame.draw.rect(screen, color, draw_rect, border_radius=15)
    text = font.render("Restart", True, (255, 255, 255))
    screen.blit(
        text,
        (draw_rect.centerx - text.get_width() // 2,
         draw_rect.centery - text.get_height() // 2)
    )

    return restart_button_rect

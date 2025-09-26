import pygame
import math
from core.utils import draw_bg
from core.stars import StarField

pygame.init()

def show_menu(screen, clock, fps, screen_width, screen_height, background_surface):
    menu_running = True

    #Fonts
    font_big = pygame.font.SysFont("arial", 80, True)
    font_small = pygame.font.SysFont("arial", 40)

    

    #Button settings
    button_width = 300
    button_height = 60
    button_x = screen_width // 2 - button_width // 2
    button_y = 400
    start_button_color = (0, 200, 0)
    quit_button_color = (200, 0, 0)
    start_button_color_hover = (0, 255, 0)
    quit_button_color_hover = (255, 0, 0)

    stars = StarField(count=50)

    # Text
    shadow_text = font_big.render("SPACE INVADERS", True, (50, 50, 50))
    title_text = font_big.render("SPACE INVADERS", True, (255, 255, 255))
    

    # Start button rectangle
    start_button_rect = pygame.Rect(button_x, 350, button_width, button_height)
    # Quit button rectangle
    quit_button_rect = pygame.Rect(button_x, 450, button_width, button_height)

    while menu_running:

        clock.tick(fps)

        draw_bg(screen, background_surface)

        stars.update()
        stars.draw(screen)

        mouse_pos = pygame.mouse.get_pos()

        if start_button_rect.collidepoint(mouse_pos):
            start_button_color = start_button_color_hover 
            start_button_rect.inflate(10, 10)
        else:
            start_button_color = (0, 200, 0)
        if quit_button_rect.collidepoint(mouse_pos):
            quit_button_color = quit_button_color_hover 
            quit_button_rect.inflate(10, 10)
        else:
            quit_button_color = (200, 0, 0)

        # Draw text
        screen.blit(shadow_text, ((screen_width//2 - title_text.get_width()//2)+4, 200+4))
        screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, 200))
        # Draw Start button
        pygame.draw.rect(screen, start_button_color, start_button_rect, border_radius=15)
        start_btn_text = font_small.render("Start (Enter)", True, (255, 255, 255))
        screen.blit(start_btn_text, (start_button_rect.centerx - start_btn_text.get_width() // 2,
                                     start_button_rect.centery - start_btn_text.get_height() // 2))

        # Draw Quit button
        pygame.draw.rect(screen, quit_button_color, quit_button_rect, border_radius=15)
        quit_button_text = font_small.render("Quit (Esc)", True, (255, 255, 255))
        screen.blit(quit_button_text, (quit_button_rect.centerx - quit_button_text.get_width() // 2,
                                    quit_button_rect.centery - quit_button_text.get_height() // 2))
        
        

        pygame.display.update()

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    menu_running = False
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game
                    menu_running = False
                if event.key == pygame.K_ESCAPE:  # Quit game
                    pygame.quit()
                    exit()

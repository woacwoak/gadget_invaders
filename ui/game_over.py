import pygame


def show_game_over(screen, clock, fps):
    font = pygame.font.SysFont(None, 100)
    running = True

    while running:
        clock.tick(fps)
        text_surface = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text_surface, ((screen.get_width() - text_surface.get_width()) // 2,
                                   (screen.get_height() - text_surface.get_height()) // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
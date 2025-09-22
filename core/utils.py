import pygame
from settings import background_img, screen_width, screen_height

def draw_bg(screen, background_surface):
    screen.blit(background_surface, (0, 0))


def show_message(
        screen, clock, fps, score,
        text, duration,
        spaceship_group,
        bullet_group, enemy_group, enemy_bullet_group, boss_bullet_group, explosion_group, boost_group,
        background_surface, stars=None, blink_spaceship=False, font_size=36):
    # Draw the message
    message_font = pygame.font.SysFont("arial", font_size, True)

    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = (current_line + " " + word).strip()
        if message_font.size(test_line)[0] < screen_width - 40:  # leave some margin
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    start_time = pygame.time.get_ticks()
    score_font = pygame.font.SysFont(None, 36)

    while pygame.time.get_ticks() - start_time < duration:
        clock.tick(fps)

        # Draw background
        draw_bg(screen, background_surface)

        for i, line in enumerate(lines):
            message_surface = message_font.render(line, True, (0, 255, 0))
            y_pos = screen_height // 2 - (len(lines) * message_surface.get_height()) // 2 + i * message_surface.get_height()
            screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, y_pos))





        # draw score
        score_text = score_font.render(f"Score: {score}", True, (0, 255, 0))
        screen.blit(score_text, score_text.get_rect(topright=(screen_width - 10, 10)))

        # Draw stars if available
        if stars:
            stars.draw(screen)

        # Draw spaceship
        if blink_spaceship:
            if ((pygame.time.get_ticks() - start_time) // 200) % 2 == 0:
                spaceship_group.draw(screen)
        else:
            spaceship_group.draw(screen)

        #Draw groups
        bullet_group.draw(screen)
        enemy_group.draw(screen)
        enemy_bullet_group.draw(screen)
        explosion_group.update()
        explosion_group.draw(screen)
        boost_group.draw(screen)
        boss_bullet_group.draw(screen)



        pygame.display.flip()

        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
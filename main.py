import pygame
import random
from settings import *
from core.player import Spaceship
from core.enemy import create_enemy_group, EnemyBullet, Boss, BossBullet
from core.stars import StarField
from core.utils import show_message
from ui.menu import show_menu
from ui.game_over import show_game_over
from core.boost import Boost

pygame.init()
pygame.mixer.init()

#Game Setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

#bg setup
background_surface = pygame.image.load(background_img).convert()
background_surface = pygame.transform.scale(background_surface, (screen_width, screen_height))

#laser sound setup
laser_sound = pygame.mixer.Sound(laser_sound)
laser_sound.set_volume(0.3)


#Sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = create_enemy_group(current_level=0)
enemy_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
boost_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
boss_bullet_group = pygame.sprite.Group()

#Player - spaceship
spaceship = Spaceship(screen_width // 2, screen_height - 100, 3, spaceship_img, laser_sound)
spaceship_group.add(spaceship)

#StarField
stars = StarField(count=50)

#Enemy shooting
last_enemy_shot = pygame.time.get_ticks()

last_boost_spawn = 0

#Levels
current_level = 1

#Boss
boss = None

def spawn_boost(boost_group):
    x = random.randint(50, screen_width - 50)
    y = -20
    boost = Boost(x, y)
    boost_group.add(boost)

#Show menu before starting
show_menu(screen, clock, FPS, screen_width, screen_height, background_surface)

#Show next level
def show_level_message(level):
    if level == 3:
        title = f"Level {level} - Boss Fight!"
    else:
        title = f"Level {level}"
    show_message(
        screen, clock, FPS, score,
        title, 1500,
        spaceship_group, bullet_group, enemy_group,
        enemy_bullet_group, boss_bullet_group, explosion_group, boost_group,
        background_surface,
        stars=stars,
        blink_spaceship=True,
        font_size=64
    )

score = 0

show_level_message(current_level)

level_messages = {
    1: "Spending 4 hours a day on your phone adds up to 1460 hours in a year!",
    2: "Take short breaks every hour to protect your eyes and mind.",
    3: "Real friends are waiting outside the screen. Go say hi!",
    4: "Every hour offline can be an hour spent learning or creating.",
    5: "Wait… you’re still here? Why are you playing so much? The game might crash soon!",
    6: "Too much screen time can affect sleep, mood, and focus.",
    7: "You control the game. Don’t let the game control you.",
    8: "Life has no respawn button — make time for real adventures!",
    9: "Too much sitting can harm your health. Get up and move!",
    10: "Blue light before bed can mess with your sleep. Log off early.",
    11: "Talking face-to-face builds stronger friendships than texting.",
}

boss_level_win = False

#Main loop
run = True
while run:
    game_over = False
    clock.tick(FPS)

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    #Draw bg
    screen.blit(background_surface, (0, 0))
    #Draw stars
    stars.update()
    stars.draw(screen)

    #draw score
    score_font = pygame.font.SysFont(None, 36)
    score_text = score_font.render(f"Score: {score}", True, (0,255,0))
    screen.blit(score_text, score_text.get_rect(topright=(screen_width - 10, 10)))

    #Booster spawn
    current_time = pygame.time.get_ticks()
    if current_time - last_boost_spawn > 20000:
        spawn_boost(boost_group)
        last_boost_spawn = current_time



    #Spaceship explosion
    explosion = spaceship.update(screen, bullet_group, stars)
    if explosion:
        explosion_group.add(explosion)
        spaceship.kill()
        game_over = True

    if game_over:
        show_game_over(screen, clock, FPS)
        break

    if stars.boost_timer:
        if pygame.time.get_ticks() - stars.boost_timer > 3000:
            stars.speed_multiplier = 1
            stars.enemy_cooldown = 500
            stars.boost_active = False
            stars.boost_timer = None

    #Enemy shooting
    enemy_cooldown = stars.enemy_cooldown
    time_now = pygame.time.get_ticks()
    if time_now - last_enemy_shot > enemy_cooldown and len(enemy_group) > 0:
        attacking_enemy = random.choice(enemy_group.sprites())
        enemy_bullet = EnemyBullet(
            attacking_enemy.rect.centerx,
            attacking_enemy.rect.bottom,
            os.path.join(img_dir, "bullet3.png")
        )
        enemy_bullet_group.add(enemy_bullet)
        last_enemy_shot = time_now

    #Boss shooting
    if boss is not None and boss.alive():
        boss_cooldown = 250
        if time_now - last_enemy_shot > boss_cooldown:
            boss_bullet = BossBullet(
                boss.rect.centerx,
                boss.rect.bottom,
                os.path.join(img_dir, "bullet3.png")
            )
            boss_bullet_group.add(boss_bullet)
            last_enemy_shot = time_now

    for bullet in enemy_bullet_group:
        bullet.update(spaceship_group, explosion_group, spaceship)

    #Event  handling
    for event in pygame.event.get():
        #if Quit Button clicked
        if event.type == pygame.QUIT:
            run = False

    if current_level != 3 and len(enemy_group) == 0:
        show_message(
            screen, clock, FPS, score,
            f"Level {current_level} Complete!", 2000,
            spaceship_group, bullet_group, enemy_group,
            enemy_bullet_group, boss_bullet_group, explosion_group, boost_group,
            background_surface, stars=stars, blink_spaceship=True, font_size=64
        )
        level_to_show = current_level
        current_level += 1
        show_message(
            screen, clock, FPS, score,
            level_messages[level_to_show], 5000,
            spaceship_group, bullet_group, enemy_group,
            enemy_bullet_group, boss_bullet_group, explosion_group, boost_group,
            background_surface, stars=stars, font_size=36
        )


        if current_level == 3:
            #Boss fight intro
            show_message(screen, clock, FPS, score,
                         "Level 3 - Boss Fight!", 1500,
                         spaceship_group, bullet_group, enemy_group,
                         enemy_bullet_group, boss_bullet_group, explosion_group, boost_group,
                         background_surface, stars=stars, blink_spaceship=True, font_size=64)
            enemy_group.empty()
            boss = Boss(screen_width // 2, 100)
            boss_group.add(boss)
        else:
            enemy_group = create_enemy_group(current_level)
            show_level_message(current_level)

            #Boss fight update and draw + health bar
    if current_level == 3 and boss is not None:
        boss.update()
        screen.blit(boss.image, boss.rect)
        boss.draw_boss_health_bar(screen)

        if boss.is_dead():
            boss.kill()
            boss_group.empty()
            score += 10
            level_to_show = current_level
            current_level += 1

            show_message(screen, clock, FPS, score, "Boss Defeated!", 1500,
                         spaceship_group, bullet_group, enemy_group,
                         enemy_bullet_group, boss_bullet_group, explosion_group, boost_group,
                         background_surface, stars=stars, blink_spaceship=True, font_size=64)

            show_message(
                screen, clock, FPS, score,
                level_messages[current_level], 5000,
                spaceship_group, bullet_group, enemy_group,
                enemy_bullet_group, boss_bullet_group, explosion_group, boost_group,
                background_surface, stars=stars, font_size=36
            )
            show_message(screen, clock, FPS, score, f"Level {current_level}", 2000,
                         spaceship_group, bullet_group, enemy_group,
                         enemy_bullet_group, boss_bullet_group, explosion_group, boost_group,
                         background_surface, stars=stars, blink_spaceship = True ,font_size=64)

            enemy_group = create_enemy_group(current_level)
            boss = None

    #Update sprites
    spaceship.update(screen, bullet_group, stars)
    for bullet in bullet_group:
        gained = bullet.update(enemy_group, boss_group, explosion_group, enemy_bullet_group)
        score += gained
    enemy_group.update()
    enemy_bullet_group.update(spaceship_group, explosion_group, spaceship)
    boss_bullet_group.update(spaceship_group, explosion_group, spaceship, bullet_group )
    explosion_group.update()
    boost_group.update(spaceship_group, stars)
    for boss_bullet in boss_bullet_group:
        boss_bullet.update(spaceship_group, explosion_group, spaceship, bullet_group)

    #Draw sprites
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    enemy_bullet_group.draw(screen)
    explosion_group.draw(screen)
    boost_group.draw(screen)
    boss_bullet_group.draw(screen)


    pygame.display.flip()

pygame.quit()

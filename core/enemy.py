import pygame
import random
import os

from settings import screen_width, screen_height, img_dir, boss_img
from core.explosion import Explosion


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, current_level):
        super().__init__()
        if current_level == 1:
            img_name = f"enemy{random.randint(1, 2)}.png"
            scale_factor = 2
        elif current_level == 2:
            img_name = f"enemy{random.randint(3, 4)}.png"
            scale_factor = 1.5
        else:
            img_name = f"enemy{random.randint(1, 2)}.png"
            scale_factor = 2


        self.image = pygame.image.load(os.path.join(img_dir, img_name)).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (self.image.get_width() * scale_factor, self.image.get_height() * scale_factor)
        )


        self.rect = self.image.get_rect(center=(x, y))
        self.move_counter = 0
        self.move_direction = 1
        self.move_delay = 3
        self.move_timer = 0

    def update(self):
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.rect.x += self.move_direction
            self.move_counter += 1
            self.move_timer = 0
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter = 0


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image):
        super().__init__()
        self.image = pygame.image.load(bullet_image).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (self.image.get_width() * 2,
             self.image.get_height() * 2)
        )
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, spaceship_group, explosion_group, spaceship):
        self.rect.y += 1
        if self.rect.top > screen_height:
            self.kill()
            return

        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, 1))
            spaceship.health_remaining -= 1

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, health = 500):
        super().__init__()
        self.image = pygame.image.load(boss_img)
        self.image = pygame.transform.scale(
            self.image,
            (self.image.get_width() * 4, self.image.get_width() * 4)
        )
        self.rect = self.image.get_rect(center=(x,y))

        #Movement
        self.speed = 1
        self.move_direction = 1
        #Health
        self.health = health
        self.max_health = health
        #change it when boss is defeated

    def update(self):
        self.rect.x += self.speed * self.move_direction
        if self.rect.right >= screen_width - 50:
            self.rect.right = screen_width - 50
            self.move_direction = -1
        elif self.rect.left <= 50:
            self.rect.left = 50
            self.move_direction = 1

    def is_dead(self):
        if self.health <= 0:
            return self.health <= 0
        return False


    def take_damage(self, amount):
        self.health -= amount

    def draw_boss_health_bar(self, screen):
        bar_width = 300
        bar_height = 20
        fill = int((self.health/self.max_health)*bar_width)
        outline_rect = pygame.Rect((screen_width//2)-(bar_width//2), 20, bar_width, bar_height)
        fill_rect = pygame.Rect((screen_width//2)-(bar_width//2), 20, fill, bar_height)
        health_rect = pygame.Rect((screen_width//2)-(bar_width//2), 20, bar_width*(self.health/self.max_health), bar_height)

        pygame.draw.rect(screen, (255, 0, 0),fill_rect)
        pygame.draw.rect(screen, (0,255,0), health_rect)
        pygame.draw.rect(screen, (255,255,255), outline_rect, 2)

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image):
        super().__init__()
        self.image = pygame.image.load(bullet_image).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (self.image.get_width() * 2,
             self.image.get_height() * 2)
        )
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, spaceship_group, explosion_group, spaceship, bullet_group):
        self.rect.y += 1
        if self.rect.top > screen_height:
            self.kill()
            return

        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, 1))
            spaceship.health_remaining -= 1
        if pygame.sprite.spritecollide(self, bullet_group, False):
            self.kill()
            explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, 1))



def create_enemy_group(current_level, rows=3, cols=5, x_offset=100, y_offset=100, x_spacing=100, y_spacing=70):
    enemy_group = pygame.sprite.Group()
    for row in range(rows):
        for col in range(cols):
            enemy = Enemy(x_offset + col * x_spacing, y_offset + row * y_spacing, current_level)
            enemy_group.add(enemy)
    return enemy_group



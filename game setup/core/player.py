import pygame
from settings import screen_width, red, green
from core.bullet import Bullet

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health, image, laser_sound):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        #health system
        self.health_start = health
        self.health_remaining = health
        #remove red bar when killed
        self.red_bar_remover = 1

        #shooting
        self.last_shot = pygame.time.get_ticks()
        self.laser_sound = laser_sound
        self.base_cooldown = 500
        self.boosted_cooldown = 250

    def update(self, screen, bullet_group, starfield):
        speed = 2

        if getattr(starfield, "boost_active", False):
            cooldown = self.boosted_cooldown
        else:
            cooldown = self.base_cooldown

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and time_now - self.last_shot > cooldown:
            self.laser_sound.play()
            bullet_group.add(Bullet(self.rect.centerx, self.rect.top))
            self.last_shot = time_now
        if self.health_remaining <= 0:
            from core.explosion import Explosion
            self.red_bar_remover = 0

        #Draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, self.rect.bottom + 10, self.rect.width, 15*self.red_bar_remover))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.bottom + 10,
                         int(self.rect.width * (self.health_remaining / self.health_start)), 15))

        if self.health_remaining <= 0:
            from core.explosion import Explosion
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            return explosion
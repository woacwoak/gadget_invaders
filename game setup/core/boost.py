import pygame
import random
import os
from settings import screen_height, booster_img

class Boost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(booster_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5,self.image.get_height()*2.5))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1

    def update(self, spaceship_group, starfield):
        self.rect.y += self.speed

        if self.rect.bottom > screen_height:
            self.kill()

        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            starfield.speed_multiplier = 3
            starfield.enemy_cooldown = 500
            starfield.boost_active = True
            starfield.boost_timer = pygame.time.get_ticks()
            self.kill()




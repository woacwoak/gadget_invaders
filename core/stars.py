import pygame
import random
from settings import screen_width, screen_height

class Star:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.size = random.randint(1, 2)
        self.speed = random.randint(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = 0
            self.x = random.randint(0, screen_width)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.size)

class StarField:
    def __init__(self, count=50):
        self.stars = []
        self.speed_multiplier = 1
        self.boost_timer = None
        self.boost_active = False
        self.enemy_cooldown = 1000

        for i in range(count):
            star = Star()
            self.stars.append(star)

    def update(self):
        for star in self.stars:
            star.y += star.speed * self.speed_multiplier
            if star.y > screen_height:
                star.y = 0
                star.x = random.randint(0, screen_width)

        if self.boost_timer:
            if pygame.time.get_ticks() - self.boost_timer > 3000:
                self.speed_multiplier = 1
                self.enemy_cooldown = 1000
                self.boost_active = False
                self.boost_timer = None

    def draw(self, surface):
        for star in self.stars:
            star.draw(surface)

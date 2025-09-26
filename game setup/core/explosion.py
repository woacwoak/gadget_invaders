import pygame
import os
from settings import img_dir

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.images = []
        self.load_images(size)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0
        self.explosion_speed = 3

    def load_images(self, size):
        for num in range(1, 6):
            img_path = os.path.join(img_dir, "Explosion Frames", f"exp{num}.png")
            img = pygame.image.load(img_path).convert_alpha()
            match size:
                case 1: #enemy bullet
                    img = pygame.transform.scale(img, (20, 20))
                case 2:  #enemy destroyed
                    img = pygame.transform.scale(img, (40, 40))
                case 3:  #player destroyed
                    img = pygame.transform.scale(img, (160, 160))
                case _:  #default size
                    img = pygame.transform.scale(img, (60, 60))

            self.images.append(img)

    def update(self):
        self.counter += 1
        if self.counter >= self.explosion_speed:
            self.counter = 0
            self.index += 1
            if self.index < len(self.images):
                self.image = self.images[self.index]
            else:
                self.kill()
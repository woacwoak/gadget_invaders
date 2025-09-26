import pygame
from core.explosion import Explosion
from core.enemy import Boss


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        from settings import bullet_img
        self.image = pygame.image.load(bullet_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2, self.image.get_height()*2))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, enemy_group, boss_group, explosion_group, enemy_bullet_group):
        self.rect.y -= 5
        points = 0

        if self.rect.bottom < 0:
            self.kill()

        hits_enemy = pygame.sprite.spritecollide(self, enemy_group, True)
        if hits_enemy:
            self.kill()
            points += len(hits_enemy)
            for hit in hits_enemy:
                explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, 2))

        hits_bullets = pygame.sprite.spritecollide(self, enemy_bullet_group, True)
        if hits_bullets:
            self.kill()
            for hit in hits_bullets:
                explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, 1))

        boss_hits = pygame.sprite.spritecollide(self, boss_group, False)  # returns one boss or None
        for boss in boss_hits:
            self.kill()
            explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, 1))
            boss.take_damage(20)

        return points


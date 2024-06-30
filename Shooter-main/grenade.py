import pygame
from explosion import Explosion  # Certifique-se de que a classe Explosion já tenha sido movida

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, grenade_img, settings):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
        self.settings = settings  # Pode incluir GRAVITY e outros parâmetros

    def update(self, screen_scroll, world_obstacle_list, explosion_group):
        self.vel_y += self.settings['GRAVITY']
        dx = self.direction * self.speed
        dy = self.vel_y

        # Verificação de colisão
        for tile in world_obstacle_list:
            # Colisão com paredes
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            # Colisão no eixo y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # Contagem regressiva
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)

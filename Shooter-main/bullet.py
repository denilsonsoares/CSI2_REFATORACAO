#bullet
import pygame
from settings import SCREEN_WIDTH
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img, sprite_groups):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.sprite_groups = sprite_groups  # Isso garante que sprite_groups seja uma propriedade da instância

    def update(self, player, world, screen_scroll):
        # Move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll

        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # Check for collision with level
        for tile in world.obstacle_list:  # Access obstacle_list through the world object
            if tile[1].colliderect(self.rect):
                self.kill()

        # Check collision with the player
        if pygame.sprite.collide_rect(self, player):
            if player.alive:
                player.health -= 5
                self.kill()

        # Check collision with each enemy
        for enemy in self.sprite_groups.enemy_group:
            if pygame.sprite.collide_rect(self, enemy):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()


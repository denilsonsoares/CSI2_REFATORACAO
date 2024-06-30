#bullet
import pygame
from settings import SCREEN_WIDTH
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, bullet_img, sprite_groups):
		pygame.sprite.Sprite.__init__(self)
        self.sprite_groups = sprite_groups
		self.speed = 10
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self, player, world, screen_scroll):
		#move bullet
		self.rect.x += (self.direction * self.speed) + screen_scroll
		#check if bullet has gone off screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()
		#check for collision with level
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect):
				self.kill()

		#check collision with characters
		if pygame.sprite.spritecollide(player, self.sprite_groups.bullet_group, False):
			if player.alive:
				player.health -= 5
				self.kill()
		for enemy in self.sprite_groups.enemy_group:
			if pygame.sprite.spritecollide(enemy, self.sprite_groups.bullet_group, False):
				if enemy.alive:
					enemy.health -= 25
					self.kill()

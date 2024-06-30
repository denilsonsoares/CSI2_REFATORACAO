import pygame
class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, screen, health):
        # Update with new health
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, 154, 24))  # Black border
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 150, 20))  # Red health bar
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 150 * ratio, 20))  # Green health fill

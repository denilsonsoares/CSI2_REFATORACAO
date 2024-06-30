import pygame
from settings import *

class GraphicsHandler:
    def __init__(self, screen):
        self.screen = screen

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_bg(self, sky_img, mountain_img, pine1_img, pine2_img, bg_scroll):
        self.screen.fill(BG)
        width = sky_img.get_width()
        for x in range(5):
            self.screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
            self.screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
            self.screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
            self.screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

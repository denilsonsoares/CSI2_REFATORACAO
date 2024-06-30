#resources.py
import pygame
from load_resources import load_resources

# Initialize Pygame mixer
pygame.mixer.init()

# Load all resources
resources = load_resources()

# Extract resources
jump_fx = resources['sounds']['jump_fx']
shot_fx = resources['sounds']['shot_fx']
grenade_fx = resources['sounds']['grenade_fx']

pygame.mixer.music.load = resources['music']['background_music']

start_img = resources['images']['buttons']['start']
exit_img = resources['images']['buttons']['exit']
restart_img = resources['images']['buttons']['restart']

sky_img = resources['images']['backgrounds']['sky']
mountain_img = resources['images']['backgrounds']['mountain']
pine1_img = resources['images']['backgrounds']['pine1']
pine2_img = resources['images']['backgrounds']['pine2']

img_list = resources['images']['tiles']
bullet_img = resources['images']['bullet']
grenade_img = resources['images']['grenade']
item_boxes = resources['images']['boxes']
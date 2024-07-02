#load_resources.py
import pygame
from settings import TILE_SIZE, TILE_TYPES

def load_resources():
    # Inicializa o mixer para poder carregar sons
    pygame.mixer.init()

    # Load music and sounds
    pygame.mixer.music.load('audio/music2.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0, 5000)
    jump_fx = pygame.mixer.Sound('audio/jump.wav')
    jump_fx.set_volume(0.05)
    shot_fx = pygame.mixer.Sound('audio/shot.wav')
    shot_fx.set_volume(0.05)
    grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
    grenade_fx.set_volume(0.05)

    # Load images
    # Button images
    start_img = pygame.image.load('img/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
    restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
    # Background
    pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
    pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
    mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
    sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
    # Store tiles in a list
    img_list = [pygame.image.load(f'img/Tile/{x}.png').convert_alpha() for x in range(TILE_TYPES)]
    img_list = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in img_list]
    # Bullet
    bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
    # Grenade
    grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
    # Pick up boxes
    health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
    ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
    grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
    item_boxes = {
        'Health': health_box_img,
        'Ammo': ammo_box_img,
        'Grenade': grenade_box_img
    }

    # Return a dictionary of all loaded resources
    return {
        "sounds": {
            "jump_fx": jump_fx,
            "shot_fx": shot_fx,
            "grenade_fx": grenade_fx
        },
        "music": {
            "background_music": pygame.mixer.music
        },
        "images": {
            "buttons": {
                "start": start_img,
                "exit": exit_img,
                "restart": restart_img
            },
            "backgrounds": {
                "pine1": pine1_img,
                "pine2": pine2_img,
                "mountain": mountain_img,
                "sky": sky_img
            },
            "tiles": img_list,
            "bullet": bullet_img,
            "grenade": grenade_img,
            "boxes": item_boxes
        }
    }

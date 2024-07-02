import pygame
from pygame import mixer
import csv
from settings import *

# Importações que não dependem do display de pygame inicializado
from screen_fade import ScreenFade
from sprite_groups import SpriteGroups
from graphics_handler import GraphicsHandler
import button

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# Após a inicialização do display, importe os recursos e módulos que dependem deles
from resources import *  # Importa imagens, sons, etc.

# Agora importe os módulos que podem precisar acessar recursos gráficos ou que dependem do display
from world import World
from grenade import Grenade

# Inicializações diversas
graphics_handler = GraphicsHandler(screen)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Futura', 30)
sprite_groups = SpriteGroups()

# Criação de elementos de UI que usam recursos gráficos
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World(sprite_groups)
player, health_bar = world.process_data(world_data, img_list, item_boxes, bullet_img, shot_fx)

run = True
while run:

    clock.tick(FPS)

    if start_game == False:
        # draw menu
        screen.fill(BG)
        # add buttons
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        # update background
        graphics_handler.draw_bg(sky_img, mountain_img, pine1_img, pine2_img, bg_scroll)
        # draw world map
        world.draw(screen, screen_scroll)
        # show player health
        health_bar.draw(screen, player.health)
        # show ammo
        graphics_handler.draw_text('AMMO: ', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        # show grenades
        graphics_handler.draw_text('GRENADES: ', font, WHITE, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))

        player.update()
        player.draw(screen)

        for enemy in sprite_groups.enemy_group:
            enemy.ai(player, screen_scroll, world, bg_scroll)
            enemy.draw(screen)
            enemy.update()
            


        # update and draw groups
        #update
        for bullet in sprite_groups.bullet_group:
            bullet.update(player, world, screen_scroll)
        for grenade in sprite_groups.grenade_group:
            grenade.update(screen_scroll, world.obstacle_list, sprite_groups.explosion_group, player, sprite_groups.enemy_group)
        for explosion in sprite_groups.explosion_group:
            explosion.update(screen_scroll)
        for item_box in sprite_groups.item_box_group:
            item_box.update(screen_scroll, player)
        for decoration in sprite_groups.decoration_group:
            decoration.update(screen_scroll)
        for water in sprite_groups.water_group:
            water.update(screen_scroll)
        for exit in sprite_groups.exit_group:
            exit.update(screen_scroll)
        #draw
        sprite_groups.bullet_group.draw(screen)
        sprite_groups.grenade_group.draw(screen)
        sprite_groups.explosion_group.draw(screen)
        sprite_groups.item_box_group.draw(screen)
        sprite_groups.decoration_group.draw(screen)
        sprite_groups.water_group.draw(screen)
        sprite_groups.water_group.draw(screen)
        sprite_groups.exit_group.draw(screen)

        # show intro
        if start_intro == True:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter = 0

        # update player actions
        if player.alive:
            # shoot bullets
            if shoot:
                player.shoot(bullet_img, shot_fx, sprite_groups)
            # throw grenades
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction, grenade_img, grenade_config)
                sprite_groups.grenade_group.add(grenade)
                # reduce grenades
                player.grenades -= 1
                grenade_thrown = True
            if player.in_air:
                player.update_action(2)  # 2: jump
            elif moving_left or moving_right:
                player.update_action(1)  # 1: run
            else:
                player.update_action(0)  # 0: idle
            screen_scroll, level_complete = player.move(moving_left, moving_right, screen_scroll, world, bg_scroll)
            bg_scroll -= screen_scroll
            # check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = sprite_groups.reset_level(16, 150)
                if level <= MAX_LEVELS:
                    # load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World(sprite_groups)
                    player, health_bar = world.process_data(world_data, img_list, item_boxes, bullet_img, shot_fx)
        else:
            screen_scroll = 0
            if death_fade.fade(screen):
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = sprite_groups.reset_level(16, 150)
                    # load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World(sprite_groups)
                    player, health_bar = world.process_data(world_data , img_list, item_boxes, bullet_img, shot_fx)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
                grenade_thrown = False
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = True

    pygame.display.update()

pygame.quit()
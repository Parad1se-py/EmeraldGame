# Copyright (c) 2022, Parad1se

# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pygame

from .settings import *
from .tiles import *
from .utils import *
from .enemy import *
from .decoration import *
from .player import *
from .particles import *


class Level:
    def __init__(self, level_data, surface, type):
        self.type = type

        # General setup of the level
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # Player data
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)

        # Dust
        self.dust_sprites = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # Terrain setup of the level
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # Grass setup of the level
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # Enemy
        orc_layout = import_csv_layout(level_data['enemies']['orc'])
        self.orc_sprites = self.create_tile_group(orc_layout, 'orc')

        # Constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

        # Decorations
        self.sky = Sky(13)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = CaveWater(screen_height - 20, level_width)
        self.clouds = Clouds(400, level_width, 20)

    # Crates setup of the level
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # Coins setup of the level
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val == '-1':
                    continue

                x = col_index * tile_size
                y = row_index * tile_size

                if type == 'terrain':
                    terrain_tile_list = import_cut_graphics(f'assets/graphics/blocks/{self.type}/terrain_tiles.png')
                    tile_surface = terrain_tile_list[int(val)]
                    sprite = StaticTile(tile_size, x, y, tile_surface)

                elif type == 'grass':
                    grass_tile_list = import_cut_graphics(f'assets/graphics/grass/{self.type}_grass/grass_tiles.png')
                    tile_surface = grass_tile_list[int(val)]
                    sprite = StaticTile(tile_size, x, y, tile_surface)

                elif type == 'crates':
                    sprite = Crate(tile_size, x, y)

                elif type == 'coins':
                    if val == '0': sprite = Coin(tile_size, x, y, 'assets/graphics/coins/gold')
                    if val == '1': sprite = Coin(tile_size, x, y, 'assets/graphics/coins/silver')

                elif type == 'orc':
                    sprite = Enemy(tile_size, x, y, 'orc')

                elif type == 'constraint':
                    sprite = Tile(tile_size, x, y)

                sprite_group.add(sprite)

        return sprite_group
        
    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
            
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprites.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                    
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
            
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()
        
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False
            
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
            
    def get_player_on_ground(self):
        self.player_on_ground = bool(self.player.sprite.on_ground)

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprites.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
                fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
                self.dust_sprites.add(fall_dust_particle)

    def setup_player(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                elif val == '1':
                    hat_surface = pygame.image.load('assets/graphics/character/hat.png')
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def sprite_updater(self):
        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # enemies
        self.orc_sprites.draw(self.display_surface)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.orc_sprites.update(self.world_shift)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()
        
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # water
        self.water.draw(self.display_surface, self.world_shift)

        # crate
        self.crate_sprites.draw(self.display_surface)
        self.crate_sprites.update(self.world_shift)

        # coins
        self.coin_sprites.draw(self.display_surface)
        self.coin_sprites.update(self.world_shift)

    def enemy_collision_reverse(self):
        for enemy in self.orc_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):
        # run the game

        self.sprite_updater()

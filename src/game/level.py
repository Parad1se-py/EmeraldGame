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


class Level:
    def __init__(self, level_data, surface, type):
        self.type = type

        # General setup of the level
        self.display_surface = surface
        self.world_shift = 0

        # Terrain setup of the level
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # Grass setup of the level
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

    """        # Crates setup of the level
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # Coins setup of the level
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')"""

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
                    sprite = AnimatedTile(tile_size, x, y, 'assets/graphics/coins/coin_tiles.png')

                sprite_group.add(sprite)


        return sprite_group

    def sprite_updater(self):
        # terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

    def run(self):
        # run the game

        self.sprite_updater()

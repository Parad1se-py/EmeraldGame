# Copyright (c) 2022, Parad1se

# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from random import choice, randint
import pygame


from .settings import *
from .tiles import AnimatedTile, StaticTile
from .utils import *


class Sky:
    def __init__(self, horizon):
        self.horizon = horizon
        self.top = pygame.image.load('assets/graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('assets/graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('assets/graphics/decoration/sky/sky_middle.png').convert()

        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(verticle_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

class Water:
    def __init__(self, top, level_width, path):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amt = int((level_width + screen_width) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amt):
            x = tile * water_tile_width + water_start
            y = top
            self.water_sprites.add(AnimatedTile(192, x, y, path))

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)

class CaveWater(Water):
    def __init__(self, top, level_width):
        super().__init__(top, level_width, 'assets/graphics/decoration/water/cave')

class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder('assets/graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            self.cloud_sprites.add(StaticTile(0, x, y, cloud))

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)

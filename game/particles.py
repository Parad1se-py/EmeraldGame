# Copyright (c) 2022, Parad1se

# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pygame
from .utils import *


class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self, pos, type):
		super().__init__()
		self.frame_index = 0
		self.animation_speed = 0.5
		if type == 'jump':
			self.frames = import_folder('assets/graphics/character/dust_particles/jump')
		elif type == 'land':
			self.frames = import_folder('assets/graphics/character/dust_particles/land')
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center=pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift

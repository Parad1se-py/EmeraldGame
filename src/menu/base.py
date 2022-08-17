import sys

import pygame
from game import *
from game_data import *

from .menu import *

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = 'assets/font/8-BIT WONDER.TTF'
        self.BLACK, self.WHITE, self.EMERALD_GREEN = (0, 0, 0), (255, 255, 255), (80, 200, 120)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            pygame.display.set_caption("EmeraldRPG")
            clock = pygame.time.Clock()
            level = Level(level_0, screen)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                screen.fill('black')
                level.run()

                pygame.display.update()
                clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key in [pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.Font(self.font_name,size)
        # font = pygame.font.SysFont('Verdana', size)
        text_surface = font.render(text, True, self.EMERALD_GREEN)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
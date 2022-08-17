from menu.base import *

EmeraldRPG = Game()

while EmeraldRPG.running:
    EmeraldRPG.curr_menu.display_menu()
    EmeraldRPG.game_loop()

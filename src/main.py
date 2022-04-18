from base import Game

EmeraldRPG = Game()

while EmeraldRPG.running:
    EmeraldRPG.curr_menu.display_menu()
    EmeraldRPG.game_loop()
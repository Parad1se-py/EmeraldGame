from base import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
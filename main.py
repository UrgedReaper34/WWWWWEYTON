# Import statements

from game import Game
import interface


if __name__ == "__main__":
    game = Game()
    game.start()
    while not game.win() and not game.lose():

        x = 'invalid'
        while x == 'invalid':
            game.show_status()
            options = game.get_options()
            choice = game.prompt_player(''.join(options))
            x = game.enter(choice)
            if x == 'invalid':
                interface.clear()
        interface.clear()
    game.show_status()
    interface.pause()
    interface.clear()

    if game.win():
        print("You have slained the BigBoss, you win")
    else:
        print("You died, restart as you are unworthy")

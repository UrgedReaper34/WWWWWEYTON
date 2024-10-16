# Import statements

from game import Game
import interface


if __name__ == "__main__":
    game = Game()
    game.start()
    while not game.win() and not game.lose():

        done = False
        while not done:
            game.show_status()
            choice = interface.prompt_player_choice(game.get_options())
            done = game.enter(choice)
            if done:
                interface.clear()
    game.show_status()
    interface.medium_pause()
    interface.clear()

    if game.win():
        print("You have slained the BigBoss, you win")
    else:
        print("You died, restart as you are unworthy")

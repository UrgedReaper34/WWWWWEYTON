from game import Game


def test_1():
    game = Game()
    here = game.get_player_position()
    game.move("D")
    game.move("A")
    assert game.get_player_position() == here


def test_2():
    pass


if __name__ == "__main__":
    test_1()

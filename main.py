import arcade
from game_window import MyGame
from constants import SCREEN_TITLE


def main():
    window = MyGame(SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

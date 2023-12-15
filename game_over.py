# game_over.py
import arcade


class GameOverScreen:
    def __init__(self, game_window):
        self.game_window = game_window
        self.game_over_scroll_y = self.game_window.height
        self.game_over_scroll_speed = 0.5
        self.player_name = ""
        self.is_high_score = False
        self.load_credits_text()

    def load_credits_text(self):
        with open("credits.txt", "r") as file:
            self.credits_text = file.read()

    def draw(self):
        # Draw the background
        arcade.draw_lrwh_rectangle_textured(0, 0, self.game_window.width, self.game_window.height, self.game_window.background)

        # Draw the sun sprite
        sun_center_x = self.game_window.width / 2
        sun_center_y = self.game_window.height / 2
        sun_sprite = arcade.Sprite("assets/images/SunSprite.png", center_x=sun_center_x, center_y=sun_center_y)
        sun_sprite.draw()

        # Draw scrolling text
        self.draw_scrolling_text()

        # Draw "Exit" button
        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14, font_name="Kenney Blocks")

    def draw_scrolling_text(self):
        start_y = self.game_over_scroll_y
        # font_size = 40
        # font_name = "Kenney Mini Square"

        # Draw credits
        for line in self.credits_text.split('\n'):
            arcade.draw_text(line, self.game_window.width / 2, start_y + 900, arcade.color.WHITE, font_size=40, anchor_x="center",
                             font_name="Kenney Mini Square")

        # High scores and input box if high score achieved
        if self.is_high_score:
            arcade.draw_text(self.player_name, self.game_window.width / 2, start_y + 400,
                             arcade.color.WHITE, font_size=40, anchor_x="center", font_name="Kenney Mini Square")
            arcade.draw_text(f"Congratulations! \n You scored: {self.game_window.current_score} \n Enter Name:",
                             self.game_window.width / 2, start_y + 300,
                             arcade.color.WHITE, font_size=40, anchor_x="center", font_name="Kenney Mini Square")

        # Draw "GAME OVER" text
        arcade.draw_text("GAME OVER", self.game_window.width / 2, start_y, arcade.color.WHITE, 100,
                         anchor_x="center",
                         font_name="Kenney Blocks")

        # start_y -= 150

    def update(self, delta_time):
        # Update the y-coordinate for scrolling
        self.game_over_scroll_y -= self.game_over_scroll_speed

        # Check and handle high score input
        self.check_high_score()

    def check_high_score(self):
        if self.game_window.scoring.is_high_score(self.game_window.current_score):
            self.is_high_score = True
        else:
            self.is_high_score = False
            # self.game_window.game_state = "WELCOME"

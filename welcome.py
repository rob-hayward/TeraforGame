# welcome.py
import arcade

class WelcomeScreen:
    def __init__(self, game_window):
        self.game_window = game_window
        self.scroll_text_y = self.game_window.height * 2.8
        self.load_scrolling_text()

    def load_scrolling_text(self):
        with open("scrolling_text.txt", "r") as file:
            self.scroll_text = file.read()

    def draw(self):
        # Draw the background
        arcade.draw_lrwh_rectangle_textured(0, 0, self.game_window.width, self.game_window.height, self.game_window.background)

        # Split the text into lines and draw
        lines = self.scroll_text.split('\n')
        line_height = 20  # Adjust as needed for spacing between lines
        start_y = self.scroll_text_y + 200

        for line in lines:
            if "TERAFOR" in line:
                # Draw the main title with a larger font
                arcade.draw_text(line, self.game_window.width / 2, start_y, arcade.color.YELLOW, 150, anchor_x="center",
                                 font_name="Kenney Blocks")
            else:
                # Draw other lines with the regular font and size
                arcade.draw_text(line, self.game_window.width / 2, start_y, arcade.color.YELLOW, 30, anchor_x="center",
                                 font_name="Kenney Mini Square")
            start_y -= line_height  # Move down for the next line

        # Draw the exit button
        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14, font_name="Kenney Blocks")

    def update(self, delta_time):
        # Scroll the text upwards
        self.scroll_text_y -= 0.5
        if self.scroll_text_y < -self.game_window.height / 2:
            self.scroll_text_y = self.game_window.height

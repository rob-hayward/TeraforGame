# game_window.py
import arcade
import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SUN_SIZE, ORBIT_RADIUS, PARTICLE_EMISSION_MIN_TIME, \
    PARTICLE_EMISSION_MAX_TIME
from square_building import group_particles_by_type, find_3x3_squares
from sun import Sun
from particles import *
from collision_handling import detect_collision, handle_collision, stationary_particles, moving_particles
from scoring import Scoring


class MyGame(arcade.Window):
    def __init__(self, title):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title, fullscreen=True)
        self.game_state = "WELCOME"
        self.paused = False
        self.sun = None
        self.light_grey_particle = None
        self.particle_timer = 0
        self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)
        self.particles = arcade.SpriteList()
        self.background = None
        self.scroll_text_y = SCREEN_HEIGHT * 2.8
        self.load_scrolling_text()
        self.player_name = ""
        self.is_high_score = False
        self.scoring = Scoring("high_score.txt")
        self.current_score = 0

    def load_scrolling_text(self):
        with open("scrolling_text.txt", "r") as file:
            self.scroll_text = file.read()

    def draw_high_scores(self, start_y):
        top_scores = self.scoring.get_top_high_scores()

        for rank, (name, score) in enumerate(top_scores, start=1):
            text = f"{rank}. {name}: {score}"
            arcade.draw_text(text, SCREEN_WIDTH / 2, start_y, arcade.color.WHITE,
                             font_size=40, font_name="Kenney Mini Square", anchor_x="center")
            start_y -= 60  # Adjust the spacing between lines if needed

    def game_over(self):
        self.current_score = sum(particle.gravitational_value for particle in stationary_particles)
        if self.scoring.is_high_score(self.current_score):
            self.is_high_score = True
            self.game_state = "GAME_OVER"
            print(f"High Score Achieved: {self.current_score}")
        else:
            self.game_state = "WELCOME"  # Or another state as needed
        print(f"Current Score: {self.current_score}")

    # move to scoring.py
    def save_high_scores(self, high_scores):
        with open("high_score.txt", "w") as file:
            for name, score in high_scores:
                file.write(f"{name},{score}\n")

    def setup(self):
        self.background = arcade.load_texture("assets/galaxy_background.png")
        self.sun = Sun("assets/SunSprite.png", scale=1.05,
                       orbit_radius=ORBIT_RADIUS,
                       orbit_speed=ORBIT_SPEED)
        self.light_grey_particle = LightGreyParticle()
        self.light_grey_particle.center_x = SCREEN_WIDTH / 2
        self.light_grey_particle.center_y = SCREEN_HEIGHT / 2
        # self.light_grey_particle.center_x = SCREEN_WIDTH # for testing game over
        # self.light_grey_particle.center_y = SCREEN_HEIGHT # for testing game over
        self.light_grey_particle.speed = 0
        self.particles.append(self.light_grey_particle)

        # Add the light grey particle to the stationary_particles set
        stationary_particles.add(self.light_grey_particle)

    def on_draw(self):
        arcade.start_render()
        if self.game_state == "WELCOME":
            self.draw_welcome_screen()
        elif self.game_state == "GAME":
            self.draw_game_screen()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()

    def draw_welcome_screen(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Split the text into lines
        lines = self.scroll_text.split('\n')
        line_height = 20  # Adjust as needed for spacing between lines
        start_y = self.scroll_text_y + 200

        for line in lines:
            if "TERAFOR" in line:  # Check if the line is the game name
                # Draw "TERAFOR" with a specific font and larger size
                arcade.draw_text(line, SCREEN_WIDTH / 2, start_y, arcade.color.YELLOW, 150, anchor_x="center",
                                 font_name="Kenney Blocks")
            else:
                # Draw other lines with the regular font and size
                arcade.draw_text(line, SCREEN_WIDTH / 2, start_y, arcade.color.YELLOW, 30, anchor_x="center",
                                 font_name="Kenney Mini Square")
            start_y -= line_height  # Move down for the next line

        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14, font_name="Kenney Blocks")

    def draw_game_screen(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.sun.draw()
        for particle in self.particles:
            particle.draw()

        # Get the top high score from scoring object
        top_high_score = self.scoring.get_top_high_scores(1)
        if top_high_score:
            high_score_name, high_score = top_high_score[0]
        else:
            high_score_name, high_score = ("", 0)

        # Display the high score in the top left corner
        high_score_text = f"High Score {high_score_name} - {high_score}"
        arcade.draw_text(high_score_text, 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14, font_name="Kenney Blocks")

        # Update and display the current score in the top right corner
        self.current_score = sum(particle.gravitational_value for particle in stationary_particles)
        current_score_text = f"Current Score {self.current_score}"
        arcade.draw_text(current_score_text, SCREEN_WIDTH - 400, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14,
                         font_name="Kenney Blocks")

        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14, font_name="Kenney Blocks")

    def draw_game_over_screen(self):
        # Draw the background
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw the sun sprite in the center
        sun_center_x = SCREEN_WIDTH / 2
        sun_center_y = SCREEN_HEIGHT / 2
        sun_sprite = arcade.Sprite("assets/SunSprite.png", center_x=sun_center_x, center_y=sun_center_y)
        sun_sprite.draw()

        # Draw the high scores on top of the sun sprite
        start_y_for_high_scores = sun_center_y + 80  # Adjust as needed
        self.draw_high_scores(start_y_for_high_scores)

        # Draw "Press ESC to exit" text
        arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, 800, arcade.color.WHITE, 90, anchor_x="center",
                         font_name="Kenney Blocks")

        # Draw "Exit" button
        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14, font_name="Kenney Blocks")

        if self.is_high_score:
            # Draw text input box higher up the page
            text_input_y_position = self.height // 2 + 200  # Adjust Y-coordinate to move higher
            arcade.draw_text("Congratulations! Enter Name:", self.width // 2, text_input_y_position,
                             arcade.color.WHITE, 40, font_name="Kenney Blocks", anchor_x="center")
            arcade.draw_text(self.player_name, self.width // 2, text_input_y_position - 60,
                             arcade.color.WHITE, 40, font_name="Kenney Mini Square", anchor_x="center")

    def update(self, delta_time):
        if self.game_state == "WELCOME":
            self.update_welcome_screen(delta_time)
        elif self.game_state == "GAME":
            self.update_game_screen(delta_time)

    def update_welcome_screen(self, delta_time):
        self.scroll_text_y -= 0.5  # Scroll the text upwards
        if self.scroll_text_y < -SCREEN_HEIGHT / 2:
            self.scroll_text_y = SCREEN_HEIGHT

    def update_game_screen(self, delta_time):
        if not self.paused:
            # Proceed with updating only if the game is not paused
            self.sun.update()
            self.light_grey_particle.update()

            # Emit new particles and update positions
            self.particle_timer += delta_time
            if self.particle_timer >= self.next_particle_time:
                self.particle_timer = 0
                self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)
                new_particle = self.sun.emit_particle()
                self.particles.append(new_particle)

            # Update particle positions and handle collisions
            detect_collision(self.particles, delta_time, self.sun)

            self.current_score = sum(particle.gravitational_value for particle in stationary_particles)

            groups = group_particles_by_type(stationary_particles)
            find_3x3_squares(groups, stationary_particles, self.particles)

            # Check for game over condition
            for particle in stationary_particles:
                if arcade.check_for_collision(particle, self.sun):
                    self.game_over()  # Handle game over
                    return

    def on_key_press(self, key, modifiers):
        if self.is_high_score:
            if key == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif key == arcade.key.ENTER and self.player_name:
                self.scoring.update_high_scores(self.player_name, self.current_score)
                self.is_high_score = False
                self.game_state = "WELCOME"  # Or another state as needed
            elif 97 <= key <= 122:  # ASCII values for lowercase letters
                if len(self.player_name) < 20:  # Limit name length
                    self.player_name += chr(key).upper()
            return

        if self.game_state in ["WELCOME", "GAME_OVER"]:
            # If the game is in the WELCOME or GAME_OVER state, pressing ESCAPE will close the game
            if key == arcade.key.ESCAPE:
                self.close()
                return

        elif self.game_state == "GAME":
            # If the game is in progress and ESCAPE is pressed, trigger game over
            if key == arcade.key.ESCAPE:
                self.game_over()  # Call the game_over method
                self.game_state = "GAME_OVER"
                return

        if self.game_state == "WELCOME":
            if key == arcade.key.SPACE:
                self.game_state = "GAME"
                return

        elif self.game_state == "GAME":
            # Define movement angles
            move_up_angle = 90
            move_down_angle = 270
            move_right_angle = 0
            move_left_angle = 180

            # Iterate over moving particles and change direction based on key press
            for particle in moving_particles:
                if isinstance(particle, PositiveParticle):
                    if key == arcade.key.W:
                        particle.angle = move_down_angle
                    elif key == arcade.key.S:
                        particle.angle = move_up_angle
                    elif key == arcade.key.A:
                        particle.angle = move_right_angle
                    elif key == arcade.key.D:
                        particle.angle = move_left_angle

                elif isinstance(particle, NegativeParticle):
                    if key == arcade.key.W:
                        particle.angle = move_up_angle
                    elif key == arcade.key.S:
                        particle.angle = move_down_angle
                    elif key == arcade.key.A:
                        particle.angle = move_left_angle
                    elif key == arcade.key.D:
                        particle.angle = move_right_angle

                elif isinstance(particle, LightGreyParticle):
                    if key == arcade.key.UP:
                        particle.angle = move_up_angle
                    elif key == arcade.key.DOWN:
                        particle.angle = move_down_angle
                    elif key == arcade.key.LEFT:
                        particle.angle = move_left_angle
                    elif key == arcade.key.RIGHT:
                        particle.angle = move_right_angle

            if key == arcade.key.RETURN:
                self.sun.reverse_orbit_direction()

            # Toggle pause state only when in GAME state
            if key == arcade.key.P:
                self.paused = not self.paused

        super().on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        super().on_key_release(key, modifiers)

        # Set angles of moving particles towards the center on key release
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D, arcade.key.UP, arcade.key.DOWN,
                   arcade.key.LEFT, arcade.key.RIGHT]:
            center_x = SCREEN_WIDTH / 2
            center_y = SCREEN_HEIGHT / 2
            for particle in moving_particles:
                if isinstance(particle, (PositiveParticle, NegativeParticle, LightGreyParticle)):
                    particle.angle = particle.angle_towards_center(center_x, center_y)

    def on_mouse_press(self, x, y, button, modifiers):
        if 0 <= x <= 100 and 0 <= y <= 20:  # Specific area for exit
            self.close()

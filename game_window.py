# game_window.py
import time

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
        self.load_credits_text()
        self.game_over_scroll_y = SCREEN_HEIGHT * 1.5
        self.game_over_scroll_speed = 0.5
        self.player_name = ""
        self.is_high_score = False
        self.scoring = Scoring("high_score.txt")
        self.current_score = 0
        self.background_noise = arcade.load_sound("assets/sounds/background_noise.wav")
        self.background_noise_playing = False
        self.background_noise_player = None  # To store the media player for background noise
        self.background_noise_volume = 0.2
        # Load music tracks
        self.track1 = arcade.load_sound("assets/sounds/Billy's Sacrifice.wav")
        self.track2 = arcade.load_sound("assets/sounds/Checking Manifest.wav")

        # Track duration in seconds (you need to set these manually)
        self.track1_duration = 234  # Example duration in seconds
        self.track2_duration = 240  # Example duration in seconds

        # Track which song is currently playing and when it started
        self.current_track = None
        self.track_start_time = None

    def play_next_track(self):
        """
        Play the next track in the playlist.
        """
        now = time.time()
        if self.current_track == 1 and (now - self.track_start_time) > self.track1_duration:
            arcade.play_sound(self.track2, looping=False)
            self.current_track = 2
            self.track_start_time = now
        elif self.current_track == 2 and (now - self.track_start_time) > self.track2_duration:
            arcade.play_sound(self.track1, looping=False)
            self.current_track = 1
            self.track_start_time = now
        elif self.current_track is None:
            # If no track has been played yet
            arcade.play_sound(self.track1, looping=False)
            self.current_track = 1
            self.track_start_time = now

    def load_scrolling_text(self):
        with open("scrolling_text.txt", "r") as file:
            self.scroll_text = file.read()

    def load_credits_text(self):
        with open("credits.txt", "r") as file:
            self.credits_text = file.read()

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
            self.game_over_scroll_y = SCREEN_HEIGHT * 1.5  # Reset scroll position
        else:
            self.game_state = "WELCOME"  # Or another state as needed

    def save_high_scores(self, high_scores):
        with open("high_score.txt", "w") as file:
            for name, score in high_scores:
                file.write(f"{name},{score}\n")

    def setup(self):
        self.background = arcade.load_texture("assets/images/galaxy_background.png")
        self.sun = Sun("assets/images/SunSprite.png", scale=1.05,
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
            if not self.background_noise_playing:
                self.background_noise_player = arcade.play_sound(self.background_noise, looping=True,
                                                                 volume=self.background_noise_volume)
                self.background_noise_playing = True
            self.draw_welcome_screen()
        elif self.game_state == "GAME":
            if self.background_noise_playing:
                arcade.stop_sound(self.background_noise_player)
                self.background_noise_playing = False
            self.draw_game_screen()
        elif self.game_state == "GAME_OVER":
            if not self.background_noise_playing:
                self.background_noise_player = arcade.play_sound(self.background_noise, looping=True,
                                                                 volume=self.background_noise_volume)
                self.background_noise_playing = True
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
        high_score_text = f"High Score: {high_score_name} - {high_score}"
        arcade.draw_text(high_score_text, 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14, font_name="Kenney Blocks")

        # Update and display the current score in the top right corner
        self.current_score = sum(particle.gravitational_value for particle in stationary_particles)
        current_score_text = f"Current Score {self.current_score}"
        arcade.draw_text(current_score_text, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14,
                         font_name="Kenney Blocks")

        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14, font_name="Kenney Blocks")

    def draw_game_over_screen(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.draw_sun_sprite()  # Draw the sun sprite
        self.draw_scrolling_game_over_text()
        self.draw_exit_button()  # Draw the "Exit" button

    def draw_sun_sprite(self):
        sun_center_x = SCREEN_WIDTH / 2
        sun_center_y = SCREEN_HEIGHT / 2
        sun_sprite = arcade.Sprite("assets/images/SunSprite.png", center_x=sun_center_x, center_y=sun_center_y)
        sun_sprite.draw()

    def draw_exit_button(self):
        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14, font_name="Kenney Blocks")


    def draw_scrolling_game_over_text(self):
        start_y = self.game_over_scroll_y
        font_size = 40  # Adjust font size as needed
        font_name = "Kenney Mini Square"  # Set the desired font

        # Draw credits
        for line in self.credits_text.split('\n'):
            arcade.draw_text(line, SCREEN_WIDTH / 2, start_y + 1300, arcade.color.WHITE, font_size, anchor_x="center",
                             font_name=font_name)
            start_y -= 50  # Adjust spacing between lines of credits

        # Draw "Title" text
        arcade.draw_text("TERAFOR", SCREEN_WIDTH / 2, start_y + 900, arcade.color.WHITE, 100, anchor_x="center",
                         font_name="Kenney Blocks")
        start_y -= 150  # Adjust the spacing for the next section

        # Draw high scores
        top_scores = self.scoring.get_top_high_scores()
        for rank, (name, score) in enumerate(top_scores, start=1):
            text = f"{rank}. {name}: {score}"
            arcade.draw_text(text, SCREEN_WIDTH / 2, start_y + 500, arcade.color.WHITE, font_size, anchor_x="center",
                             font_name=font_name)
            start_y -= 70  # Adjust the spacing between lines

        # Draw input box if high score achieved
        if self.is_high_score:
            arcade.draw_text(self.player_name, SCREEN_WIDTH / 2, start_y + 400,
                             arcade.color.WHITE, font_size, anchor_x="center", font_name=font_name)
            arcade.draw_text(f"Congratulations! You scored: {self.current_score}! Enter Name:", SCREEN_WIDTH / 2, start_y + 300,
                             arcade.color.WHITE, font_size, anchor_x="center", font_name=font_name)
            start_y -= 100  # Adjust spacing for high scores

        # Draw "GAME OVER" text
        arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, start_y + 100, arcade.color.WHITE, 100, anchor_x="center",
                         font_name="Kenney Blocks")
        start_y -= 150  # Adjust the spacing for the next section

        # Update the y-coordinate for scrolling
        self.game_over_scroll_y -= self.game_over_scroll_speed

    def update(self, delta_time):
        if self.game_state == "WELCOME":
            self.update_welcome_screen(delta_time)
        elif self.game_state == "GAME":
            self.update_game_screen(delta_time)
            self.play_next_track()

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

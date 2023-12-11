# game_window.py
import arcade
import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SUN_SIZE, ORBIT_RADIUS, PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME
from square_building import group_particles_by_type, find_3x3_squares
from sun import Sun
from particles import *
from collision_handling import detect_collision, handle_collision, stationary_particles, moving_particles


class MyGame(arcade.Window):
    def __init__(self, title):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title, fullscreen=True)
        self.game_state = "WELCOME"  # New game state attribute
        self.paused = False
        self.sun = None
        self.light_grey_particle = None
        self.particle_timer = 0
        self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)
        self.particles = arcade.SpriteList()
        self.background = None
        self.high_score = 0
        self.high_score_name = ""
        self.load_high_score()  # Load the high score at initialization
        self.scroll_text_y = -SCREEN_HEIGHT  # Start position for scrolling text
        self.scroll_text = "Welcome to the Game! [Scrolling Introduction Text Here. Lets test it because I did not see it before.]"

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                name, score = file.read().split(',')
                self.high_score = int(score)
                self.high_score_name = name
        except FileNotFoundError:
            self.high_score = 0
            self.high_score_name = ""

    def save_high_score(self, name, score):
        with open("high_score.txt", "w") as file:
            file.write(f"{name},{score}")

    def update_score(self):
        # Calculate the current score
        self.current_score = sum(particle.gravitational_value for particle in stationary_particles)

    def setup(self):
        self.background = arcade.load_texture("assets/galaxy_background.png")
        self.sun = Sun("assets/SunSprite.png", scale=1.05,
                       orbit_radius=ORBIT_RADIUS,
                       orbit_speed=ORBIT_SPEED)

        # Calculate starting positions for the 3x3 square
        start_x = SCREEN_WIDTH / 2 - 20  # Leftmost particle's center
        start_y = SCREEN_HEIGHT / 2 - 20  # Topmost particle's center

        self.light_grey_particle = LightGreyParticle()
        self.light_grey_particle.center_x = SCREEN_WIDTH / 2
        self.light_grey_particle.center_y = SCREEN_HEIGHT / 2
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

    def draw_welcome_screen(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Press 'Space' to Launch", SCREEN_WIDTH / 2, 50, arcade.color.WHITE, 24,
                         anchor_x="center")
        arcade.draw_text(self.scroll_text, SCREEN_WIDTH / 2, self.scroll_text_y, arcade.color.YELLOW, 18,
                         anchor_x="center")

    def draw_game_screen(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.sun.draw()
        for particle in self.particles:
            particle.draw()

        # Display the high score in the top left corner
        high_score_text = f"High Score: {self.high_score_name} - {self.high_score}"
        arcade.draw_text(high_score_text, 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)

        # Update the current score
        self.update_score()  # Make sure the current score is updated

        # Display the current score in the top right corner
        current_score_text = f"Current Score: {self.current_score}"
        arcade.draw_text(current_score_text, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)

        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14)

    def update(self, delta_time):
        if self.game_state == "WELCOME":
            self.update_welcome_screen(delta_time)
        elif self.game_state == "GAME":
            self.update_game_screen(delta_time)

    def update_welcome_screen(self, delta_time):
        self.scroll_text_y += 1  # Adjust speed as needed
        if self.scroll_text_y > SCREEN_HEIGHT:
            self.scroll_text_y = -SCREEN_HEIGHT  # Reset scrolling

    def update_game_screen(self, delta_time):
        if not self.paused:
            # Proceed with updating only if the game is not paused
            self.sun.update()
            # self.light_grey_particle.update()

            # Emit new particles and update positions
            self.particle_timer += delta_time
            if self.particle_timer >= self.next_particle_time:
                self.particle_timer = 0
                self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)
                new_particle = self.sun.emit_particle()
                self.particles.append(new_particle)

            # Update particle positions and handle collisions
            detect_collision(self.particles, delta_time, self.sun)

            groups = group_particles_by_type(stationary_particles)
            find_3x3_squares(groups, stationary_particles, self.particles)

    def on_key_press(self, key, modifiers):
        if self.game_state == "WELCOME":
            if key == arcade.key.SPACE:
                self.game_state = "GAME"
                return  # Return early to avoid processing further key events

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

            # Control for light grey particles
            if key == arcade.key.UP:
                for particle in moving_particles:
                    if isinstance(particle, LightGreyParticle) and particle.speed < 5.0:
                        particle.speed += 0.1  # Increase speed, up to a maximum of 5.0
            elif key == arcade.key.DOWN:
                for particle in moving_particles:
                    if isinstance(particle, LightGreyParticle) and particle.speed > 0.5:
                        particle.speed -= 0.1  # Decrease speed, but not below 0.1

            # Reverse orbit direction logic
            if key == arcade.key.RIGHT:
                if self.sun.orbit_speed > 0:  # Currently moving clockwise
                    self.sun.reverse_orbit_direction()
            elif key == arcade.key.LEFT:
                if self.sun.orbit_speed < 0:  # Currently moving anticlockwise
                    self.sun.reverse_orbit_direction()

            # Toggle pause state only when in GAME state
            if key == arcade.key.SPACE:
                self.paused = not self.paused

        if key == arcade.key.ESCAPE:
            self.close()

        super().on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        super().on_key_release(key, modifiers)

        # Set angles of moving particles towards the center on key release
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            center_x = SCREEN_WIDTH / 2
            center_y = SCREEN_HEIGHT / 2
            for particle in moving_particles:
                if isinstance(particle, (PositiveParticle, NegativeParticle)):
                    particle.angle = particle.angle_towards_center(center_x, center_y)

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if the exit text is clicked
        if 0 <= x <= 100 and 0 <= y <= 20:
            self.close()

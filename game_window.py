# game_window.py
import arcade
import random
import time
from square_building import group_particles_by_type, find_3x3_squares
from sun import Sun
from particles import *
from collision_handling import detect_collision, stationary_particles, moving_particles
from scoring import Scoring
from sound_track import SoundTrack
from welcome import WelcomeScreen
from game_over import GameOverScreen

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
        self.background = arcade.load_texture("assets/images/galaxy_background.png")
        self.scoring = Scoring("high_score.txt")
        self.current_score = 0
        self.sound_track = SoundTrack()

        # Initialize the different screens
        self.welcome_screen = WelcomeScreen(self)
        self.game_over_screen = GameOverScreen(self)

    def setup(self):
        self.sun = Sun("assets/images/SunSprite.png", scale=1.05,
                       orbit_radius=ORBIT_RADIUS, orbit_speed=ORBIT_SPEED)
        self.light_grey_particle = LightGreyParticle()
        self.light_grey_particle.center_x = SCREEN_WIDTH / 2
        self.light_grey_particle.center_y = SCREEN_HEIGHT / 2
        self.light_grey_particle.speed = 0
        self.particles.append(self.light_grey_particle)
        stationary_particles.add(self.light_grey_particle)

    def on_draw(self):
        arcade.start_render()
        if self.game_state == "WELCOME":
            self.sound_track.play_background_noise()
            self.welcome_screen.draw()
        elif self.game_state == "GAME":
            self.sound_track.stop_background_noise()
            self.draw_game_screen()
        elif self.game_state == "GAME_OVER":
            self.sound_track.play_background_noise()
            self.game_over_screen.draw()

    def draw_game_screen(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.sun.draw()
        for particle in self.particles:
            particle.draw()

        # Display the high score and current score
        top_high_score = self.scoring.get_top_high_scores(1)
        high_score_name, high_score = top_high_score[0] if top_high_score else ("", 0)
        arcade.draw_text(f"High Score: {high_score_name} - {high_score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14, font_name="Kenney Blocks")
        self.current_score = sum(particle.gravitational_value for particle in stationary_particles)
        arcade.draw_text(f"Current Score: {self.current_score}", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14, font_name="Kenney Blocks")
        arcade.draw_text("Exit", 10, 10, arcade.color.WHITE, 14, font_name="Kenney Blocks")

    def update(self, delta_time):
        if self.game_state == "WELCOME":
            self.welcome_screen.update(delta_time)
        elif self.game_state == "GAME":
            now = time.time()
            self.sound_track.play_next_track(now)
            self.update_game_screen(delta_time)
        elif self.game_state == "GAME_OVER":
            self.game_over_screen.update(delta_time)

    def update_game_screen(self, delta_time):
        if not self.paused:
            self.sun.update()
            self.light_grey_particle.update()
            self.particle_timer += delta_time
            if self.particle_timer >= self.next_particle_time:
                self.particle_timer = 0
                self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)
                new_particle = self.sun.emit_particle()
                self.particles.append(new_particle)
            detect_collision(self.particles, delta_time, self.sun)
            groups = group_particles_by_type(stationary_particles)
            find_3x3_squares(groups, stationary_particles, self.particles)
            for particle in stationary_particles:
                if arcade.check_for_collision(particle, self.sun):
                    self.game_over()

    def game_over(self):
        self.current_score = sum(particle.gravitational_value for particle in stationary_particles)
        if self.scoring.is_high_score(self.current_score):
            self.game_over_screen.is_high_score = True
            self.game_over_screen.player_name = ""
        self.game_state = "GAME_OVER"

    def on_key_press(self, key, modifiers):
        if self.game_over_screen.is_high_score:
            if key == arcade.key.BACKSPACE:
                self.game_over_screen.player_name = self.game_over_screen.player_name[:-1]
            elif key == arcade.key.ENTER and self.game_over_screen.player_name:
                self.scoring.update_high_scores(self.game_over_screen.player_name, self.current_score)
                self.game_over_screen.is_high_score = False
                self.game_state = "WELCOME"
            elif 97 <= key <= 122:
                if len(self.game_over_screen.player_name) < 20:
                    self.game_over_screen.player_name += chr(key).upper()
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

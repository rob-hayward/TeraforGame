# game_window.py
import arcade
import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SUN_SIZE, ORBIT_RADIUS, PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME
from sun import Sun
from particles import *
from collision_handling import update_particles, handle_collision
from square_building import check_for_adjacent_neutral_particles, check_for_squares, handle_gravitational_collapse, check_for_adjacent_squares, check_for_big_squares


class MyGame(arcade.Window):
    def __init__(self, title):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title, fullscreen=True)
        self.sun = None
        self.light_grey_particle = None
        self.particle_timer = 0
        self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)
        self.particles = arcade.SpriteList()

    def setup(self):
        self.sun = Sun(SUN_SIZE)
        self.light_grey_particle = LightGreyParticle()
        self.light_grey_particle.center_x = SCREEN_WIDTH / 2
        self.light_grey_particle.center_y = SCREEN_HEIGHT / 2
        self.light_grey_particle.speed = 0
        self.particles.append(self.light_grey_particle)

    def on_draw(self):
        arcade.start_render()
        self.sun.draw()
        for particle in self.particles:
            particle.draw()

    def update(self, delta_time):
        self.sun.update()
        self.light_grey_particle.update()

        # Emit new particles and update positions
        self.particle_timer += delta_time
        if self.particle_timer >= self.next_particle_time:
            self.particle_timer = 0
            self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)
            new_particle = self.sun.emit_particle()
            self.particles.append(new_particle)

        # Update and handle FireParticle separately
        for particle in self.particles:
            if isinstance(particle, FireParticle):
                particle.update()
            else:
                # Update particle positions and handle collisions/explosions
                update_particles(self.particles, delta_time, self.sun.center_x, self.sun.center_y)

                # Check for squares and big squares
                neutral_particle_classes = [LightGreyParticle, DarkGreyParticle, BrownParticle, RustRedParticle,
                                            CrimsonParticle, OrangeParticle, BrightYellowParticle, LightYellowParticle,
                                            WhiteParticle, BlueWhiteParticle, VividBlueParticle]
                adjacent_pairs_by_type = check_for_adjacent_neutral_particles(self.particles, neutral_particle_classes)
                for pairs_list in adjacent_pairs_by_type.values():
                    square_particles = check_for_squares(pairs_list)
                    if square_particles:
                        # Check for adjacent squares and big squares within those squares
                        adjacent_squares = check_for_adjacent_squares(square_particles)
                        big_squares = check_for_big_squares(adjacent_squares)
                        handle_gravitational_collapse(self.particles, square_particles, big_squares)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close()

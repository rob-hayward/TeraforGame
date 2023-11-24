# game_window.py
import arcade
import math
import random
import time
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SUN_SIZE, ORBIT_RADIUS, PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME
from sun import Sun
from particles import LightGreyParticle

class MyGame(arcade.Window):
    def __init__(self, title):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title, fullscreen=True)
        self.sun = None
        self.light_grey_particle = None
        self.particle_timer = 0
        self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)
        self.particles = []

    def setup(self):
        self.sun = Sun(SUN_SIZE)  # Initialize the sun
        self.light_grey_particle = LightGreyParticle()
        self.light_grey_particle.center_x = SCREEN_WIDTH / 2
        self.light_grey_particle.center_y = SCREEN_HEIGHT / 2

    def on_draw(self):
        arcade.start_render()
        self.sun.draw()
        self.light_grey_particle.draw()
        for particle in self.particles:
            particle.draw()

    def update(self, delta_time):
        self.sun.update()
        self.light_grey_particle.update()
        # Update particle timer
        self.particle_timer += delta_time
        if self.particle_timer >= self.next_particle_time:
            # Reset timer and set next particle time
            self.particle_timer = 0
            self.next_particle_time = random.uniform(PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME)

            # Emit a particle from the sun
            new_particle = self.sun.emit_particle()
            self.particles.append(new_particle)

        # Update each particle's position
        for particle in self.particles:
            # Move particle towards the center of the screen
            particle.center_x -= particle.speed * math.cos(particle.angle)
            particle.center_y -= particle.speed * math.sin(particle.angle)
            particle.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close()

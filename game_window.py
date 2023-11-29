# game_window.py
import arcade
import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SUN_SIZE, ORBIT_RADIUS, PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME
from sun import Sun
from particles import LightGreyParticle, FireParticle
from collision_handling import update_particles, handle_collision


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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close()

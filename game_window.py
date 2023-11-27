import arcade
import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SUN_SIZE, ORBIT_RADIUS, PARTICLE_EMISSION_MIN_TIME, PARTICLE_EMISSION_MAX_TIME
from sun import Sun
from particles import LightGreyParticle
from collision_handling import handle_collision

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

        # Collision detection and handling
        for particle in self.particles:
            if particle.speed > 0:
                # Predict the next position of the particle
                next_x = particle.center_x - particle.speed * math.cos(particle.angle)
                next_y = particle.center_y - particle.speed * math.sin(particle.angle)

                # Temporarily update the particle's position
                particle.center_x = next_x
                particle.center_y = next_y

                # Check for collision at this new position
                hit_list = arcade.check_for_collision_with_list(particle, self.particles)
                for hit_particle in hit_list:
                    if hit_particle != particle:
                        handle_collision(particle, hit_particle)
                        break  # Stop checking after the first collision

                # Revert the position if no collision occurred
                if not hit_list:
                    particle.center_x -= particle.speed * math.cos(particle.angle)
                    particle.center_y -= particle.speed * math.sin(particle.angle)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close()

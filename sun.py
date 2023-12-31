# sun.py
import random
from collision_handling import moving_particles
from particles import LightGreyParticle, PositiveParticle, NegativeParticle
import arcade
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ORBIT_RADIUS, ORBIT_SPEED


class Sun(arcade.Sprite):
    def __init__(self, image_file, scale=1.05, orbit_radius=ORBIT_RADIUS, orbit_speed=ORBIT_SPEED):
        super().__init__(image_file, scale)
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.orbit_center_x = SCREEN_WIDTH / 2
        self.orbit_center_y = SCREEN_HEIGHT / 2
        self.angle = 0
        self.radius = 650
        self.positive_emission_sound = arcade.load_sound("assets/sounds/positive_emission_sound.wav")
        self.negative_emission_sound = arcade.load_sound("assets/sounds/negative_emission_sound.wav")
        self.neutral_emission_sound = arcade.load_sound("assets/sounds/neutral_emission_sound.wav")

    def reverse_orbit_direction(self):
        self.orbit_speed = -self.orbit_speed

    def emit_particle(self):
        particle_type = random.choice([LightGreyParticle, PositiveParticle, NegativeParticle])
        particle = particle_type()

        # Play sound based on particle type
        if isinstance(particle, PositiveParticle):
            arcade.play_sound(self.positive_emission_sound)
        elif isinstance(particle, NegativeParticle):
            arcade.play_sound(self.negative_emission_sound)
        elif isinstance(particle, LightGreyParticle):
            arcade.play_sound(self.neutral_emission_sound)

        offset = 1  # Offset to place the particle slightly away from the sun's edge
        particle.center_x = self.center_x - ((self.width / 2) + offset) * math.cos(self.angle)
        particle.center_y = self.center_y - ((self.height / 2) + offset) * math.sin(self.angle)
        particle.angle = math.degrees(math.atan2(SCREEN_HEIGHT / 2 - particle.center_y,
                                                 SCREEN_WIDTH / 2 - particle.center_x))
        particle.speed = 0.5
        moving_particles.add(particle)
        return particle

    def update(self, delta_time=1 / 60):
        self.angle += self.orbit_speed * delta_time
        self.center_x = self.orbit_center_x + self.orbit_radius * math.cos(self.angle)
        self.center_y = self.orbit_center_y + self.orbit_radius * math.sin(self.angle)

# sun.py
import arcade
import math
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SUN_SIZE, ORBIT_RADIUS, ORBIT_SPEED
from particles import LightGreyParticle, PositiveParticle, NegativeParticle


class Sun(arcade.Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        # self.change_colors = True
        # self.color_phase = 0
        self.orbit_center_x = SCREEN_WIDTH / 2
        self.orbit_center_y = SCREEN_HEIGHT / 2
        self.orbit_radius = ORBIT_RADIUS
        self.angle = 0

        # self.update_texture()
        self.texture = arcade.make_soft_circle_texture(self.size, arcade.color.YELLOW, outer_alpha=255)

    # def update_texture(self):
    #     # Change color to simulate burning
    #     if self.change_colors:
    #         if self.color_phase == 0:
    #             color = arcade.color.WHITE
    #         elif self.color_phase == 1:
    #             color = arcade.color.YELLOW
    #         elif self.color_phase == 2:
    #             color = (255, 255, 204)  # Lighter Yellow
    #         self.color_phase = (self.color_phase + 1) % 3
    #
    #         self.texture = arcade.make_soft_circle_texture(self.size, color, outer_alpha=255)

    def emit_particle(self):
        # Randomly choose the type of particle
        particle_type = random.choice([LightGreyParticle, PositiveParticle, NegativeParticle])
        particle = particle_type()

        # Calculate the offset to place the particle slightly away from the sun's edge
        offset = 1  # You can adjust this value

        # Position the particle slightly away from the edge of the sun
        particle.center_x = self.center_x - ((self.size / 2) + offset) * math.cos(self.angle)
        particle.center_y = self.center_y - ((self.size / 2) + offset) * math.sin(self.angle)


        # Set the angle and speed for the particle to move towards the screen center
        particle.angle = math.degrees(math.atan2(SCREEN_HEIGHT / 2 - particle.center_y,
                                                 SCREEN_WIDTH / 2 - particle.center_x))
        particle.speed = 1  # Set the initial speed

        return particle

    def update(self):
        self.angle += ORBIT_SPEED  # Adjust this value to change the speed of orbit
        self.center_x = self.orbit_center_x + self.orbit_radius * math.cos(self.angle)
        self.center_y = self.orbit_center_y + self.orbit_radius * math.sin(self.angle)
        # self.update_texture()
# particles.py contains the Particle class and its subclasses.
import arcade
import math
from constants import *

class Particle(arcade.Sprite):
    def __init__(self, color, width, height, gravitational_value):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.gravitational_value = gravitational_value
        self.texture = arcade.make_soft_square_texture(max(width, height), color, outer_alpha=255)
        self.speed = 1
        self.angle = 0
        self.is_neutral = True  # Default value for neutral particles

    def update(self):
        # Update position based on speed and angle
        self.center_x += self.speed * math.cos(math.radians(self.angle))
        self.center_y += self.speed * math.sin(math.radians(self.angle))

class LightGreyParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_LIGHT_GREY, 20, 20, 1)

class DarkGreyParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_DARK_GREY, 20, 20, 2)

class BrownParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_BROWN, 20, 20, 3)

class RustRedParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_RUST_RED, 20, 20, 4)

class CrimsonParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_CRIMSON, 20, 20, 5)

class OrangeParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_ORANGE, 20, 20, 6)

class BrightYellowParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_BRIGHT_YELLOW, 20, 20, 7)

class LightYellowParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_LIGHT_YELLOW, 20, 20, 8)

class WhiteParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_WHITE, 20, 20, 9)

class BlueWhiteParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_BLUE_WHITE, 20, 20, 10)

class VividBlueParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_VIVID_BLUE, 20, 20, 11)


class PositiveParticle(Particle):
    instances = []  # Class-level attribute for tracking instances

    def __init__(self):
        super().__init__(COLOR_ELECTRIC_BLUE, 20, 20, 0.5)
        PositiveParticle.instances.append(self)  # Add this instance to the list
        self.is_neutral = False

    @classmethod
    def remove_instance(cls, instance):
        if instance in cls.instances:
            cls.instances.remove(instance)


class NegativeParticle(Particle):
    instances = []  # Class-level attribute for tracking instances

    def __init__(self):
        super().__init__(COLOR_BRIGHT_RED, 20, 20, 0.5)
        NegativeParticle.instances.append(self)  # Add this instance to the list
        self.is_neutral = False
    @classmethod
    def remove_instance(cls, instance):
        if instance in cls.instances:
            cls.instances.remove(instance)


class FireParticle(arcade.Sprite):
    def __init__(self, sun_center_x, sun_center_y):
        # Create a fire texture
        fire_texture = self.create_fire_texture(20)
        super().__init__(texture=fire_texture, scale=1)

        self.center_x = (sun_center_x + sun_center_y) / 2  # Set initial position
        self.center_y = (sun_center_x + sun_center_y) / 2

        # Set direction towards the screen edge
        dx = SCREEN_WIDTH / 2 - self.center_x
        dy = SCREEN_HEIGHT / 2 - self.center_y
        self.angle = math.degrees(math.atan2(dy, dx)) + 180
        self.speed = 2

    @staticmethod
    def create_fire_texture(size):
        return arcade.make_soft_circle_texture(size, arcade.color.ORANGE, outer_alpha=255)

    def check_collision_with_sun(self, sun):
        # Check for collision with the sun sprite
        return arcade.check_for_collision(self, sun)

    def is_outside_screen(self):
        # Check if the particle is outside the screen bounds
        return (self.center_x < 0 or self.center_x > SCREEN_WIDTH or
                self.center_y < 0 or self.center_y > SCREEN_HEIGHT)

    def update(self):
        self.center_x += self.speed * math.cos(math.radians(self.angle))
        self.center_y += self.speed * math.sin(math.radians(self.angle))


class RadioactiveParticle(Particle):
    def __init__(self):
        super().__init__(arcade.color.GREEN_YELLOW, 20, 20, 0)  # Example color and size
        self.speed = 2  # Example speed

    def update(self):
        super().update()
        # Check if outside the screen or handle collision logic
        if self.is_outside_screen():
            self.remove_from_sprite_lists()

    def is_outside_screen(self):
        return (self.center_x < 0 or self.center_x > SCREEN_WIDTH or
                self.center_y < 0 or self.center_y > SCREEN_HEIGHT)






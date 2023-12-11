# particles.py contains the Particle class and its subclasses.
import arcade
import math
from constants import *


class Particle(arcade.Sprite):
    def __init__(self, image_file, width, height, gravitational_value):
        super().__init__(image_file, scale=1)
        self.width = width
        self.height = height
        self.gravitational_value = gravitational_value
        self.speed = 1
        self.angle = 0
        self.is_neutral = True  # Default value for neutral particles

    def update(self):
        # Update position based on speed and angle
        self.center_x += self.speed * math.cos(math.radians(self.angle))
        self.center_y += self.speed * math.sin(math.radians(self.angle))

    def angle_towards_center(self, center_x, center_y):
        # Calculate the angle towards the center of the screen
        dx = center_x - self.center_x
        dy = center_y - self.center_y
        return math.degrees(math.atan2(dy, dx))


class LightGreyParticle(Particle):
    def __init__(self):
        super().__init__("assets/light_grey_rock.png", 20, 20, 1)


class DarkGreyParticle(Particle):
    def __init__(self):
        super().__init__("assets/dark_grey_rock.png", 20, 20, 2)


class BrownParticle(Particle):
    def __init__(self):
        super().__init__("assets/brown_rock.png", 20, 20, 3)

# class RustRedParticle(Particle):
#     def __init__(self):
#         super().__init__(COLOR_RUST_RED, 20, 20, 4)
#
# class CrimsonParticle(Particle):
#     def __init__(self):
#         super().__init__(COLOR_CRIMSON, 20, 20, 5)
#
# class OrangeParticle(Particle):
#     def __init__(self):
#         super().__init__(COLOR_ORANGE, 20, 20, 6)
#
# class BrightYellowParticle(Particle):
#     def __init__(self):
#         super().__init__(COLOR_BRIGHT_YELLOW, 20, 20, 7)
#
# class LightYellowParticle(Particle):
#     def __init__(self):
#         super().__init__(COLOR_LIGHT_YELLOW, 20, 20, 8)
#
# class WhiteParticle(Particle):
#     def __init__(self):
#         super().__init__(COLOR_WHITE, 20, 20, 9)
#
# class BlueWhiteParticle(Particle):
#     def __init__(self):
#         super().__init__(COLOR_BLUE_WHITE, 20, 20, 10)
#
# class VividBlueParticle(Particle):
#     def __init__(self):
#         super().__init__(COLOR_VIVID_BLUE, 20, 20, 11)


class PositiveParticle(Particle):
    instances = []  # Class-level attribute for tracking instances

    def __init__(self):
        super().__init__("assets/blue_energy2.png", 20, 20, 0)
        PositiveParticle.instances.append(self)  # Add this instance to the list
        self.is_neutral = False

    @classmethod
    def remove_instance(cls, instance):
        if instance in cls.instances:
            cls.instances.remove(instance)


class NegativeParticle(Particle):
    instances = []  # Class-level attribute for tracking instances

    def __init__(self):
        super().__init__("assets/red_energy2.png", 20, 20, 0)
        NegativeParticle.instances.append(self)  # Add this instance to the list
        self.is_neutral = False

    @classmethod
    def remove_instance(cls, instance):
        if instance in cls.instances:
            cls.instances.remove(instance)


class FireParticle(Particle):
    def __init__(self, initial_x, initial_y):
        super().__init__("assets/purple_energy.png", 20, 20, 0)  # Assuming 'fire_particle.png' is your fire image
        self.center_x = initial_x
        self.center_y = initial_y
        dx = SCREEN_WIDTH / 2 - self.center_x
        dy = SCREEN_HEIGHT / 2 - self.center_y
        self.angle = math.degrees(math.atan2(dy, dx)) + 180
        self.speed = 0.5

    def update(self):
        super().update()  # This calls the update method from Particle class


class RadioactiveParticle(Particle):
    def __init__(self):
        super().__init__("assets/green_energy.png", 20, 20, 0)
        self.speed = 0.2

    def update(self):
        super().update()
        # Update position based on speed and direction
        self.center_x += self.speed * math.cos(math.radians(self.angle))
        self.center_y += self.speed * math.sin(math.radians(self.angle))


GRAVITATIONAL_MAPPING = {
    1: LightGreyParticle,
    2: DarkGreyParticle,
    3: BrownParticle,
    # ... continue mapping for other particle types
}
import arcade
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

    def update(self):
        pass

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
    def __init__(self):
        super().__init__(COLOR_ELECTRIC_BLUE, 10, 10, 0.5)

class NegativeParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_BRIGHT_RED, 10, 10, 0.5)

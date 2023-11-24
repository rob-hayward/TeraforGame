import arcade
from constants import *


class Particle(arcade.Sprite):
    def __init__(self, color, size, gravitational_value):
        super().__init__()
        self.color = color
        self.size = size
        self.gravitational_value = gravitational_value
        self.width = size
        self.height = size
        self.texture = arcade.make_soft_square_texture(size, color, outer_alpha=255)
        self.speed = 1  # Adjust as needed
        self.angle = 0  # Direction angle; adjust based on desired movement

    def update(self):
        # Update particle logic here (movement, interactions, etc.)
        pass

# Specific Particle Types
class LightGreyParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_LIGHT_GREY, 20, 1)

class DarkGreyParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_DARK_GREY, 20, 2)

class BrownParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_BROWN, 20, 3)

class RustRedParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_RUST_RED, 20, 4)

class CrimsonParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_CRIMSON, 20, 5)

class OrangeParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_ORANGE, 20, 6)

class BrightYellowParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_BRIGHT_YELLOW, 20, 7)

class LightYellowParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_LIGHT_YELLOW, 20, 8)

class WhiteParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_WHITE, 20, 9)

class BlueWhiteParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_BLUE_WHITE, 20, 10)

class VividBlueParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_VIVID_BLUE, 20, 11)

class PositiveParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_ELECTRIC_BLUE, 10, 0.5)

class NegativeParticle(Particle):
    def __init__(self):
        super().__init__(COLOR_BRIGHT_RED, 10, 0.5)


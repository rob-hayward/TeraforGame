# collision_handling.py
import arcade
from constants import COLOR_LIGHT_GREY
from particles import LightGreyParticle, DarkGreyParticle, PositiveParticle, NegativeParticle


def handle_collision(particle1, particle2):
    """
    Align particles upon collision, considering different sizes.
    """
    # Determine the direction of collision
    x_diff = particle1.center_x - particle2.center_x
    y_diff = particle1.center_y - particle2.center_y

    # Check if either particle is a smaller particle (positive or negative)
    smaller_particle = None
    if isinstance(particle1, (PositiveParticle, NegativeParticle)):
        smaller_particle = particle1
    elif isinstance(particle2, (PositiveParticle, NegativeParticle)):
        smaller_particle = particle2

    if smaller_particle:
        # Align smaller particle based on the collision with a larger particle
        align_smaller_particle(smaller_particle, particle1 if smaller_particle != particle1 else particle2, x_diff, y_diff)
    else:
        # Standard alignment for equal-sized particles
        standard_alignment(particle1, particle2, x_diff, y_diff)

    # Stop the movement of both particles
    particle1.speed = 0
    particle2.speed = 0


def align_smaller_particle(smaller_particle, other_particle, x_diff, y_diff):
    """
    Align a smaller particle (either positive or negative) with a larger particle.
    """
    x_diff = smaller_particle.center_x - other_particle.center_x
    y_diff = smaller_particle.center_y - other_particle.center_y

    if abs(x_diff) > abs(y_diff):
        # Horizontal collision
        if x_diff > 10 and y_diff > 0:
            if smaller_particle.speed > 0:
                # smaller_particle is moving left and is above other_particle center
                smaller_particle.left = other_particle.right
                smaller_particle.top = other_particle.top
            else:
                # smaller_particle is stationary on left of and above other_particle center
                other_particle.right = smaller_particle.left
                other_particle.top = smaller_particle.top

        elif x_diff > 10 and y_diff < 0:
            if smaller_particle.speed > 0:
                # smaller_particle is moving left and is below other_particle center
                smaller_particle.left = other_particle.right
                smaller_particle.bottom = other_particle.bottom
            else:
                # smaller_particle stationary on left of and below other_particle center
                other_particle.right = smaller_particle.left
                other_particle.bottom = smaller_particle.bottom

        elif x_diff < 10 and y_diff > 0:
            if smaller_particle.speed > 0:
                # smaller_particle is moving right and is above other_particle center
                smaller_particle.right = other_particle.left
                smaller_particle.top = other_particle.top
            else:
                # smaller_particle is stationary on right of and above other_particle center
                other_particle.left = smaller_particle.right
                other_particle.top = smaller_particle.top

        else:
            if smaller_particle.speed > 0:
                # smaller_particle is moving right and is below other_particle center
                smaller_particle.right = other_particle.left
                smaller_particle.bottom = other_particle.bottom
            else:
                # smaller_particle is stationary on right of and below other_particle center
                other_particle.left = smaller_particle.right
                other_particle.bottom = smaller_particle.bottom

    else:
        # Vertical collision
        if x_diff > 0 and y_diff > 10:
            # smaller_particle is moving down and is right of other_particle center
            if smaller_particle.speed > 0:
                smaller_particle.bottom = other_particle.top
                smaller_particle.left = other_particle.left
            # smaller_particle is stationary and is right of other_particle center
            else:
                other_particle.top = smaller_particle.bottom
                other_particle.left = smaller_particle.left

        elif x_diff > 0 and y_diff < 10:
            # smaller_particle is moving up and is right of other_particle center
            if smaller_particle.speed > 0:
                smaller_particle.top = other_particle.bottom
                smaller_particle.left = other_particle.left
            # smaller_particle is stationary and is right of other_particle center
            else:
                other_particle.bottom = smaller_particle.top
                other_particle.left = smaller_particle.left

        elif x_diff < 0 and y_diff > 10:
            # smaller_particle is moving down and is left of other_particle center
            if smaller_particle.speed > 0:
                smaller_particle.bottom = other_particle.top
                smaller_particle.right = other_particle.right
            # smaller_particle is stationary and is left of other_particle center
            else:
                other_particle.top = smaller_particle.bottom
                other_particle.right = smaller_particle.right
            # smaller_particle is above other_particle and to the left of other_particle center

        else:
            # smaller_particle is moving up and is left of other_particle center
            if smaller_particle.speed > 0:
                smaller_particle.top = other_particle.bottom
                smaller_particle.right = other_particle.right
            # smaller_particle is stationary and is left of other_particle center
            else:
                other_particle.bottom = smaller_particle.top
                other_particle.right = smaller_particle.right


def standard_alignment(particle1, particle2, x_diff, y_diff):
    """
    Align two particles of similar size upon collision.
    """
    # x_diff = particle1.center_x - particle2.center_x
    # y_diff = particle1.center_y - particle2.center_y

    if abs(x_diff) > abs(y_diff):
        # Horizontal collision
        if x_diff > 0:
            # particle1 moving and is to the right of particle2
            if particle1.speed > 0:
                particle1.left = particle2.right
                particle1.top = particle2.top
            # particle1 is stationary and is to the right of particle2
            else:
                particle2.right = particle1.left
                particle2.top = particle1.top

        else:
            # particle1 is moving and is to the left of particle2
            if particle1.speed > 0:
                particle1.right = particle2.left
                particle1.top = particle2.top
            # particle1 is stationary and is to the left of particle2
            else:
                particle2.left = particle1.right
                particle2.top = particle1.top
    else:
        # Vertical collision
        if y_diff > 0:
            # particle1 moving and is above particle2
            if particle1.speed > 0:
                particle1.bottom = particle2.top
                particle1.left = particle2.left
            # particle1 is stationary and is above particle2
            else:
                particle2.top = particle1.bottom
                particle2.left = particle1.left

        else:
            # particle1 is moving and is below particle2
            if particle1.speed > 0:
                particle1.top = particle2.bottom
                particle1.left = particle2.left
            # particle1 is stationary and is below particle2
            else:
                particle2.bottom = particle1.top
                particle2.left = particle1.left

    # # Stop the movement of both particles
    # particle1.speed = 0
    # particle2.speed = 0


def check_for_cubes(particles):
    # Iterate through particles and check if any form a cube
    for particle in particles:
        if is_cube(particle):
            # Replace with a dark grey particle
            dark_grey_particle = DarkGreyParticle()
            dark_grey_particle.center_x = particle.center_x
            dark_grey_particle.center_y = particle.center_y
            particles.append(dark_grey_particle)
            particles.remove(particle)


def is_cube(particle):
    # Implement logic to determine if this particle is part of a cube
    return False  # Placeholder logic

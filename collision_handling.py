# collision_handling.py
import math
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from particles import LightGreyParticle, DarkGreyParticle, PositiveParticle, NegativeParticle, FireParticle


def handle_repulsion(particle1, particle2, particles, sun_center_x, sun_center_y):
    fire_particle = FireParticle(sun_center_x, sun_center_y)
    fire_particle.center_x = (particle1.center_x + particle2.center_x) / 2
    fire_particle.center_y = (particle1.center_y + particle2.center_y) / 2

    particles.append(fire_particle)

    # Remove the original particles
    particles.remove(particle1)
    particles.remove(particle2)
    if isinstance(particle1, PositiveParticle):
        PositiveParticle.remove_instance(particle1)
    if isinstance(particle2, PositiveParticle):
        PositiveParticle.remove_instance(particle2)
    if isinstance(particle1, NegativeParticle):
        NegativeParticle.remove_instance(particle1)
    if isinstance(particle2, NegativeParticle):
        NegativeParticle.remove_instance(particle2)


def update_particles(particles, delta_time, sun_center_x, sun_center_y):
    handled_particles = set()
    for particle in particles:
        particle.update()

        # Check for adjacent positive or negative particles
        check_for_adjacent_charged_particles(particles, sun_center_x, sun_center_y, handled_particles)

        # Collision detection and handling
        hit_list = arcade.check_for_collision_with_list(particle, particles)
        for hit_particle in hit_list:
            if hit_particle != particle and hit_particle not in handled_particles:
                # Handle standard collision
                handle_collision(particle, hit_particle)
                handled_particles.update([particle, hit_particle])
                break  # Stop checking after the first collision


def check_for_adjacent_charged_particles(particles, sun_center_x, sun_center_y, handled_particles):
    # Check for similarly charged particles
    for particle1 in PositiveParticle.instances:
        if particle1 in handled_particles:
            continue
        for particle2 in PositiveParticle.instances:
            if particle2 in handled_particles or particle1 is particle2:
                continue
            if check_proximity(particle1, particle2):
                handle_repulsion(particle1, particle2, particles, sun_center_x, sun_center_y)
                handled_particles.update([particle1, particle2])
                break

    for particle1 in NegativeParticle.instances:
        if particle1 in handled_particles:
            continue
        for particle2 in NegativeParticle.instances:
            if particle2 in handled_particles or particle1 is particle2:
                continue
            if check_proximity(particle1, particle2):
                handle_repulsion(particle1, particle2, particles, sun_center_x, sun_center_y)
                handled_particles.update([particle1, particle2])
                break

    # Check for oppositely charged particles
    for particle1 in PositiveParticle.instances:
        if particle1 in handled_particles:
            continue
        for particle2 in NegativeParticle.instances:
            if particle2 in handled_particles or particle1 is particle2:
                continue
            if check_proximity(particle1, particle2):
                handle_attraction(particle1, particle2, particles)
                handled_particles.update([particle1, particle2])
                break


def check_proximity(particle1, particle2):
    distance = math.sqrt((particle1.center_x - particle2.center_x) ** 2 +
                         (particle1.center_y - particle2.center_y) ** 2)
    return distance <= 21  # Adjacent particles


def handle_attraction(particle1, particle2, particles):
    # Create two light grey particles
    light_grey_particle1 = LightGreyParticle()
    light_grey_particle2 = LightGreyParticle()

    # Set their positions
    light_grey_particle1.center_x, light_grey_particle1.center_y = particle1.center_x, particle1.center_y
    light_grey_particle2.center_x, light_grey_particle2.center_y = particle2.center_x, particle2.center_y

    # Set speed to 0 to make them stationary
    light_grey_particle1.speed = 0
    light_grey_particle2.speed = 0

    # Add new particles to the list
    particles.append(light_grey_particle1)
    particles.append(light_grey_particle2)

    # Stop the movement of original particles and remove them
    particle1.speed = 0
    particle2.speed = 0
    particles.remove(particle1)
    particles.remove(particle2)
    PositiveParticle.remove_instance(particle1)
    NegativeParticle.remove_instance(particle2)


def handle_collision(particle1, particle2):
    if isinstance(particle1, FireParticle) or isinstance(particle2, FireParticle):
        return

    """
    Align particles upon collision
    """
    # Determine the direction of collision
    x_diff = particle1.center_x - particle2.center_x
    y_diff = particle1.center_y - particle2.center_y

    # Reset the angle of both particles
    particle1.angle = 0
    particle2.angle = 0

    # Align the particles
    standard_alignment(particle1, particle2, x_diff, y_diff)

    # Stop the movement of both particles
    particle1.speed = 0
    particle2.speed = 0


def standard_alignment(particle1, particle2, x_diff, y_diff):
    """
    Align two particles upon collision.
    """

    if abs(x_diff) > abs(y_diff):
        # Horizontal collision
        if x_diff > 0:
            # particle1 moving and is to the right of particle2
            if particle1.speed > 0:
                (particle1.left, particle1.top) = (particle2.right, particle2.top)
                # particle1.top = particle2.top
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




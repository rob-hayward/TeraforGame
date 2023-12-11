# square_building.py
from collections import defaultdict
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
# from collision_handling import stationary_particles
from particles import GRAVITATIONAL_MAPPING, LightGreyParticle, DarkGreyParticle, BrownParticle, PositiveParticle, \
    NegativeParticle, RadioactiveParticle, FireParticle


def group_particles_by_type(particles):
    groups = defaultdict(set)
    for particle in particles:
        groups[type(particle)].add((particle.center_x, particle.center_y))
    return groups


def find_3x3_squares(groups, stationary_particles, particles):
    for particle_type, coordinates in groups.items():
        if len(coordinates) >= 9:
            for coord in coordinates:
                if is_3x3_square(coord, coordinates):
                    handle_gravitational_collapse(stationary_particles, particles, particle_type, coord)


def is_3x3_square(coord, coordinates, margin=1):
    x, y = coord
    square_coords = set()
    for dx in range(3):
        for dy in range(3):
            expected_x = x + dx * 20
            expected_y = y + dy * 20
            # Check if there's a particle within the margin of error
            found = any(
                abs(particle_x - expected_x) <= margin and abs(particle_y - expected_y) <= margin
                for particle_x, particle_y in coordinates
            )
            if found:
                square_coords.add((expected_x, expected_y))
    return len(square_coords) == 9


def handle_gravitational_collapse(stationary_particles, particles, particle_type, coord):
    screen_center_x = SCREEN_WIDTH / 2
    screen_center_y = SCREEN_HEIGHT / 2
    x, y = coord

    # Calculate the center coordinates of the 3x3 square
    center_x = x + 20  # 20 is the width of each particle
    center_y = y + 20  # 20 is the height of each particle

    # Find the central particle and the particle closest to the screen center
    central_particle = None
    closest_particle = None
    min_distance_to_center = float('inf')

    for particle in stationary_particles:
        if particle.center_x == center_x and particle.center_y == center_y:
            central_particle = particle

        # Calculate distance to the screen center
        distance_to_center = math.sqrt(
            (particle.center_x - screen_center_x) ** 2 + (particle.center_y - screen_center_y) ** 2)
        if distance_to_center < min_distance_to_center:
            min_distance_to_center = distance_to_center
            closest_particle = particle

    if central_particle is None or closest_particle is None:
        return  # Essential particles not found

    # Replace the central particle
    replace_particle(central_particle, stationary_particles, particles)

    # Replace the closest particle if it's different from the central particle
    if closest_particle is not central_particle:
        replace_particle(closest_particle, stationary_particles, particles)


def replace_particle(old_particle, stationary_particles, particles):
    next_gravitational_value = old_particle.gravitational_value + 1
    NewParticleClass = GRAVITATIONAL_MAPPING.get(next_gravitational_value, LightGreyParticle)

    if NewParticleClass:
        new_particle = NewParticleClass()
        new_particle.center_x, new_particle.center_y = old_particle.center_x, old_particle.center_y
        new_particle.speed = 0

        stationary_particles.remove(old_particle)
        stationary_particles.add(new_particle)
        particles.remove(old_particle)
        particles.append(new_particle)






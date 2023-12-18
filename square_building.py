# square_building.py
from collections import defaultdict
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from particles import GRAVITATIONAL_MAPPING, PositiveParticle, NegativeParticle


def group_particles_by_type(stationary_particles):
    groups = defaultdict(set)
    for particle in stationary_particles:
        if isinstance(particle, (PositiveParticle, NegativeParticle)):
            continue
        rounded_x = round(particle.center_x)
        rounded_y = round(particle.center_y)
        groups[type(particle)].add((rounded_x, rounded_y))
    return groups


def find_3x3_squares(groups, stationary_particles, moving_particles, particles):
    for particle_type, coordinates in groups.items():
        if len(coordinates) >= 9:
            for coord in coordinates:
                if check_for_square(coord, coordinates):
                    handle_gravitational_collapse(stationary_particles, moving_particles, particles, particle_type, coord)


def check_for_square(center_coord, coordinates):
    x, y = center_coord
    nearby_particles = 0
    for particle_x, particle_y in coordinates:
        if abs(round(particle_x) - x) <= 30 and abs(round(particle_y) - y) <= 30:
            nearby_particles += 1
    return nearby_particles == 9


def handle_gravitational_collapse(stationary_particles, moving_particles, particles, particle_type, center_coord):
    screen_center_x = SCREEN_WIDTH / 2
    screen_center_y = SCREEN_HEIGHT / 2
    square_particles = set([particle for particle in stationary_particles
                            if isinstance(particle, particle_type) and
                               abs(particle.center_x - center_coord[0]) <= 30 and
                               abs(particle.center_y - center_coord[1]) <= 30])
    sorted_square_particles = sorted(square_particles,
                                     key=lambda p: (math.sqrt((p.center_x - screen_center_x) ** 2 +
                                                              (p.center_y - screen_center_y) ** 2),
                                                    p.center_x, p.center_y))
    particles_to_replace = sorted_square_particles[:4]
    replace_particles(particles_to_replace, stationary_particles, moving_particles, particles)


def replace_particles(particles_to_replace, stationary_particles, moving_particles, particles):
    replaced_particles = []
    for old_particle in particles_to_replace:
        next_gravitational_value = old_particle.gravitational_value + 1
        NewParticleClass = GRAVITATIONAL_MAPPING.get(next_gravitational_value, None)
        if NewParticleClass:
            new_particle = NewParticleClass()
            new_particle.center_x, new_particle.center_y = old_particle.center_x, old_particle.center_y
            new_particle.speed = 0
            safe_remove_particle(old_particle, stationary_particles, moving_particles, particles)
            stationary_particles.add(new_particle)
            particles.append(new_particle)
            replaced_particles.append(new_particle)
    print(f"Replaced {len(replaced_particles)} particles")


def safe_remove_particle(particle, stationary_particles, moving_particles, particles):
    if particle in stationary_particles:
        stationary_particles.remove(particle)
    if particle in moving_particles:
        moving_particles.remove(particle)
    if particle in particles:
        particles.remove(particle)

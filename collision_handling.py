# collision_handling.py
import math
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from particles import LightGreyParticle, DarkGreyParticle, PositiveParticle, NegativeParticle, FireParticle, \
    RadioactiveParticle, GRAVITATIONAL_MAPPING
import random
import sun

# from square_building import handle_gravitational_increase

# Two sets to track moving and stationary particles
moving_particles = set()
stationary_particles = set()


def safe_remove_particles(particle1, particle2, particles):
    # Remove particles from their respective sets
    if particle1 in moving_particles:
        moving_particles.discard(particle1)
    if particle2 in moving_particles:
        moving_particles.discard(particle2)
    if particle1 in stationary_particles:
        stationary_particles.discard(particle1)
    if particle2 in stationary_particles:
        stationary_particles.discard(particle2)
    # Remove particles from the main particles list
    if particle1 in particles:
        particles.remove(particle1)
    if particle2 in particles:
        particles.remove(particle2)


def detect_collision(particles, delta_time, sun):
    global moving_particles, stationary_particles
    for particle in particles:
        particle.update()

        # Handle collision for FireParticle
        if isinstance(particle, FireParticle):
            handle_fire_particle_collision(particle, particles, sun)

        # Check for screen boundary for all particles
        if particle.center_x < 0 or particle.center_x > SCREEN_WIDTH or particle.center_y < 0 or particle.center_y > SCREEN_HEIGHT:
            particles.remove(particle)

        # Collision detection and handling for moving particles
        if particle in moving_particles:
            for stationary_particle in stationary_particles:
                if arcade.check_for_collision(particle, stationary_particle):
                    handle_collision(particle, stationary_particle, particles)
                    break  # Once a collision is handled, move to the next particle


def handle_collision(moving_particle, stationary_particle, particles):
    if isinstance(stationary_particle, RadioactiveParticle) or isinstance(moving_particle, RadioactiveParticle):
        safe_remove_particles(moving_particle, stationary_particle, particles)

    else:
        # Set the speed and angle of both particles
        moving_particle.angle = 0
        stationary_particle.angle = 0
        moving_particle.speed = 0

        align_particles(moving_particle, stationary_particle)
        check_adjacent_particles(particles, sun)


def align_particles(moving_particle, stationary_particle):
    # Determine x and y differences
    x_diff = moving_particle.center_x - stationary_particle.center_x
    y_diff = moving_particle.center_y - stationary_particle.center_y

    # Horizontal alignment
    if abs(x_diff) > abs(y_diff):
        if x_diff > 0:
            moving_particle.left = round(stationary_particle.right)
        else:
            moving_particle.right = round(stationary_particle.left)
        moving_particle.top = round(stationary_particle.top)
    # Vertical alignment
    else:
        if y_diff > 0:
            moving_particle.bottom = round(stationary_particle.top)
        else:
            moving_particle.top = round(stationary_particle.bottom)
        moving_particle.left = round(stationary_particle.left)

    # Move the moving particle to stationary particles set
    moving_particles.discard(moving_particle)
    stationary_particles.add(moving_particle)


def check_adjacent_particles(particles, sun):
    # Create a copy of stationary_particles for safe iteration
    stationary_particles_copy = set(stationary_particles)

    for particle1 in stationary_particles_copy:
        for particle2 in stationary_particles_copy:

            # Skip checking a particle against itself
            if particle1 is particle2:
                continue

            if check_proximity(particle1, particle2):
                # Skip radioactive particles
                if isinstance(particle1, RadioactiveParticle) or isinstance(particle2, RadioactiveParticle):
                    continue

                # repel same charge particles
                if isinstance(particle1, PositiveParticle) and isinstance(particle2, PositiveParticle) or \
                        isinstance(particle1, NegativeParticle) and isinstance(particle2, NegativeParticle):
                    handle_repulsion(particle1, particle2, particles, sun)

                # attract opposite charge particles
                if isinstance(particle1, PositiveParticle) and isinstance(particle2, NegativeParticle) or \
                        isinstance(particle1, NegativeParticle) and isinstance(particle2, PositiveParticle):
                    handle_attraction(particle1, particle2, particles)

                # # look for particle with adjacent heavier particle
                # if particle1.gravitational_value != particle2.gravitational_value and (
                #         particle1.gravitational_value and particle2.gravitational_value > 0):
                #     check_multiple_adjacent(particle1, particle2, particles, sun)


def check_proximity(particle1, particle2):
    # Calculate the distance between two particles
    dx = particle1.center_x - particle2.center_x
    dy = particle1.center_y - particle2.center_y
    squared_distance = dx * dx + dy * dy

    # Define the proximity threshold (this can be adjusted as needed)
    proximity_threshold = 21 * 21  # Example threshold
    return squared_distance <= proximity_threshold


def handle_repulsion(particle1, particle2, particles, sun):
    # Calculate the midpoint between the two colliding particles
    mid_x = (particle1.center_x + particle2.center_x) / 2
    mid_y = (particle1.center_y + particle2.center_y) / 2

    safe_remove_particles(particle1, particle2, particles)

    # Create a FireParticle at this midpoint
    fire_particle = FireParticle(mid_x, mid_y)

    # Set the direction of the FireParticle to move away from the sun
    # Calculate angle away from the center of the screen (which is presumably where the sun is)
    dx = SCREEN_WIDTH / 2 - mid_x
    dy = SCREEN_HEIGHT / 2 - mid_y
    angle_away_from_center = math.degrees(math.atan2(dy, dx)) + 180
    fire_particle.angle = angle_away_from_center

    # Add the FireParticle to the particles list
    particles.append(fire_particle)


def handle_attraction(particle1, particle2, particles):
    # Create two neutral light grey particles
    neutral_particle1 = LightGreyParticle()
    neutral_particle2 = LightGreyParticle()

    safe_remove_particles(particle1, particle2, particles)

    # Position them at the same locations as the original particles
    neutral_particle1.center_x, neutral_particle1.center_y = particle1.center_x, particle1.center_y
    neutral_particle2.center_x, neutral_particle2.center_y = particle2.center_x, particle2.center_y

    # Ensure they are stationary
    neutral_particle1.speed = 0
    neutral_particle2.speed = 0

    # Add the new neutral particles to the stationary set and the main particles list
    stationary_particles.add(neutral_particle1)
    stationary_particles.add(neutral_particle2)
    particles.append(neutral_particle1)
    particles.append(neutral_particle2)


def handle_fire_particle_collision(particle, particles, sun):
    if arcade.check_for_collision(particle, sun):
        particles.remove(particle)
        emit_radioactive_particles(particle, particles)
        return True
    return False


def emit_radioactive_particles(particle, particles):
    base_angle_away_from_sun = math.degrees(
        math.atan2(SCREEN_HEIGHT / 2 - particle.center_y, SCREEN_WIDTH / 2 - particle.center_x))
    for i in range(2):
        radioactive_particle = RadioactiveParticle()
        radioactive_particle.center_x = particle.center_x
        radioactive_particle.center_y = particle.center_y

        angle_deviation = random.uniform(-30, 30)
        radioactive_particle.angle = base_angle_away_from_sun + angle_deviation
        radioactive_particle.speed = 0.2

        moving_particles.add(radioactive_particle)
        particles.append(radioactive_particle)


# def check_multiple_adjacent(particle1, particle2, particles, sun):
#     # Create a copy of stationary_particles for safe iteration
#     stationary_particles_copy = set(stationary_particles)
#
#     for particle3 in stationary_particles_copy:
#         if particle3 is particle1 or particle3 is particle2:
#             continue
#
#         if check_proximity(particle1, particle3) and check_proximity(particle2, particle3):
#             # Skip radioactive and charged particles
#             if isinstance(particle3, RadioactiveParticle or PositiveParticle or NegativeParticle):
#                 continue
#
#             # Find the particle with the lowest gravitational value
#             min_gravitational_particle = min([particle1, particle2, particle3], key=lambda p: p.gravitational_value)
#
#             # Check if this particle has at least two adjacent particles with higher gravitational values
#             adjacent_higher_particles = sum(1 for p in [particle1, particle2, particle3]
#                                             if p.gravitational_value > min_gravitational_particle.gravitational_value)
#
#             if adjacent_higher_particles >= 2:
#                 handle_gravitational_increase(min_gravitational_particle, particles)
#
#
# def handle_gravitational_increase(particle, particles):
#     # Get the next gravitational value
#     next_gravitational_value = particle.gravitational_value + 1
#
#     # Find the particle class corresponding to the next gravitational value
#     NewParticleClass = GRAVITATIONAL_MAPPING.get(next_gravitational_value)
#
#     if NewParticleClass:
#         # Create a new particle of the higher gravitational class
#         new_particle = NewParticleClass()
#         new_particle.center_x, new_particle.center_y = particle.center_x, particle.center_y
#         new_particle.speed = 0  # Assuming the new particle should be stationary initially
#
#         # Replace the existing particle with the new one
#         if particle in stationary_particles:
#             stationary_particles.remove(particle)
#         if particle in particles:
#             particles.remove(particle)
#
#         stationary_particles.add(new_particle)
#         particles.append(new_particle)
#
#         print(f"Replaced particle with higher gravitational particle at ({new_particle.center_x}, {new_particle.center_y})")
#     else:
#         print("No higher gravitational particle class found")


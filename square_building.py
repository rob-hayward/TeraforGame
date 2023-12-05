# square_building.py
import math
from particles import *


def check_proximity(particle1, particle2):
    squared_distance = (particle1.center_x - particle2.center_x) ** 2 + \
                       (particle1.center_y - particle2.center_y) ** 2
    return squared_distance <= (21 ** 2)  # Compare against squared distance


def is_square(pair1, pair2):
    p1, p2 = pair1
    p3, p4 = pair2
    return {p1.center_x, p2.center_x} == {p3.center_x, p4.center_x} and \
           {p1.center_y, p2.center_y} == {p3.center_y, p4.center_y}


def find_square_center(square):
    x_coords = [p.center_x for p in square]
    y_coords = [p.center_y for p in square]
    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    return center_x, center_y


def check_square_proximity(square1, square2):
    center1 = find_square_center(square1)
    center2 = find_square_center(square2)

    x_diff = abs(center1[0] - center2[0])
    y_diff = abs(center1[1] - center2[1])

    # Check if squares are adjacent and aligned
    # Considering squares are 40x40, and centers will be at least 40 units apart
    # Allow a small buffer (1 unit) for alignment
    return (x_diff <= 41 and y_diff == 0) or (y_diff <= 41 and x_diff == 0)


def is_big_square(square_pair1, square_pair2):
    for square1 in square_pair1:
        for square2 in square_pair2:
            if square1 == square2:
                return False
    # Find the centers of each square in the pairs
    center1_pair1 = find_square_center(square_pair1[0])
    center2_pair1 = find_square_center(square_pair1[1])
    center1_pair2 = find_square_center(square_pair2[0])
    center2_pair2 = find_square_center(square_pair2[1])

    # Check if the centers of the pairs form a larger square
    # This involves checking if they are diagonally aligned
    diagonal_distance = math.sqrt(2) * 40  # Diagonal distance in a 40x40 square
    if (abs(center1_pair1[0] - center2_pair2[0]) == diagonal_distance and
        abs(center1_pair1[1] - center2_pair2[1]) == diagonal_distance) or \
       (abs(center2_pair1[0] - center1_pair2[0]) == diagonal_distance and
        abs(center2_pair1[1] - center1_pair2[1]) == diagonal_distance):
        return True

    return False


def handle_gravitational_collapse(particles, square_particles, big_square_particles):
    processed_particles = set()  # Track processed particles to avoid duplication

    # Process big squares
    for big_square in big_square_particles:
        # Check if any particles in the big square have already been processed
        if any(p in processed_particles for pair in big_square for p in pair):
            continue

        print("Big square detected")

        # Identify the central four particles of each constituent square
        central_particles = []
        for square in big_square:
            # Assuming the square is a list of four particles, find the central point
            central_x = sum(p.center_x for p in square) / 4
            central_y = sum(p.center_y for p in square) / 4

            # Find the particle closest to the central point
            central_particle = min(square, key=lambda p: (p.center_x - central_x) ** 2 + (p.center_y - central_y) ** 2)
            central_particles.append(central_particle)

        # Determine the next gravitational value
        next_gravitational_value = central_particles[0].gravitational_value + 1

        # Create a mapping from gravitational value to particle class
        gravitational_mapping = {
            1: LightGreyParticle, 2: DarkGreyParticle, 3: BrownParticle,
            4: RustRedParticle, 5: CrimsonParticle, 6: OrangeParticle,
            7: BrightYellowParticle, 8: LightYellowParticle, 9: WhiteParticle,
            10: BlueWhiteParticle, 11: VividBlueParticle
        }
        new_particle_class = gravitational_mapping.get(next_gravitational_value, LightGreyParticle)

        # Replace the central particles with the next type
        for old_particle in central_particles:
            if old_particle not in processed_particles:
                new_particle = new_particle_class()
                new_particle.center_x, new_particle.center_y = old_particle.center_x, old_particle.center_y
                new_particle.speed = old_particle.speed
                particles.append(new_particle)
                particles.remove(old_particle)
                processed_particles.add(old_particle)


def check_for_adjacent_neutral_particles(particles, neutral_particle_classes):
    adjacent_pairs_by_type = {cls: [] for cls in neutral_particle_classes}
    for particle_class in neutral_particle_classes:
        class_instances = [p for p in particles if isinstance(p, particle_class)]
        for i, particle1 in enumerate(class_instances):
            for particle2 in class_instances[i+1:]:
                if check_proximity(particle1, particle2):
                    adjacent_pairs_by_type[particle_class].append((particle1, particle2))
    return adjacent_pairs_by_type


def check_for_squares(adjacent_pairs_list):
    squares_by_type = []
    for pair1 in adjacent_pairs_list:
        for pair2 in adjacent_pairs_list:
            if pair1 != pair2 and set(pair1).isdisjoint(set(pair2)) and is_square(pair1, pair2):
                squares_by_type.append([pair1[0], pair1[1], pair2[0], pair2[1]])
    return squares_by_type


def check_for_adjacent_squares(squares_list):
    adjacent_square_pairs = []

    # Check each pair of squares for proximity
    for i, square1 in enumerate(squares_list):
        for square2 in squares_list[i + 1:]:
            if check_square_proximity(square1, square2):
                # Add the adjacent square pair to the list
                adjacent_square_pairs.append((square1, square2))

    return adjacent_square_pairs


def check_for_big_squares(adjacent_squares_list):
    # Early exit if there are less than 2 sets of adjacent squares
    if len(adjacent_squares_list) < 2:
        return []

    big_squares = []

    for pair1 in adjacent_squares_list:
        for pair2 in adjacent_squares_list:
            if pair1 != pair2:
                # Flatten the pairs of squares to simple lists
                squares1 = pair1[0] + pair1[1]
                squares2 = pair2[0] + pair2[1]

                # Check if any square in pair1 is also in pair2
                if not any(square in squares2 for square in squares1):
                    if is_big_square(pair1, pair2):
                        big_squares.append(pair1 + pair2)

    return big_squares



# Example Usage
particles = []  # This should be your list of particle instances
neutral_particle_classes = [LightGreyParticle, DarkGreyParticle, BrownParticle, RustRedParticle,
                            CrimsonParticle, OrangeParticle, BrightYellowParticle, LightYellowParticle,
                            WhiteParticle, BlueWhiteParticle, VividBlueParticle]

adjacent_pairs_by_type = check_for_adjacent_neutral_particles(particles, neutral_particle_classes)

for particle_class, pairs_list in adjacent_pairs_by_type.items():
    square_particles = check_for_squares(pairs_list)
    if square_particles:
        handle_gravitational_collapse(particles, square_particles)




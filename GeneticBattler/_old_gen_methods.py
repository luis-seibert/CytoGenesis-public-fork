import numpy as np


def is_neighbour(center_skew, tile_skew):
    """Checks if tile coordinates are neighbours of own center in skewed axial coordinates"""

    r_dir, q_dir = np.subtract(center_skew, tile_skew)
    abs_sum = abs(r_dir) + abs(q_dir)

    if abs_sum == 1:
        return True
    elif abs_sum == 2 and r_dir + q_dir == 0:
        return True
    else:
        return False


def calc_no_hex(dist):
    """Calculates number of hexagons in the grid with n=number of rings around central hex"""

    return 3 * dist**2 + 3 * dist + 1

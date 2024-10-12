import math
import numpy as np
import random
from hexagon import HexagonTile
from cell import Cell


def compute_skew_to_pix(CENTER, min_radius, skew_coords):
    """Converts relative skewed hexagonal position to absolute pixel coordinates"""

    r, q = skew_coords

    pix_x = CENTER[0] + r * 2 * min_radius + min_radius * q
    pix_y = CENTER[1] + q * math.sqrt((2 * min_radius) ** 2 - min_radius ** 2)

    return pix_x, pix_y


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


def round_to_odd(value):
    """Round to the nearest integer and force it to be odd if it's even"""

    rounded = round(value)

    # If even, adjust by 1 to make it odd
    return rounded if rounded % 2 != 0 else rounded + 1 if value > rounded else rounded - 1


def round_to_even(value):
    """Round to the nearest integer and force it to be even if it's odd"""

    rounded = round(value)

    # If even, adjust by 1 to make it odd
    return rounded if rounded % 2 == 0 else rounded + 1 if value > rounded else rounded - 1


def axial_to_cube(skew):
    """Converts axial (skewed) r, q to cube coordinates with r, q, s"""

    r = skew[0]
    q = skew[1]
    s = -q-r
    return r, q, s


def cube_to_axial(cube):
    """Converts cube r, q, s to axial (skewed) coordinates with r, q"""

    r, q, s = cube
    return r, q


def cube_distance(a, b):
    vec = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return (abs(vec[0]) + abs(vec[1]) + abs(vec[2])) / 2


def calc_skew_dist(skew_1, skew_2):
    """Calculates distance in hex tiles between two coordinates in skewed coordinates"""

    skew_1_cube = axial_to_cube(skew_1)
    skew_2_cube = axial_to_cube(skew_2)

    return int(cube_distance(skew_1_cube, skew_2_cube))


def gaussian_probability(dist, sigma=0.25):
    """Calculate gaussian probability from distance with given std_dev = sigma"""

    coeff = 1 / (sigma * np.sqrt(2 * np.pi))
    exponent = np.exp(-(dist ** 2) / (2 * sigma ** 2))
    return coeff * exponent


def create_hexagon(skew_coords, HEX_COL, CENTER, SIZE, no_lvls):
    """Creates a hexagon tile at position with min radius given by SIZE and nutrient value"""

    dist = calc_skew_dist((0, 0), skew_coords)   # distance to center
    #variance = (dist / no_lvls)**1.15
    rand_fact = 0.35   # percentage of randomness
    lam_inc = 0.2   # steepness of exponential increase of nutrient reduction
    nut_col = HEX_COL[1] * np.exp(-lam_inc*dist) * (1 + random.uniform(-rand_fact, rand_fact))
    #nutr_color = HEX_COL[1] - random.randint(dist**3, round(HEX_COL[1] * variance) - dist**3)

    return HexagonTile(CENTER,
                       SIZE,
                       center_skew=skew_coords,
                       colour=[HEX_COL[0], nut_col, HEX_COL[2]],
                       nutrient=nut_col/HEX_COL[1],
                       cell_hex=None,
                       hex_neighbours=None)


def init_hexagons(HEX_COL, CENTER, SIZE, rings, no_lvls):
    """Creates a hexagonal tile hexagon with a number of rings around central hexagon
    hexagons: flat dict with skew coordinates as tuple for hex access
    """

    hexagons = {}
    coords = calc_hextiles((0,0), rings)

    # Create hexagons with coordinates
    for center_skew in coords:
        new_hex = create_hexagon(center_skew, HEX_COL, CENTER, SIZE, no_lvls)
        hexagons[center_skew] = new_hex

    return hexagons


def calc_hextiles(center, dist):
    """Calculates all hexagon tiles with distance from center through the constraint r+q+s = 0"""

    base_vect = [i for i in range(-dist, dist + 1)]
    coords = []  # [cube_to_axial((r, q, s)) for r in base_vect for q in base_vect for s in base_vect if r + q + s == 0]
    for r in base_vect:
        for q in base_vect:
            for s in base_vect:
                if r + q + s == 0:
                    coord = cube_to_axial((r, q, s))
                    coord = (coord[0] + center[0], coord[1] + center[1])
                    coords.append(coord)

    return coords


def calc_neighbours(center):
    """Calculates neighbouring tiles relative to center"""

    r, q = center

    return [(-1+r,0+q), (-1+r,1+q), (0+r,-1+q), (0+r,1+q), (1+r,-1+q), (1+r,0+q)]


def generate_random_positions(hexagons, no_cells):
    """Creates n random cell positions with a Gaussian distribution around central hexagon"""

    coords, probabilities = [], []

    # Calculate probabilities from distance to center
    for hex_key in hexagons:
        distance = hexagons[hex_key].dist
        coords.append(hexagons[hex_key].center_skew)
        probabilities.append(gaussian_probability(distance))   # Calculate Gaussian prob for each distance

    # Normalize probabilities to sum to 1
    probabilities /= np.array(probabilities).sum()

    # Clip no_cells to number of hexagons
    if no_cells > len(hexagons):
        no_cells = len(hexagons)

    selected_indices = np.random.choice(len(coords), size=no_cells, replace=False, p=probabilities)

    return [coords[i] for i in selected_indices]


def create_cell_line(game_state, cell_state, hexagons, no_cells, curr_lvl):
    """Creates a cell line of n-cells on given hexagons"""

    # Clip no_cells to number of hexagons
    if no_cells > len(hexagons):
        no_cells = len(hexagons)

    cell_line = {}
    pos_coords = generate_random_positions(hexagons, no_cells)   # generate random skew coordinates for cells

    for i in range(no_cells):
        x, y = pos_coords[i]
        cell = Cell((x, y), game_state, cell_state)
        cell.cell_state.NUTCONS = cell.cell_state.NUTCONS * (0.5 + 0.5 * (curr_lvl / (1 + curr_lvl)))
        cell_line[(x, y)] = cell

        hexagons[(x, y)].cell_hex = cell

    return cell_line


def replicate(cell, cell_line, hexagons):
    """Replicates given mature cell, alters the parent and adds daughter cell"""

    # Get neighbouring hex tiles
    all_neighbours = calc_neighbours(cell.center_skew)
    neighbours = [hexagons[neighbour] for neighbour in all_neighbours if neighbour in hexagons and hexagons[neighbour].cell_hex is None]

    if len(neighbours) > 0:
        # Clone daughter cell into random free hexagon
        new_hex = random.choice(neighbours)
        new_cell = Cell(new_hex.center_skew, cell.CELL_ARGS)
        new_cell.energy = cell.energy / 2
        cell_line[new_hex.center_skew] = new_cell
        hexagons[new_hex.center_skew].cell_hex = new_cell

        # Highlight new hexagon
        hexagons[new_hex.center_skew].new_cell = True

        # Half mother cell energy
        cell.energy = cell.energy / 2

    else:
        cell.growth = False   # growth arrest

    return cell_line, hexagons


def calc_no_hex(dist):
    """Calculates number of hexagons in the grid with n=number of rings around central hex"""

    return 3 * dist**2 + 3 * dist + 1


def disp_fps(screen, font, clock, color):
    fps_text = {
        'text': font.render('FPS: ' + str(int(clock.get_fps())), True, color),
        'pos': (20, 20)}
    screen.blit(fps_text['text'], fps_text['pos'])


def calc_frame_delay(frame_count, FPS, img_fps, no_img):
    """Calculates img index for given img FPS"""

    frame_delay = FPS // img_fps

    return (frame_count // frame_delay) % no_img

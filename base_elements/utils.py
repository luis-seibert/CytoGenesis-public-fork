import math
from typing import Any

import yaml


def get_config_from_yaml(path: str) -> Any:
    """Get configs from a yaml file.

    Args:
        path (str): The path to the yaml file.
    """

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config


def calculate_hexagon_neighbors(
    axial_coordinate: tuple[int, int],
) -> list[tuple[int, int]]:
    """Calculates neighboring tiles relative to given axial coordinates.

    Args:
        axial_coordinate (tuple[int, int]): The axial coordinates of the hexagon.

    Returns:
        list[tuple[int, int]]: A list of neighboring hexagon coordinates.
    """

    r, q = axial_coordinate

    return [
        (-1 + r, 0 + q),
        (-1 + r, 1 + q),
        (0 + r, -1 + q),
        (0 + r, 1 + q),
        (1 + r, -1 + q),
        (1 + r, 0 + q),
    ]


def calculate_axial_distance(a_axial: tuple[int, int], b_axial: tuple[int, int]) -> int:
    """Calculates distance in hex tiles between two coordinates in skewed coordinates.

    Args:
        a_axial (tuple[int, int]): The axial coordinates of the first hexagon.
        b_axial (tuple[int, int]): The axial coordinates of the second hexagon.

    Returns:
        int: The distance in hex tiles between the two coordinates.
    """

    a_cube = axial_to_cube(a_axial)
    b_cube = axial_to_cube(b_axial)

    return round(cube_distance(a_cube, b_cube))


def cube_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    """Calculates distance in hex tiles between two coordinates in cube coordinates.

    Args:
        a (tuple[int, int, int]): The cube coordinates of the first hexagon.
        b (tuple[int, int, int]): The cube coordinates of the second hexagon.

    Returns:
        float: The distance in hex tiles between the two coordinates.
    """

    vector = a[0] - b[0], a[1] - b[1], a[2] - b[2]

    return (abs(vector[0]) + abs(vector[1]) + abs(vector[2])) / 2


def axial_to_cube(coordinates_axial: tuple[int, int]) -> tuple[int, int, int]:
    """Converts axial (skewed) r, q to cube coordinates with r, q, s.

    Args:
        coordinates_axial (tuple[int, int]): The axial coordinates of the hexagon.

    Returns:
        tuple[int, int, int]: The cube coordinates of the hexagon.
    """

    r = coordinates_axial[0]
    q = coordinates_axial[1]
    s = -q - r

    return r, q, s


def cube_to_axial(coordinates_cube: tuple[int, int, int]) -> tuple[int, int]:
    """Converts cube r, q, s to axial (skewed) coordinates with r, q.

    Args:
        coordinates_cube (tuple[int, int, int]): The cube coordinates of the hexagon.

    Returns:
        tuple[int, int]: The axial coordinates of the hexagon.
    """

    r, q, _ = coordinates_cube

    return r, q


def calculate_pixel_from_axial(
    center: tuple[int, int], minimal_radius: int, axial_coordinates: tuple[int, int]
) -> tuple[int, int]:
    """Converts relative skewed hexagonal position to absolute pixel coordinates.

    Args:
        center (tuple[int, int]): The center pixel coordinates.
        minimal_radius (int): The minimal radius of the hexagon.
        axial_coordinates (tuple[int, int]): The axial coordinates of the hexagon.

    Returns:
        tuple[int, int]: The pixel coordinates of the hexagon.
    """

    r, q = axial_coordinates

    x_offset = r * 2 * minimal_radius + minimal_radius * q
    y_offset = q * math.sqrt(3) * minimal_radius

    pix_x = round(center[0] + x_offset)
    pix_y = round(center[1] + y_offset)

    return (pix_x, pix_y)

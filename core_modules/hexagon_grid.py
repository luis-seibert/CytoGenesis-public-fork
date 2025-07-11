"""Core module for the hexagonal grid.

This module contains the HexagonGrid class, which creates a grid of hexagonal tiles and manages
their properties. The grid is generated based on the number of rings, nutrient variation, and
nutrient richness. The hexagons are represented in axial coordinates, and their vertices are
calculated based on the screen size and hexagon radius. The class also provides methods to update
the hexagon vertices and create hexagons with specific properties.
"""

import math
import random

import numpy

from assets.colors import Colors
from core_modules.game_state import GameState
from core_modules.hexagon_tile import HexagonTile
from core_modules.utils import (
    calculate_axial_distance,
    calculate_pixel_from_axial,
    convert_cube_to_axial,
)


class HexagonGrid:
    """Hexagonal grid class that creates a grid of hexagonal tiles.

    Args:
        game_state (GameState): The game state containing the current game parameters.
        screen_size (tuple[int, int]): The size of the screen.
        center_offset (tuple[float, float], optional): Custom center point as fractions of screen
            size. Defaults to (0.5, 0.5).
    """

    def __init__(
        self,
        game_state: GameState,
        screen_size: tuple[int, int],
        center_offset: tuple[float, float] = (0.5, 0.5),
    ) -> None:
        self._update_size_parameters(
            screen_size, game_state.default_hexagon_minimal_radius_fraction, center_offset
        )
        self.default_hexagon_body_color = list(Colors().hexagon_body)
        self.hexagons = self._create_hexagon_ring(
            game_state.current_level,
            game_state.hexagon_nutrient_variation,
            game_state.hexagon_nutrient_richness,
        )
        self.update_hexagon_vertices(game_state, screen_size, center_offset)

    def create_hexagon(
        self, axial_coordinate, nutrient_variation: float, nutrient_richness: float
    ) -> HexagonTile:
        """Creates a hexagon tile with the given axial coordinates.

        Args:
            axial_coordinate (tuple[int, int]): The axial coordinates of the hexagon.
            nutrient_variation (float): The variation of nutrient.
            nutrient_richness (float): The richness of nutrient.

        Returns:
            HexagonTile: The created hexagon tile.
        """

        axial_distance_to_center = calculate_axial_distance((0, 0), axial_coordinate)
        nutrient_distance_factor = numpy.exp(-nutrient_variation * axial_distance_to_center)
        nutrient_randomness_factor = random.uniform(-nutrient_richness, nutrient_richness)

        nutrient_value = min(
            nutrient_distance_factor * (1 + nutrient_randomness_factor),
            1,
        )

        vertices = self._get_hexagon_vertices(axial_coordinate)

        return HexagonTile(
            axial_coordinate,
            vertices,
            nutrient_value,
            self.default_hexagon_body_color,
        )

    def update_hexagon_vertices(
        self,
        game_state: GameState,
        screen_size: tuple[int, int],
        center_offset: tuple[float, float] = (0.5, 0.5),
    ) -> None:
        """Updates the vertices of all hexagons in the grid based on the new screen size.

        Args:
            game_state (GameState): The game state containing the current game parameters.
            screen_size (tuple[int, int]): The new screen size.
            center_offset (tuple[float, float], optional): Custom center point as fractions of
                screen size. Defaults to (0.5, 0.5).
        """

        self._update_size_parameters(
            screen_size, game_state.default_hexagon_minimal_radius_fraction, center_offset
        )

        for hexagon in self.hexagons.values():
            hexagon.vertices = self._get_hexagon_vertices(hexagon.coordinate_axial)

    def recreate_background_hexagon_grid(
        self, game_state: GameState, screen_size: tuple[int, int], radius_fraction: int = 20
    ) -> None:
        """Recreate the hexagon grid for background use (like main menu).

        Args:
            game_state (GameState): The game state containing the current game parameters.
            screen_size (tuple[int, int]): The screen size.
            radius_fraction (int): The radius fraction for hexagon size. Defaults to 20.
        """

        original_radius = game_state.default_hexagon_minimal_radius_fraction
        game_state.default_hexagon_minimal_radius_fraction = radius_fraction
        self._update_size_parameters(screen_size, radius_fraction)

        screen_width, screen_height = screen_size
        number_r_hexagons = round(screen_width / self.maximal_radius / 2) + 9
        number_q_hexagons = round(screen_height / self.minimal_radius / 2) + 4

        coordinates = []
        r_offset = -round(number_r_hexagons / 2)
        q_offset = -round(number_q_hexagons / 2)
        for r in range(number_r_hexagons):
            for q in range(number_q_hexagons):
                coordinates.append((r_offset + r, q_offset + q))

        self.hexagons = {}
        for coordinate in coordinates:
            self.hexagons[coordinate] = self.create_hexagon(
                coordinate,
                game_state.hexagon_nutrient_variation,
                game_state.hexagon_nutrient_richness,
            )

        game_state.default_hexagon_minimal_radius_fraction = original_radius

    def get_total_nutrient(self) -> float:
        """Get the total nutrient remaining in all hexagons.

        Returns:
            float: The total nutrient value across all hexagons.
        """

        return sum(hexagon.nutrient_value for hexagon in self.hexagons.values())

    def _update_size_parameters(
        self,
        screen_size: tuple[int, int],
        radius_fraction: int,
        center_offset: tuple[float, float] = (0.5, 0.5),
    ) -> None:
        """Updates the size parameters of the hexagonal grid based on the screen size.

        Args:
            screen_size (tuple[int, int]): The size of the screen.
            game_state (GameState): The game state containing the current game parameters.
            center_offset (tuple[float, float], optional): Custom center point as fractions of
                screen size. Defaults to (0.5, 0.5).
        """

        self.screen_center_pixel = (
            round(screen_size[0] * center_offset[0]),
            round(screen_size[1] * center_offset[1]),
        )
        self.minimal_radius = round(round(screen_size[1] // radius_fraction))
        self.maximal_radius = round(self.minimal_radius / (math.sqrt(3) / 2))

    def _create_hexagon_ring(
        self, number_rings: int, nutrient_variation: float, nutrient_richness: float
    ) -> dict[tuple[int, int], HexagonTile]:
        """Creates a hexagonal tile grid with a given number of rings around the center tile.

        Args:
            number_rings (int): The number of rings to create around the center tile.
            nutrient_variation (float): The variation of nutrient.
            nutrient_richness (float): The richness of nutrient.

        Returns:
            dict: A dictionary containing the hexagonal tiles with their axial coordinates as keys.
        """

        hexagon_grid = {}
        hexagon_coordinates = self._get_neighbor_coordinates_with_distance((0, 0), number_rings)

        for axial_coordinates in hexagon_coordinates:
            hexagon = self.create_hexagon(
                axial_coordinates,
                nutrient_variation,
                nutrient_richness,
            )
            hexagon_grid[axial_coordinates] = hexagon

        return hexagon_grid

    def _get_neighbor_coordinates_with_distance(
        self, center_axial: tuple[int, int], distance_axial: int
    ) -> list[tuple[int, int]]:
        """Calculates all hexagon tiles with the given distance from the center.

        The coordinates are calculated in cube coordinates (r, q, s) and then converted to axial
        coordinates (r, q),. Valid hexagons are selected with r + q + s = 0.

        Args:
            center_axial (tuple[int, int]): The axial coordinates of the center hexagon.
            distance_axial (int): The distance from the center hexagon.

        Returns:
            list[tuple[int, int]]: A list of axial coordinates of hexagons within given distance.
        """

        base_vector = list(range(-distance_axial, distance_axial + 1))
        coordinates = []
        for r in base_vector:
            for q in base_vector:
                for s in base_vector:
                    if r + q + s == 0:
                        coordinate = convert_cube_to_axial((r, q, s))
                        coordinate = (
                            coordinate[0] + center_axial[0],
                            coordinate[1] + center_axial[1],
                        )
                        coordinates.append(coordinate)

        return coordinates

    def _get_hexagon_vertices(
        self, hexagon_coordinate_axial: tuple[int, int]
    ) -> list[tuple[float, float]]:
        """Calculates the vertices of a hexagon based on its axial coordinates.

        Args:
            hexagon_coordinate_axial (tuple[int, int]): The axial coordinates of the hexagon.

        Returns:
            list[tuple[float, float]]: A list of vertices of the hexagon.
        """

        x_coordinate_pixel, y_coordinate_pixel = calculate_pixel_from_axial(
            self.screen_center_pixel, self.minimal_radius, hexagon_coordinate_axial
        )

        vertices = []
        for i in range(6):
            angle = math.radians(30 + 60 * i)  # 60 degrees increments for hexagon inner angles
            x = x_coordinate_pixel + self.maximal_radius * math.cos(angle)
            y = y_coordinate_pixel + self.maximal_radius * math.sin(angle)
            vertices.append((x, y))

        return vertices

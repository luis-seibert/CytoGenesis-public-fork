import random

import numpy
from pygame import Surface

from base_elements.game_state import GameState
from base_elements.hexagon_tile import HexagonTile


class HexagonGrid:
    def __init__(self, game_state: GameState, screen: Surface) -> None:
        self.game_state: GameState = game_state
        self.screen: Surface = screen

    def initialize_hexagons(self) -> dict[tuple[int, int], HexagonTile]:
        """Creates a hexagonal tile hexagon with a number of rings around central hexagon
        hexagons: flat dict with skew coordinates as tuple for hex access
        """

        hexagons = {}
        rings = self.game_state.current_level
        coordinates = self.get_hextile_distant_neighbours((0, 0), rings)

        # Create hexagons with coordinates
        for axial_coordinates in coordinates:
            new_hexagon = self.create_hexagon(axial_coordinates)
            hexagons[axial_coordinates] = new_hexagon

        return hexagons

    def main_menu_grid(self) -> dict[tuple[int, int], HexagonTile]:

        screen_width, screen_height = self.screen.get_size()
        dummy_hexagon = self.create_hexagon((0, 0))
        number_r_hexagons = int(screen_width / dummy_hexagon.maximal_radius) + 1
        number_q_hexagons = int(screen_height / dummy_hexagon.minimal_radius) + 1

        coordinates = []
        r_offset = -int(round(number_r_hexagons / 2))
        q_offset = -int(round(number_q_hexagons / 2))
        for r in range(number_r_hexagons):
            for q in range(number_q_hexagons):
                coordinates.append((r_offset + r, q_offset + q))

        hexagons = {}
        for coordinate in coordinates:
            hexagons[coordinate] = self.create_hexagon(coordinate)

        return hexagons

    def create_hexagon(self, axial_coordinate):
        """Creates a hexagon tile at position with min radius given by SIZE and nutrient value"""

        distance_to_center = self.axial_distance((0, 0), axial_coordinate)

        hexagon_color = list(self.game_state.default_hexagon_body_color)

        nutrient_color = (
            hexagon_color[self.game_state.default_hexagon_nutrient_color_index]
            * numpy.exp(-self.game_state.hexagon_nutrient_varation * distance_to_center)
            * (
                1
                + random.uniform(
                    -self.game_state.hexagon_nutrient_richness,
                    self.game_state.hexagon_nutrient_richness,
                )
            )
        )
        if nutrient_color > 255:
            nutrient_color = 255

        index = self.game_state.default_hexagon_nutrient_color_index
        hexagon_color[index] = nutrient_color

        return HexagonTile(
            self.screen,
            self.game_state.default_hexagon_size,
            axial_coordinate,
            distance_to_center,
            hexagon_color,
            nutrient_color / 255,
        )

    def get_hextile_distant_neighbours(
        self, center_axial: tuple[int, int], distance_axial: int
    ) -> list[tuple[int, int]]:
        """Calculates all hexagon tiles with distance from center through the constraint r+q+s = 0"""

        base_vector = [i for i in range(-distance_axial, distance_axial + 1)]
        coordinates = []
        for r in base_vector:
            for q in base_vector:
                for s in base_vector:
                    if r + q + s == 0:
                        coordinate = self.cube_to_axial((r, q, s))
                        coordinate = (
                            coordinate[0] + center_axial[0],
                            coordinate[1] + center_axial[1],
                        )
                        coordinates.append(coordinate)

        return coordinates

    def axial_distance(self, a_axial: tuple[int, int], b_axial: tuple[int, int]) -> int:
        """Calculates distance in hex tiles between two coordinates in skewed coordinates"""

        a_cube = self.axial_to_cube(a_axial)
        b_cube = self.axial_to_cube(b_axial)

        return int(self.cube_distance(a_cube, b_cube))

    def axial_to_cube(self, coordinates_axial: tuple[int, int]) -> tuple[int, int, int]:
        """Converts axial (skewed) r, q to cube coordinates with r, q, s"""

        r = coordinates_axial[0]
        q = coordinates_axial[1]
        s = -q - r

        return r, q, s

    def cube_to_axial(self, coordinates_cube: tuple[int, int, int]) -> tuple[int, int]:
        """Converts cube r, q, s to axial (skewed) coordinates with r, q"""

        r, q, s = coordinates_cube

        return r, q

    def cube_distance(self, a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
        vec = a[0] - b[0], a[1] - b[1], a[2] - b[2]

        return (abs(vec[0]) + abs(vec[1]) + abs(vec[2])) / 2

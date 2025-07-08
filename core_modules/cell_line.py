"""Core module for managing a line of cells in a hexagonal grid.

This module contains the CellLine class, which is responsible for creating and managing a line of
cells in a hexagonal grid. The class includes methods for replicating cells, calculating biomass,
and generating random positions for cells based on a Gaussian distribution. It also includes
methods for scaling energy consumption rates and calculating Gaussian probabilities.
"""

import random

import numpy

from core_modules.cell import Cell
from core_modules.game_state import GameState
from core_modules.hexagon_grid import HexagonGrid
from core_modules.hexagon_tile import HexagonTile
from core_modules.utils import calculate_axial_distance, calculate_hexagon_neighbors


class CellLine:
    """Class that manages operations on a line of cells in a hexagonal grid.

    Args:
        hexagon_grid (HexagonGrid): The hexagonal grid containing the cells.
        game_state (GameState): The game state containing the current game parameters.
        screen_size (tuple[int, int]): The size of the screen.
        center_offset (tuple[float, float], optional): Custom center point as fractions of screen
            size. Defaults to (0.5, 0.5).
    """

    def __init__(
        self,
        hexagon_grid: HexagonGrid,
        game_state: GameState,
        screen_size: tuple[int, int],
        center_offset: tuple[float, float] = (0.5, 0.5),
    ) -> None:
        self.center_offset = center_offset
        self.cells = self._create_cells(hexagon_grid, game_state, screen_size, center_offset)

    def replicate_cell(
        self,
        cell_coordinate: tuple[int, int],
        hexagon_grid: HexagonGrid,
        game_state: GameState,
        screen_size: tuple[int, int],
    ) -> tuple[int, int] | None:
        """Replicates given mature cell to a new cell in the hexagon grid.

        Args:
            cell_coordinate (tuple[int, int]): The coordinate of the cell to replicate.
            hexagon_grid (HexagonGrid): The hexagonal grid containing the cells.
            game_state (GameState): The game state containing the current game parameters.
            screen_size (tuple[int, int]): The size of the screen.

        Returns:
            tuple[int, int] | None: The coordinates of the new cell or None if no unoccupied
                neighbors are found.
        """

        neighbor_coordinates = calculate_hexagon_neighbors(cell_coordinate)
        unoccupied_hexagons = hexagon_grid.hexagons.keys() - self.cells.keys()
        unoccupied_neighbors_coordinates = list(
            set(neighbor_coordinates).intersection(unoccupied_hexagons)
        )

        if unoccupied_neighbors_coordinates:
            daughter_coordinates = random.choice(unoccupied_neighbors_coordinates)
            daughter_cell = Cell(
                daughter_coordinates,
                game_state,
                hexagon_grid.minimal_radius,
                screen_size,
                self.center_offset,
            )

            self.cells[cell_coordinate].energy_value /= 2
            daughter_cell.energy_value = self.cells[cell_coordinate].energy_value
            self.cells[daughter_coordinates] = daughter_cell
            hexagon_grid.hexagons[daughter_coordinates].set_highlight()

            return daughter_coordinates

        self.cells[cell_coordinate].growth = False

        return None

    def get_biomass(self) -> float:
        """Calculates the total biomass of the cell line.

        Returns:
            float: The total biomass of the cell line.
        """

        return sum(cell.energy_value for cell in self.cells.values())

    def _create_cells(
        self,
        hexagon_grid: HexagonGrid,
        game_state: GameState,
        screen_size: tuple[int, int],
        center_offset: tuple[float, float] = (0.5, 0.5),
    ) -> dict[tuple[int, int], Cell]:
        """Creates a cell line on given hexagon grid.

        Args:
            hexagon_grid (HexagonGrid): The hexagonal grid to create cells on.
            game_state (GameState): The game state containing the current game parameters.
            screen_size (tuple[int, int]): The size of the screen.
            center_offset (tuple[float, float], optional): Custom center point as fractions of
                screen size. Defaults to (0.5, 0.5).

        Returns:
            dict[tuple[int, int], Cell]: A dictionary of cells with their coordinates as keys.
        """

        number_cells = min(game_state.number_cells, len(hexagon_grid.hexagons))
        coordinates = self._generate_random_positions(hexagon_grid.hexagons, number_cells)

        cells = {}
        for i in range(number_cells):
            cell = Cell(
                coordinates[i], game_state, hexagon_grid.minimal_radius, screen_size, center_offset
            )
            cell.energy_consumption_rate_maximum = self._scale_energy_consumption_rate(
                game_state.cell_energy_consumption_rate_maximum,
                game_state.current_level,
            )
            cells[coordinates[i]] = cell

        return cells

    def _generate_random_positions(
        self, hexagons: dict[tuple[int, int], HexagonTile], number_cells: int
    ) -> list[tuple[int, int]]:
        """Creates random cell positions with a Gaussian distribution around central hexagon.

        Args:
            hexagons (dict[tuple[int, int], HexagonTile]): The hexagonal tiles.
            number_cells (int): The number of cells to create.

        Returns:
            list[tuple[int, int]]: A list of random cell positions.
        """

        random_coordinates, coordinate_probabilities = [], []

        for hexagon_coordinate in hexagons.keys():
            distance_to_center = calculate_axial_distance((0, 0), hexagon_coordinate)
            random_coordinates.append(hexagon_coordinate)
            coordinate_probabilities.append(self._gaussian_probability(distance_to_center))

        coordinate_probabilities /= numpy.array(
            coordinate_probabilities
        ).sum()  # Normalize probabilities to sum to 1

        number_cells = min(number_cells, len(hexagons))

        selected_indices = numpy.random.choice(
            len(random_coordinates),
            size=number_cells,
            replace=False,
            p=coordinate_probabilities,
        )

        return [random_coordinates[i] for i in selected_indices]

    def _gaussian_probability(self, distance: float, sigma: float = 0.25) -> float:
        """Calculate gaussian probability from distance with given standard deviation.

        Args:
            distance (float): The distance from the center.
            sigma (float, optional): The standard deviation. Defaults to 0.25.

        Returns:
            float: The gaussian probability.
        """

        coefficient = 1 / (sigma * numpy.sqrt(2 * numpy.pi))
        exponent = numpy.exp(-(distance**2) / (2 * sigma**2))

        return coefficient * exponent

    def _scale_energy_consumption_rate(
        self,
        energy_consumption_rate: float,
        current_level: int,
    ) -> float:
        """Scale energy consumption rate based on current level.

        Args:
            energy_consumption_rate (float): The base energy consumption rate.
            current_level (int): The current level of the game.

        Returns:
            float: The scaled energy consumption rate.
        """

        return energy_consumption_rate * (0.5 + 0.5 * (current_level / (1 + current_level)))

import random

import numpy

from base_elements.cell import Cell
from base_elements.game_state import GameState
from base_elements.hexagon_grid import HexagonGrid
from base_elements.hexagon_tile import HexagonTile
from base_elements.utils import calculate_axial_distance, calculate_hexagon_neighbors


class CellLine:
    """Cell line class that manages the cells in the game."""

    def __init__(
        self,
        hexagon_grid: HexagonGrid,
        game_state: GameState,
        screen_size: tuple[int, int],
    ) -> None:
        self.cells = self._create_cells(hexagon_grid, game_state, screen_size)

    def update_cell_radius(self, hexagon_grid: HexagonGrid) -> None:
        """Updates the radius of all cells in the cell line.

        Args:
            hexagon_grid (HexagonGrid): The hexagonal grid containing the cells.
        """

        for cell in self.cells.values():
            cell.update_radius(hexagon_grid.minimal_radius)

    def _create_cells(
        self,
        hexagon_grid: HexagonGrid,
        game_state: GameState,
        screen_size: tuple[int, int],
    ) -> dict[tuple[int, int], Cell]:
        """Creates a cell line on given hexagon grid.

        Args:
            hexagon_grid (HexagonGrid): The hexagonal grid to create cells on.
            game_state (GameState): The game state containing the current game parameters.
            screen_size (tuple[int, int]): The size of the screen.

        Returns:
            dict[tuple[int, int], Cell]: A dictionary of cells with their coordinates as keys.
        """

        number_cells = min(game_state.number_cells, len(hexagon_grid.hexagons))
        coordinates = self._generate_random_positions(
            hexagon_grid.hexagons, number_cells
        )

        cells = {}
        for i in range(number_cells):
            cell = Cell(
                coordinates[i], game_state, hexagon_grid.minimal_radius, screen_size
            )
            cell.energy_consumption_rate_maximum = self._scale_energy_consumption_rate(
                game_state.cell_energy_consumption_rate_maximum,
                game_state.current_level,
            )
            cells[coordinates[i]] = cell

        return cells

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
            )

            self.cells[cell_coordinate].energy_value /= 2
            daughter_cell.energy_value = self.cells[cell_coordinate].energy_value

            self.cells[daughter_coordinates] = daughter_cell
            hexagon_grid.hexagons[daughter_coordinates].set_highlight()

            return daughter_coordinates

        self.cells[cell_coordinate].growth = False

    def get_biomass(self) -> float:
        """Calculates the total biomass of the cell line.

        Returns:
            float: The total biomass of the cell line.
        """

        return sum(cell.energy_value for cell in self.cells.values())

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
            coordinate_probabilities.append(
                self._gaussian_probability(distance_to_center)
            )

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

    def _gaussian_probability(self, distance, sigma=0.25) -> float:
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
            float: The scaled energy consumption rate."""

        return energy_consumption_rate * (
            0.5 + 0.5 * (current_level / (1 + current_level))
        )

        # TODO how to scale this correctly, in respect to dt!?

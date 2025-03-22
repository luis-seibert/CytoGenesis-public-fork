import random

import numpy
from pygame import Surface

from base_elements.cell import Cell
from base_elements.game_state import GameState
from base_elements.hexagon_tile import HexagonTile


class CellLine:
    def __init__(
        self,
        screen: Surface,
    ) -> None:
        self.screen: Surface = screen

    def create_cells(
        self, hexagons: dict[tuple[int, int], HexagonTile], game_state: GameState
    ) -> dict[tuple[int, int], Cell]:
        """Creates a cell line of n-cells on given hexagons"""

        # Clip number_cells to number of hexagons
        if game_state.number_cells > len(hexagons):
            level_number_cells = len(hexagons)
        else:
            level_number_cells = game_state.number_cells

        cells_coordinates = self.generate_random_positions(
            hexagons, level_number_cells
        )  # generate random skew coordinates for cells

        cells = {}
        for i in range(level_number_cells):
            cell_coordinates = cells_coordinates[i]
            cell = Cell(self.screen, cell_coordinates, game_state)
            cell.game_state.cell_energy_consumption_rate_maximum = (
                cell.game_state.cell_energy_consumption_rate_maximum
                * (
                    0.5
                    + 0.5 * (game_state.current_level / (1 + game_state.current_level))
                )
            )
            cells[cell_coordinates] = cell

            hexagons[cell_coordinates].cell_on_hexagon = cell

        return cells

    def replicate_cell(
        self,
        cell: Cell,
        cells,
        hexagons: dict[tuple[int, int], HexagonTile],
        game_state: GameState,
    ):
        """Replicates given mature cell, alters the parent and adds daughter cell"""

        # Get neighbouring hex tiles
        all_neighbours_coordinates = self.calculate_hexagon_neighbours(
            cell.center_axial
        )

        valid_neighbour_coordinates = [
            neighbour_coordinate
            for neighbour_coordinate in all_neighbours_coordinates
            if neighbour_coordinate in hexagons
            and not hexagons[neighbour_coordinate].cell_on_hexagon
        ]

        if valid_neighbour_coordinates:
            # Clone daughter cell into random free hexagon
            daughter_hexagon_coordinates = random.choice(valid_neighbour_coordinates)
            new_cell = Cell(
                self.screen,
                hexagons[daughter_hexagon_coordinates].coordinate_axial,
                game_state,
            )
            new_cell.energy = cell.energy / 2
            cells[daughter_hexagon_coordinates] = new_cell
            hexagons[daughter_hexagon_coordinates].cell_on_hexagon = new_cell

            # Highlight new hexagon
            hexagons[daughter_hexagon_coordinates].highlight = True

            # Half mother cell energy
            cell.energy = cell.energy / 2

        else:
            cell.growth = False  # growth arrest

        return cells, hexagons

    def gaussian_probability(self, dist, sigma=0.25):
        """Calculate gaussian probability from distance with given std_dev = sigma"""

        coeff = 1 / (sigma * numpy.sqrt(2 * numpy.pi))
        exponent = numpy.exp(-(dist**2) / (2 * sigma**2))
        return coeff * exponent

    def generate_random_positions(
        self, hexagons: dict[tuple[int, int], HexagonTile], number_cells: int
    ):
        """Creates n random cell positions with a Gaussian distribution around central hexagon"""

        coords, probabilities = [], []

        # Calculate probabilities from distance to center
        for hex_key in hexagons:
            distance = hexagons[hex_key].distance_to_center
            coords.append(hexagons[hex_key].coordinate_axial)
            probabilities.append(
                self.gaussian_probability(distance)
            )  # Calculate Gaussian prob for each distance

        # Normalize probabilities to sum to 1
        probabilities /= numpy.array(probabilities).sum()

        # Clip no_cells to number of hexagons
        if number_cells > len(hexagons):
            number_cells = len(hexagons)

        selected_indices = numpy.random.choice(
            len(coords), size=number_cells, replace=False, p=probabilities
        )

        return [coords[i] for i in selected_indices]

    def calculate_hexagon_neighbours(self, center: tuple[int, int]):
        """Calculates neighbouring tiles relative to center"""

        r, q = center

        return [
            (-1 + r, 0 + q),
            (-1 + r, 1 + q),
            (0 + r, -1 + q),
            (0 + r, 1 + q),
            (1 + r, -1 + q),
            (1 + r, 0 + q),
        ]

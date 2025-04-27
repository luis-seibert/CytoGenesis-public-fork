"""Core module for a hexagonal tile in the game.

This module defines the HexagonTile class, which represents a single hexagonal tile in the game.
The class includes methods for updating the nutrient value of the tile, setting highlights, and
managing the tile's visual properties. The nutrient value is updated based on the cell's energy
consumption rate and nutrient affinity, and the class also provides methods for calculating the
tile's vertices and updating the body color based on the nutrient value.
"""

import math

from core_modules.cell import Cell
from core_modules.simulator import update_nutrient_value


class HexagonTile:
    """Flat top hexagon class.

    Args:
        coordinate_axial (tuple[int, int]): The axial coordinates of the hexagon.
        vertices (list[tuple[float, float]]): The vertices of the hexagon.
        nutrient_value (float): The nutrient value of the hexagon.
        default_body_color (list[int]): The default body color of the hexagon.
        highlight_ticks (int): The number of ticks to highlight the hexagon. Defaults to 0.
    """

    def __init__(
        self,
        coordinate_axial: tuple[int, int],
        vertices: list[tuple[float, float]],
        nutrient_value: float,
        default_body_color: list[int],
        highlight_ticks: int = 0,
    ) -> None:
        self.coordinate_axial = coordinate_axial
        self.vertices = vertices
        self.nutrient_value = nutrient_value
        self.highlight_ticks = highlight_ticks

        self.body_color = default_body_color.copy()
        self._update_body_color()

    def update(self, cell: Cell) -> Cell:
        """Updates the nutrient value of the hexagon with mass preservation.

        Args:
            cell (Cell): The cell on the hexagon.

        Returns:
            Cell: The updated cell.
        """

        self.nutrient_value, cell.energy_value, cell.growth = update_nutrient_value(
            nutrient_value=self.nutrient_value,
            energy_value=cell.energy_value,
            growth=cell.growth,
            energy_consumption_rate_maximum=cell.energy_consumption_rate_maximum,
            energy_affinity=cell.energy_affinity,
            division_threshold=cell.division_threshold,
        )

        self._update_highlight_ticks()
        self._update_body_color()

        return cell

    def set_highlight(self, highlight_ticks: int = 15) -> None:
        """Sets the highlight ticks of the hexagon.

        Args:
            highlight_ticks (int): The number of ticks to highlight the hexagon. Defaults to 15.
        """

        self.highlight_ticks = highlight_ticks

    def old_update_nutrient_value(self, cell: Cell) -> Cell:
        """Updates the nutrient value of the hexagon with mass preservation.

        The nutrient value is updated based on the cell's energy consumption rate and nutrient
        affinity with the Monod equation. The cell absorbs only as much nutrient as needed
        without exceeding the division threshold.

        Args:
            cell (Cell): The cell on the hexagon.

        Returns:
            Cell: The updated cell.
        """

        if cell.growth and self.nutrient_value > 0:
            # Monod equation-based uptake
            nutrient_uptake = cell.energy_consumption_rate_maximum * (
                self.nutrient_value / (self.nutrient_value + cell.energy_affinity)
            )

            # Cap uptake to what is actually available
            nutrient_uptake = min(nutrient_uptake, self.nutrient_value)

            # Cap uptake so cell does not exceed division threshold
            max_possible_uptake = cell.division_threshold - cell.energy_value
            nutrient_uptake = min(nutrient_uptake, max_possible_uptake)

            # Update values
            self.nutrient_value -= nutrient_uptake
            cell.energy_value += nutrient_uptake

            # Check if cell can grow
            if math.isclose(self.nutrient_value, 0, abs_tol=0.005):
                self.nutrient_value = 0
                cell.growth = False

        return cell

    def _update_body_color(self) -> None:
        """Updates the body color of the hexagon."""

        self.body_color[1] = round(self.nutrient_value * 255)

    def _update_highlight_ticks(self) -> None:
        """Updates the highlight ticks of the hexagon."""

        if self.highlight_ticks > 0:
            self.highlight_ticks -= 1

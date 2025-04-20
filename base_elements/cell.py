import random

from base_elements.game_state import GameState
from base_elements.utils import calculate_pixel_from_axial


class Cell:
    """Cell class representing a single cell in the game."""

    def __init__(
        self,
        coordinate_axial: tuple[int, int],
        game_state: GameState,
        hexagon_minimal_radius: int,
        screen_size: tuple[int, int],
    ):
        self.coordinate_axial = coordinate_axial
        self.coordinate_pixel = self.calculate_pixel_position(
            screen_size, hexagon_minimal_radius, coordinate_axial
        )
        self.growth = True

        self.energy_affinity = game_state.cell_energy_affinity
        self.default_division_threshold = game_state.cell_division_threshold
        self.division_threshold = game_state.cell_division_threshold
        self.energy_value = min(
            self._calculate_randomized_energy_value(
                game_state.cell_energy_initial, game_state.cell_energy_variation
            ),
            self.division_threshold,
        )
        self.energy_consumption_rate_maximum = (
            game_state.cell_energy_consumption_rate_maximum
        )
        self.update_radius(hexagon_minimal_radius)

    def update_radius(self, hexagon_minimal_radius: int) -> None:
        """Update the cell's visual state parameters.

        Args:
            hexagon_minimal_radius (int): The minimal radius of the hexagon.
        """

        radius_factor = self.energy_value / self.default_division_threshold
        if radius_factor > 1:
            print("glitch")
        self.radius = hexagon_minimal_radius * radius_factor

    def calculate_pixel_position(
        self,
        screen_size: tuple[int, int],
        hexagon_minimal_radius: int,
        coordinate_axial: tuple[int, int],
    ) -> tuple[int, int]:
        """Calculate the pixel position of the cell based on its axial coordinates.

        Args:
            screen_size (tuple[int, int]): The size of the screen.
            hexagon_minimal_radius (int): The minimal radius of the hexagon.
            coordinate_axial (tuple[int, int]): The axial coordinates of the cell.

        Returns:
            tuple[int, int]: The pixel position of the cell on the screen.
        """

        offset = calculate_pixel_from_axial(
            (0, 0), hexagon_minimal_radius, coordinate_axial
        )

        return (
            round(screen_size[0] // 2) + offset[0],
            round(screen_size[1] // 2) + offset[1],
        )

    def _calculate_randomized_energy_value(
        self, initial_energy_value: float, energy_variation: float
    ) -> float:
        """Calculate a randomized energy value based on the initial value and variation.

        Args:
            initial_energy_value (float): The initial energy value.
            energy_variation (float): The variation factor for the energy value.

        Returns:
            float: The randomized energy value."""

        energy_value = initial_energy_value * (
            1 + energy_variation * random.uniform(-1, 1)
        )

        return energy_value

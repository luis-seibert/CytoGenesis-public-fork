"""Core module for the Cell class.

This module defines the Cell class, which represents a single cell in the game.
It includes methods for initializing the cell, calculating its pixel position,
updating its radius, and calculating a randomized energy value.
The Cell class is used to manage the cell's properties, such as its energy value,
growth state, and visual representation on the screen.
"""

import random

from core_modules.game_state import GameState
from core_modules.utils import calculate_pixel_from_axial


class Cell:
    """Cell class representing a single cell in the game.

    Args:
        coordinate_axial (tuple[int, int]): The axial coordinates of the cell.
        game_state (GameState): The game state containing the current game parameters.
        hexagon_minimal_radius (int): The minimal radius of the hexagon.
        screen_size (tuple[int, int]): The size of the screen.
        center_offset (tuple[float, float], optional): Custom center point as fractions of screen
            size. Defaults to (0.5, 0.5).
    """

    def __init__(
        self,
        coordinate_axial: tuple[int, int],
        game_state: GameState,
        hexagon_minimal_radius: int,
        screen_size: tuple[int, int],
        center_offset: tuple[float, float] = (0.5, 0.5),
    ):
        self.coordinate_axial = coordinate_axial
        self.center_offset = center_offset
        self.coordinate_pixel = self.calculate_pixel_position(
            screen_size, hexagon_minimal_radius, coordinate_axial, center_offset
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
        self.energy_consumption_rate_maximum = game_state.cell_energy_consumption_rate_maximum
        self.update_radius(hexagon_minimal_radius)

    def update_radius(self, hexagon_minimal_radius: int) -> None:
        """Update the cell's visual state parameters.

        Args:
            hexagon_minimal_radius (int): The minimal radius of the hexagon.
        """

        radius_factor = self.energy_value / self.default_division_threshold
        self.radius = hexagon_minimal_radius * radius_factor

    def calculate_pixel_position(
        self,
        screen_size: tuple[int, int],
        hexagon_minimal_radius: int,
        coordinate_axial: tuple[int, int],
        center_offset: tuple[float, float] = (0.5, 0.5),
    ) -> tuple[int, int]:
        """Calculate the pixel position of the cell based on its axial coordinates.

        Args:
            screen_size (tuple[int, int]): The size of the screen.
            hexagon_minimal_radius (int): The minimal radius of the hexagon.
            coordinate_axial (tuple[int, int]): The axial coordinates of the cell.
            center_offset (tuple[float, float], optional): Custom center point as fractions of
                screen size. Defaults to (0.5, 0.5).

        Returns:
            tuple[int, int]: The pixel position of the cell on the screen.
        """

        offset = calculate_pixel_from_axial((0, 0), hexagon_minimal_radius, coordinate_axial)

        return (
            round(screen_size[0] * center_offset[0]) + offset[0],
            round(screen_size[1] * center_offset[1]) + offset[1],
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

        energy_value = initial_energy_value * (1 + energy_variation * random.uniform(-1, 1))

        return energy_value

"""Core module for tracking process parameters during colonization phase."""

import math
import time
from typing import Dict, List

from core_modules.cell_line import CellLine
from core_modules.hexagon_grid import HexagonGrid


class ProcessTracker:
    """Lightweight class to track essential process parameters for plotting."""

    def __init__(self) -> None:
        self.start_time: float = time.time()
        self.timestamps: List[float] = []
        self.total_biomass: List[float] = []
        self.growth_rate: List[float] = []
        self.total_substrate: List[float] = []

        self.previous_biomass: float = 0.0
        self.previous_time: float = 0.0

    def update(self, cell_line: CellLine, hexagon_grid: HexagonGrid) -> None:
        """Update the tracked parameters with current game state.

        Args:
            cell_line (CellLine): Current cell line with all cells.
            hexagon_grid (HexagonGrid): The hexagon grid containing nutrient data.
        """

        current_time = time.time() - self.start_time
        current_biomass = cell_line.get_biomass()

        self.timestamps.append(current_time)
        self.total_biomass.append(current_biomass)
        self.total_substrate.append(hexagon_grid.get_total_nutrient())

        if len(self.total_biomass) >= 2:
            window_size = min(5, len(self.total_biomass))

            if window_size >= 2:
                start_idx = max(0, len(self.total_biomass) - window_size)

                start_biomass = self.total_biomass[start_idx]
                end_biomass = current_biomass
                start_time = self.timestamps[start_idx]
                end_time = current_time

                time_diff = end_time - start_time

                if time_diff > 0 and start_biomass > 0 and end_biomass > 0:
                    epsilon = 1e-10
                    biomass_ratio = max(end_biomass / max(start_biomass, epsilon), epsilon)

                    biomass_ratio = max(0.1, min(biomass_ratio, 10.0))

                    growth_rate = math.log(biomass_ratio) / time_diff

                    growth_rate = max(-5.0, min(growth_rate, 5.0))

                    self.growth_rate.append(growth_rate)
                else:
                    self.growth_rate.append(0.0)
            else:
                self.growth_rate.append(0.0)
        else:
            self.growth_rate.append(0.0)

        self.previous_biomass = current_biomass
        self.previous_time = current_time

    def get_data_dict(self) -> Dict[str, List]:
        """Get tracked data as a dictionary.

        Returns:
            Dict[str, List]: Dictionary containing only the plotted parameters.
        """

        return {
            "timestamps": self.timestamps,
            "total_biomass": self.total_biomass,
            "growth_rate": self.growth_rate,
            "total_substrate": self.total_substrate,
        }

    def reset(self) -> None:
        """Reset all tracked data."""

        self.start_time = time.time()
        self.timestamps.clear()
        self.total_biomass.clear()
        self.growth_rate.clear()
        self.total_substrate.clear()
        self.previous_biomass = 0.0
        self.previous_time = 0.0

    def initialize_with_initial_state(self, cell_line, hexagon_grid) -> None:
        """Initialize the tracker with actual initial state from the game.

        Args:
            cell_line: The cell line to get initial biomass from.
            hexagon_grid: The hexagon grid to get initial substrate from.
        """

        self.reset()
        initial_biomass = cell_line.get_biomass()
        initial_substrate = hexagon_grid.get_total_nutrient()

        self.timestamps.append(0.0)
        self.total_biomass.append(initial_biomass)
        self.growth_rate.append(0.0)
        self.total_substrate.append(initial_substrate)
        self.previous_biomass = initial_biomass
        self.previous_time = 0.0

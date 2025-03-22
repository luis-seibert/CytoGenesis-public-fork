import math

import pygame
from pygame import Surface

from base_elements.cell import Cell
from base_elements.utils import calculate_pixel_from_axial


class HexagonTile:

    def __init__(
        self,
        screen: Surface,
        minimal_radius: int,
        coordinate_axial: tuple[int, int],
        distance_to_center: float,
        color: list[int],
        nutrient: float,
        cell_on_hexagon: None | Cell = None,
    ) -> None:
        """Flat top hexagon class"""

        screen_size: tuple[int, int] = screen.get_size()
        screen_width_center = int(round(screen_size[0] / 2))
        screen_height_center = int(round(screen_size[1] / 2))

        self.screen_center: tuple[int, int] = (
            screen_width_center,
            screen_height_center,
        )
        self.minimal_radius: int = minimal_radius
        self.maximal_radius: float = self.compute_maximum_radius()
        self.coordinate_axial: tuple[int, int] = coordinate_axial
        self.color: list[int | float] = list(color)
        self.relative_nutrient: float = nutrient
        self.cell_on_hexagon: None | Cell = cell_on_hexagon
        self.distance_to_center: float = distance_to_center

        self.highlight_offset: int = 2
        self.max_highlight_ticks: int = 15
        self.relative_nutrient_color_index: int = 1

        self.vertices: list[tuple[float, float]] = self.compute_vertices()
        self.highlight_tick: int = 0
        self.highlight: bool = False  # Flag for cell replication on this tile

    def update(self, cell: Cell) -> Cell:
        """Updates tile visuals and cell growth"""
        # qS = qS max * S/(S+Ks)

        if self.highlight_tick > 0:
            self.highlight_tick -= 1

        if cell.growth and not math.isclose(self.relative_nutrient, 0, abs_tol=0.005):
            dNutridt = (
                cell.game_state.cell_energy_consumption_rate_maximum
                * self.relative_nutrient
                / (self.relative_nutrient + cell.game_state.cell_energy_affinity)
            )

            lower = min(dNutridt, self.relative_nutrient)
            upper = min(lower, cell.game_state.cell_division_threshold)
            dNutridt = upper
            self.relative_nutrient -= dNutridt
            self.color[self.relative_nutrient_color_index] = int(
                round(self.relative_nutrient * 255, 0)
            )

            cell.energy += dNutridt

        else:
            cell.growth = False

        return cell

    def compute_maximum_radius(self) -> float:
        """Returns max radius of the hexagon"""

        return self.minimal_radius / (math.sqrt(3) / 2)

    def compute_vertices(self) -> list[tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""

        x_pix, y_pix = calculate_pixel_from_axial(
            self.screen_center, self.minimal_radius, self.coordinate_axial
        )

        vertices = []
        for i in range(6):
            angle = math.radians(30 + 60 * i)  # 60 degrees increments
            x = x_pix + self.maximal_radius * math.cos(angle)
            y = y_pix + self.maximal_radius * math.sin(angle)
            vertices.append((x, y))

        return vertices

    def render(self, screen: Surface, border_colour) -> None:
        """Renders the hexagon on the screen"""

        color = tuple([int(round(val)) for val in self.color])
        pygame.draw.polygon(screen, color, self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    def render_highlight(self, screen: Surface, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""

        self.highlight_tick = self.max_highlight_ticks
        pygame.draw.polygon(screen, self.highlight_colour(), self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    def highlight_colour(self) -> list[int]:
        """Colour of the hexagon tile when rendering highlight"""

        offset = self.highlight_offset * self.highlight_tick

        return list(self._brighten(x, offset) for x in self.color)

    def _brighten(self, x: int | float, y: int | float) -> int:
        return int(round(x + y, 0)) if x + y < 255 else 255

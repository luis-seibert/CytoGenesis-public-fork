from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List
from typing import Tuple
import gen_methods

import pygame


@dataclass
class HexagonTile:
    """Flat top hexagon class"""

    CENTER: Tuple[int, int]   # Center of the screen
    min_radius: float   # minimal radius of hexagon tile
    center_skew: Tuple[int, int]   # position of hexagon in skewed axial coordinates
    colour: List[int, int, int]   # base color value of tile
    nutrient: float   # nutrient value of tile
    cell_hex: None   # cell on the tile
    hex_neighbours: None   # adjacent hex tiles

    highlight_offset: int = 2
    max_highlight_ticks: int = 15

    def __post_init__(self):
        self.max_radius = self.compute_max_radius()
        self.vertices = self.compute_vertices()
        self.highlight_tick = 0
        self.new_cell = False  # Flag for fresh cell replication on this tile
        self.dist = gen_methods.calc_skew_dist((0,0), self.center_skew)

    def update(self, cell):
        """Updates tile visuals"""

        if self.highlight_tick > 0:
            self.highlight_tick -= 1

        if cell.growth and not math.isclose(self.nutrient, 0, abs_tol=0.05):
            dNutridt = cell.CELL_ARGS['NUTCONS'] * self.nutrient / (self.nutrient + cell.CELL_ARGS['NUTAFF'])
            dNutridt = min(self.nutrient, dNutridt)
            self.nutrient -= dNutridt
            self.colour[cell.CELL_ARGS['NUT_COL']] = self.nutrient * 255

            cell.energy += dNutridt

        else:
            cell.growth = False

        return self, cell

    def compute_max_radius(self) -> float:
        """Returns max radius of the hexagon"""

        return self.min_radius / (math.sqrt(3) / 2)

    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""

        x_skew, y_skew = self.center_skew
        x_pix, y_pix = gen_methods.compute_skew_to_pix(CENTER=self.CENTER,
                                                       min_radius=self.min_radius,
                                                       skew_coords=(x_skew, y_skew))

        vertices = []
        for i in range(6):
            angle = math.radians(30 + 60 * i) # 60 degrees increments
            x = x_pix + self.max_radius * math.cos(angle)
            y = y_pix + self.max_radius * math.sin(angle)
            vertices.append((x, y))

        return vertices

    def render(self, screen, border_colour) -> None:
        """Renders the hexagon on the screen"""

        color = tuple([int(round(val)) for val in self.highlight_colour])
        pygame.draw.polygon(screen, color, self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""

        self.highlight_tick = self.max_highlight_ticks
        # pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    @property
    def highlight_colour(self) -> List[int, ...]:
        """Colour of the hexagon tile when rendering highlight"""

        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255

        return list(brighten(x, offset) for x in self.colour)

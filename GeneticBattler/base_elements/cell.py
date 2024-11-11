import os
import random

import pygame
from pygame import Surface

from base_elements.game_state import GameState
from base_elements.utils import calculate_pixel_from_axial, round_to_even


# Define the Cell class
class Cell(pygame.sprite.Sprite):
    def __init__(
        self,
        screen: Surface,
        center_axial: tuple[int, int],
        game_state: GameState,
    ):
        super().__init__()
        self.screen_size: tuple[int, int] = screen.get_size()

        self.game_state: GameState = game_state
        self.center_axial: tuple[int, int] = center_axial
        self.energy: float = self.game_state.cell_energy_initial * (
            1 + self.game_state.cell_energy_variation * random.uniform(-1, 1)
        )

        self.growth = True
        image_path = os.path.join(os.getcwd(), "images", "COCCUS2.png")
        self.image = pygame.image.load(image_path)
        self.rectangle = self.image.get_rect()
        self.rectangle.center = self.center_axial
        self.temporary_image = pygame.image.load(image_path)

    def update(self) -> None:
        """Calculate factor of displayed cell size"""

        relative_size = self.energy / self.game_state.cell_division_threshold
        scaled_size = round_to_even(relative_size * self.game_state.cell_body_size)
        self.image = pygame.transform.scale(
            self.temporary_image, (scaled_size, scaled_size)
        )

        self.rectangle = self.image.get_rect()
        self.rectangle.center = calculate_pixel_from_axial(
            (self.screen_size[0] // 2, self.screen_size[1] // 2),
            int(self.game_state.cell_body_size / 2),
            self.center_axial,
        )

    def render(self, screen: Surface) -> None:
        self.update()
        screen.blit(self.image, self.rectangle)

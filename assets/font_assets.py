import os

import pygame


class FontAssets:
    """Font assets class that loads and manages font assets for the game.

    Args:
        screen_size (tuple[int, int]): The size of the screen.
    """

    def __init__(self, screen_size: tuple[int, int]) -> None:
        pygame.init()
        base_font_size = screen_size[1] / 30  # Scale font size based on screen height
        pixel_font_path = os.path.join(
            os.getcwd(), "assets", "fonts", "Grand9K Pixel.ttf"
        )
        self._load_fonts(base_font_size, pixel_font_path)

    def _load_fonts(self, base_font_size: float, pixel_font_path: str) -> None:
        """Load fonts dynamically based on the base font size."""

        self.huge_font = pygame.font.Font(pixel_font_path, round(base_font_size * 4))
        self.title_font = pygame.font.Font(pixel_font_path, round(base_font_size * 1.5))
        self.large_font = pygame.font.Font(pixel_font_path, round(base_font_size * 1.5))
        self.medium_font = pygame.font.Font(pixel_font_path, round(base_font_size * 1))
        self.medium_small_font = pygame.font.Font(
            pixel_font_path, round(base_font_size)
        )
        self.small_font = pygame.font.Font(pixel_font_path, round(base_font_size * 0.8))

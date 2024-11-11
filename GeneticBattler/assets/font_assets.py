import os

import pygame


class FontAssets:
    pygame.init()
    pixel_font_path = os.path.join(os.getcwd(), "assets", "fonts", "Grand9K Pixel.ttf")

    huge_font = pygame.font.Font(pixel_font_path, 85)
    title_font = pygame.font.Font(pixel_font_path, 40)
    large_font = pygame.font.Font(pixel_font_path, 32)
    medium_font = pygame.font.Font(pixel_font_path, 25)
    small_font = pygame.font.Font(pixel_font_path, 16)

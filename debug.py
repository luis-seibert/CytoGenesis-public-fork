import pygame

pygame.init()
import os


root_path = os.getcwd()
print(root_path)


pixel_font_path = os.path.join(root_path, "fonts", "Grand9K Pixel.ttf")
# os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

huge_font = pygame.font.Font(pixel_font_path, 85)

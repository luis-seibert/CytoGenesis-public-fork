import pygame
from pygame import Surface
from pygame.time import Clock

from assets.colors import Colors
from assets.font_assets import FontAssets
from assets.image_assets import ImageAssets
from base_elements.game_state import GameState
from game_phases.main_menu import MainMenu

# PYGAME INITIALIZATION #
pygame.init()
pygame.display.set_caption("CytoGenesis")  # window title
windowed_screen_size = (1024, 576)

colors: Colors = Colors()
screen: Surface = pygame.display.set_mode(windowed_screen_size)
clock: Clock = pygame.time.Clock()
font_assets: FontAssets = FontAssets()
image_assets: ImageAssets = ImageAssets(windowed_screen_size)
game_state: GameState = GameState(screen_size=windowed_screen_size)


main_menu: MainMenu = MainMenu(
    screen,
    clock,
    font_assets,
    image_assets,
    game_state,
    colors,
)


main_menu.run_main_menu()

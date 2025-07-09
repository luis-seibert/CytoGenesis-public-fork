import pygame
from pygame.time import Clock

from core_modules.game_state import GameState
from core_modules.render_manager import RenderManager
from game_phases.main_menu import MainMenu


def run_game() -> None:
    """Main game loop that initializes Pygame and runs the game."""

    pygame.init()
    pygame.display.set_caption("CytoGenesis")

    clock: Clock = pygame.time.Clock()
    game_state = GameState()
    desktop_sizes = pygame.display.get_desktop_sizes()
    render_manager = RenderManager(
        initial_screen_size=desktop_sizes[0] if desktop_sizes else (800, 600),
        full_screen=game_state.full_screen,
    )

    try:
        MainMenu(clock, game_state, render_manager).run_main_menu()
    finally:
        pygame.quit()


if __name__ == "__main__":
    run_game()

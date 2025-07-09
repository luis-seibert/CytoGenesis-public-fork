"""
CytoGenesis - Bioprocess Engineering Game

A strategic simulation game that combines cellular biology with bioprocess engineering principles.
This educational game demonstrates microbial growth dynamics using Monod kinetics and challenges
players to optimize reactor conditions for maximum biomass yield.

Features:
    - Real-time simulation of cellular growth and nutrient consumption
    - Hexagonal grid-based strategic gameplay
    - Scientific accuracy with Monod kinetics modeling
    - Progressive difficulty with reactor mixing challenges
    - Educational value for bioprocess engineering concepts

Architecture:
    - Core simulation engine with Numba optimization
    - Modular game phases for different gameplay modes
    - Asset management system for graphics and configuration
    - Clean separation of game logic, rendering, and user interface

Author: Luis Seibert
"""

import pygame
from pygame.time import Clock

from core_modules.game_state import GameState
from core_modules.render_manager import RenderManager
from game_phases.main_menu import MainMenu


def run_game() -> None:
    """
    Main game loop that initializes Pygame and runs the game.

    This function sets up the game environment, initializes all necessary components,
    and starts the main menu. It handles the complete game lifecycle from startup
    to shutdown, ensuring proper resource cleanup.

    Game Flow:
        1. Initialize Pygame and display systems
        2. Set up game state and render manager
        3. Configure display based on system capabilities
        4. Launch main menu and handle game phases
        5. Clean up resources on exit

    Raises:
        pygame.error: If Pygame initialization fails
        SystemError: If display initialization fails
    """

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

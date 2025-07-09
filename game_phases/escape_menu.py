"""Escape menu for the game phases.

This module contains the EscapeMenu class which handles the escape menu functionality
that can be triggered during colonization and shop phases. It provides options to
access settings, return to main menu, or quit the game.
"""

from enum import Enum

import pygame
from pygame.time import Clock

from core_modules import event_handler
from core_modules.game_state import GameState
from core_modules.render_manager import RenderManager
from game_phases.settings_menu import SettingsMenu


class EscapeMenuOption(Enum):
    """Enumeration for escape menu options."""

    RESUME = 0
    SETTINGS = 1
    MAIN_MENU = 2
    QUIT = 3


class EscapeMenuResult(Enum):
    """Enumeration for escape menu results."""

    RESUME = "resume"
    MAIN_MENU = "main_menu"
    QUIT = "quit"


class EscapeMenu:
    """Escape menu class that handles the pause menu during game phases.

    Args:
        clock (Clock): The clock to manage the game loop.
        render_manager (RenderManager): The render manager to handle rendering.
        hexagon_grid: The hexagon grid for the settings menu.
    """

    def __init__(
        self,
        clock: Clock,
        render_manager: RenderManager,
        background_hexagon_grid,
    ) -> None:
        self.clock: Clock = clock
        self.render_manager: RenderManager = render_manager
        self.background_hexagon_grid = background_hexagon_grid
        self.selected_option: int = 0
        self.options = ["Resume", "Settings", "Main Menu", "Quit"]

        # Initialize settings menu with the provided background grid
        self.settings_menu: SettingsMenu = SettingsMenu(
            self.clock, self.render_manager, self.background_hexagon_grid
        )

    def show_escape_menu(self, game_state: GameState) -> EscapeMenuResult:
        """Display the escape menu and handle user input.

        Args:
            game_state (GameState): The current game state.

        Returns:
            EscapeMenuResult: The action chosen by the user.
        """
        while True:
            for event in pygame.event.get():
                event_handler.handle_quit(event)

                if event_handler.handle_escape(event):
                    return EscapeMenuResult.RESUME

                self.selected_option = event_handler.handle_option_navigation(
                    event,
                    self.selected_option,
                    len(self.options),
                )

                if event_handler.handle_option_selection(event):
                    if self.selected_option == EscapeMenuOption.RESUME.value:
                        return EscapeMenuResult.RESUME
                    elif self.selected_option == EscapeMenuOption.SETTINGS.value:
                        updated_game_state = self.settings_menu.run_settings_menu(game_state)
                        game_state = updated_game_state  # Update game state from settings
                        # Continue the loop to return to escape menu after settings
                    elif self.selected_option == EscapeMenuOption.MAIN_MENU.value:
                        return EscapeMenuResult.MAIN_MENU
                    elif self.selected_option == EscapeMenuOption.QUIT.value:
                        return EscapeMenuResult.QUIT

            self._render_escape_menu(game_state)

    def _render_escape_menu(self, game_state: GameState) -> None:
        """Render the escape menu with game-consistent styling.

        Args:
            game_state (GameState): The current game state.
        """

        # Render the background hexagon grid (like main menu and settings)
        self.render_manager.render_hexagons(self.background_hexagon_grid)

        # Add shadow overlay for consistency with main menu and settings
        self.render_manager.render_shadow_overlay(color="black", alpha=60)

        # Game is paused header
        self.render_manager.render_text(
            "GAME PAUSED",
            "huge_font",
            "white",
            {"center": (0.5, 0.25)},
        )

        # Menu options using the render_manager's render_options method for consistency
        self.render_manager.render_options(
            option_items=self.options,
            selected_option=self.selected_option,
            font_name="title_font",
            position_args={"center": (0.5, 0.5)},
            distance_between_options=0.075,
            highlight_color="white",
            option_color="black",
        )

        self.render_manager.update_screen(game_state, self.clock)

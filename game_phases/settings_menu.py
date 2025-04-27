"""Game phase for the settings menu of the game.

This phase allows the player to adjust game settings such as the number of levels, show FPS,
and toggle fullscreen mode. It includes rendering the settings menu and handling user input.
"""

import pygame
from pygame.time import Clock

from core_modules import event_handler
from core_modules.game_state import GameState
from core_modules.hexagon_grid import HexagonGrid
from core_modules.render_manager import RenderManager


class SettingsMenu:
    """Settings menu class that manages the settings menu of the game.

    Args:
        clock (Clock): The clock to manage the game loop.
        render_manager (RenderManager): The render manager to handle rendering.
        hexagon_grid (HexagonGrid): The hexagon grid for rendering the background.
    """

    def __init__(
        self, clock: Clock, render_manager: RenderManager, hexagon_grid: HexagonGrid
    ) -> None:
        self.clock: Clock = clock
        self.render_manager: RenderManager = render_manager
        self.hexagon_grid: HexagonGrid = hexagon_grid

        self.menu_options: list[str] = [
            "Number of levels",
            "Show FPS",
            "Fullscreen",
        ]
        self.selected_option: int = 0
        self.secondary_option_selected: bool = False
        self.full_screen_toggled: bool = False

    def run_settings_menu(self, game_state: GameState) -> GameState:
        """Main loop for the settings menu.

        Args:
            game_state (GameState): The current game state.

        Returns:
            GameState: The updated game state after settings changes.
        """

        while True:
            for event in pygame.event.get():
                event_handler.handle_quit(event)

                if self.secondary_option_selected:
                    if self.selected_option == 0:  # Number of levels
                        game_state.default_number_levels = (
                            event_handler.handle_change_option_value_with_circling(
                                event,
                                game_state.default_number_levels,
                                game_state.max_number_levels,
                                1,  # At least one level is required to be played
                            )
                        )
                    elif self.selected_option == 1:  # Toggle show fps
                        game_state.show_fps = event_handler.handle_change_bool_option(
                            event, game_state.show_fps
                        )
                    elif self.selected_option == 2:  # Toggle fullscreen
                        game_state.full_screen = event_handler.handle_change_bool_option(
                            event, game_state.full_screen
                        )
                        self.full_screen_toggled = event_handler.handle_change_bool_option(
                            event, self.full_screen_toggled
                        )

                else:
                    self.selected_option = event_handler.handle_option_navigation(
                        event, self.selected_option, len(self.menu_options)
                    )
                    if self.full_screen_toggled:
                        self.render_manager.toggle_full_screen(game_state.full_screen)
                        self.hexagon_grid.update_hexagon_vertices(
                            game_state, self.render_manager.current_screen_size
                        )
                        self.full_screen_toggled = False
                    if event_handler.handle_escape(event):
                        return game_state

                self.secondary_option_selected = event_handler.handle_secondary_option_selection(
                    event, self.secondary_option_selected
                )

            self._render_settings(game_state)

    def _render_menu_options(self, option_values: list) -> None:
        """Helper method to render menu options and their values.

        Args:
            option_values (list): The values of the options to be rendered.
        """

        option_distance = 0.075

        if self.secondary_option_selected:
            self.render_manager.render_options(
                self.menu_options,
                None,
                "title_font",
                {
                    "topleft": (
                        0.1,
                        0.25,
                    )
                },
                distance_between_options=option_distance,
                highlight_color="white",
                option_color="black",
            )
            self.render_manager.render_options(
                option_values,
                self.selected_option,
                "title_font",
                {
                    "topright": (
                        0.9,
                        0.25,
                    )
                },
                distance_between_options=option_distance,
                highlight_color="white",
                option_color="black",
            )
        else:
            self.render_manager.render_options(
                self.menu_options,
                self.selected_option,
                "title_font",
                {
                    "topleft": (
                        0.1,
                        0.25,
                    )
                },
                distance_between_options=option_distance,
                highlight_color="white",
                option_color="black",
            )
            self.render_manager.render_options(
                option_values,
                None,
                "title_font",
                {
                    "topright": (
                        0.9,
                        0.25,
                    )
                },
                distance_between_options=option_distance,
                highlight_color="white",
                option_color="black",
            )

    def _render_settings(self, game_state: GameState) -> None:
        """Renders the settings menu.

        Args:
            game_state (GameState): The current game state.
        """

        # Background hexagons
        self.render_manager.render_hexagons(self.hexagon_grid)

        # Shadow overlay
        self.render_manager.render_shadow_overlay(color="black", alpha=60)

        # Title
        self.render_manager.render_text(
            "Settings",
            "title_font",
            "white",
            {
                "center": (
                    0.5,
                    0.1,
                )
            },
        )

        # Settings menu options
        settings_menu_option_values = [
            game_state.default_number_levels,
            game_state.show_fps,
            game_state.full_screen,
        ]

        # Menu options and their values
        self._render_menu_options(settings_menu_option_values)

        self.render_manager.update_screen(game_state, self.clock)

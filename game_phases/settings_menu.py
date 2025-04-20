import pygame
from pygame.time import Clock

from base_elements import event_handler
from base_elements.game_state import GameState
from base_elements.hexagon_grid import HexagonGrid
from base_elements.render_manager import RenderManager


class SettingsMenu:
    """Settings menu class that manages the settings menu of the game."""

    def __init__(
        self, clock: Clock, render_manager: RenderManager, hexagon_grid: HexagonGrid
    ) -> None:
        self.clock = clock
        self.render_manager = render_manager
        self.hexagon_grid = hexagon_grid

        self.menu_options: list[str] = [
            "Number of levels",
            "Size of Inoculum",
            "Show FPS",
            "Fullscreen",
        ]
        self.selected_option = 0
        self.secondary_option_selected = False
        self.full_screen_toggled = False

    def run_settings_menu(self, game_state: GameState) -> GameState:
        """Main loop for the settings menu.

        Args:
            game_state (GameState): The current game state.
        Returns:
            GameState: The updated game state after settings changes."""

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
                                1,  # At least one level is required
                            )
                        )
                    elif self.selected_option == 1:  # Number of initial cells
                        game_state.default_number_cells = (
                            event_handler.handle_change_option_value_with_circling(
                                event,
                                game_state.default_number_cells,
                                game_state.max_number_initial_cells,
                                1,  # At least one cell is required
                            )
                        )
                    elif self.selected_option == 2:  # Show fps
                        game_state.show_fps = event_handler.handle_change_bool_option(
                            event, game_state.show_fps
                        )
                    elif self.selected_option == 3:  # Toggle fullscreen
                        game_state.full_screen = (
                            event_handler.handle_change_bool_option(
                                event, game_state.full_screen
                            )
                        )
                        self.full_screen_toggled = (
                            event_handler.handle_change_bool_option(
                                event, self.full_screen_toggled
                            )
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

                self.secondary_option_selected = (
                    event_handler.handle_secondary_option_selection(
                        event, self.secondary_option_selected
                    )
                )

            self.render_settings(game_state)

    def render_settings(self, game_state: GameState) -> None:
        """Renders the settings menu.

        Args:
            game_state (GameState): The current game state.
        """

        self.render_manager.render_hexagons(self.hexagon_grid)
        self.render_manager.render_shadow_overlay(color="black", alpha=100)
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

        settings_menu_option_values = [
            game_state.default_number_levels,
            game_state.default_number_cells,
            game_state.show_fps,
            game_state.full_screen,
        ]

        self._render_menu_options(settings_menu_option_values)

        self.render_manager.render_fps(game_state, self.clock, "small_font")
        pygame.display.flip()
        self.clock.tick(game_state.fps_maximum)

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

import sys

import pygame
from pygame import Surface
from pygame.time import Clock

from assets.colors import Colors
from assets.font_assets import FontAssets
from assets.image_assets import ImageAssets
from base_elements.game_state import GameState
from base_elements.hexagon_grid import HexagonGrid
from base_elements.utils import display_fps
from utils import event_handler


class SettingsMenu:
    def __init__(
        self,
        screen: Surface,
        clock: Clock,
        font_assets: FontAssets,
        image_assets: ImageAssets,
        colors: Colors,
    ) -> None:
        pygame.init()

        self.screen: Surface = screen
        self.clock: Clock = clock
        self.font_assets: FontAssets = font_assets
        self.image_assets: ImageAssets = image_assets
        self.colors: Colors = colors

        self.screen_size: tuple[int, int] = screen.get_size()

        self.menu_options: list[str] = [
            "Number of levels",
            "Size of Inoculum",
            "Show FPS",
        ]
        self.selected_option: int = 0
        self.secondary_option_selected: bool = False

    def run_settings_menu(self, game_state: GameState) -> GameState:
        """Runs the settings menu."""

        # Create hexagon grid for settings menu
        hexagon_grid = HexagonGrid(game_state, self.screen)
        self.settings_menu_hexagons = hexagon_grid.main_menu_grid()
        for coordinate in self.settings_menu_hexagons:
            hexagon_nutrient_color = self.settings_menu_hexagons[coordinate].color[
                game_state.default_hexagon_nutrient_color_index
            ]
            hexagon_nutrient_color = min(hexagon_nutrient_color + 110, 255)
            self.settings_menu_hexagons[coordinate].color[
                game_state.default_hexagon_nutrient_color_index
            ] = hexagon_nutrient_color

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
                else:
                    self.selected_option = event_handler.handle_option_navigation(
                        event, self.selected_option, len(self.menu_options)
                    )
                    if event_handler.handle_escape(event):
                        return game_state

                self.secondary_option_selected = (
                    event_handler.handle_secondary_option_selection(
                        event, self.secondary_option_selected
                    )
                )

            self.render_settings(
                game_state, self.selected_option, self.secondary_option_selected
            )

    def render_settings(
        self,
        game_state: GameState,
        selected_option: int,
        secondary_option_selected: bool,
    ):
        """Renders the options menu"""

        global frame_count

        # Render background
        self.screen.blit(
            self.image_assets.colonization_phase_background,
            self.image_assets.colonization_phase_background_rectangle,
        )

        # Render background hexagons
        for hexagon in self.settings_menu_hexagons.values():
            hexagon.render(self.screen, self.colors.black)

        # Shade overlay
        game_over_screen_fade = pygame.Surface(self.screen.get_size())
        game_over_screen_fade.fill((0, 0, 0))
        game_over_screen_fade.set_alpha(60)
        self.screen.blit(game_over_screen_fade, (0, 0))

        # Render the title
        title_text = self.font_assets.title_font.render(
            "Settings", True, self.colors.black
        )
        title_rect = title_text.get_rect(
            center=(self.screen_size[0] // 2, self.screen_size[1] // 10)
        )
        self.screen.blit(title_text, title_rect)

        # Render the settings menu options
        for i, option in enumerate(self.menu_options):
            color = (
                self.colors.orange
                if i == selected_option and not secondary_option_selected
                else self.colors.gray
            )
            option_text = self.font_assets.title_font.render(option, True, color)
            option_rect = option_text.get_rect(
                topleft=(self.screen_size[0] // 10, self.screen_size[1] // 4 + i * 50)
            )
            self.screen.blit(option_text, option_rect)

        # Render the settings menu option values
        settings_menu_option_values = [
            game_state.default_number_levels,
            game_state.default_number_cells,
            game_state.show_fps,
        ]

        for i, option in enumerate(settings_menu_option_values):
            color = (
                self.colors.orange
                if i == selected_option and secondary_option_selected
                else self.colors.gray
            )
            option_text = self.font_assets.title_font.render(str(option), True, color)
            option_rect = option_text.get_rect(
                topright=(
                    self.screen_size[0] - self.screen_size[0] // 10,
                    self.screen_size[1] // 4 + i * 50,
                )
            )
            self.screen.blit(option_text, option_rect)

        # Display FPS
        if game_state.show_fps:
            display_fps(
                self.screen, self.font_assets.small_font, self.clock, self.colors.black
            )

        # Update display
        pygame.display.flip()  # Update the display

        # Cap frame rate
        self.clock.tick(game_state.fps_maximum)
        # self.frame_count += 1

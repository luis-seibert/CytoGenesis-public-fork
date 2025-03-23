# import random
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
from game_phases.colonization_phase import ColonizationPhase
from game_phases.final_screen import FinalScreen
from game_phases.settings_menu import SettingsMenu
from game_phases.shop_phase import ShopPhase
from utils import event_handler


class MainMenu:
    """Main menu class that handles the main menu of the game."""

    def __init__(
        self,
        screen: Surface,
        clock: Clock,
        font_assets: FontAssets,
        image_assets: ImageAssets,
        game_state: GameState,
        colors: Colors,
    ) -> None:
        self.screen: Surface = screen
        self.clock: Clock = clock
        self.image_assets: ImageAssets = image_assets
        self.font_assets: FontAssets = font_assets
        self.game_state: GameState = game_state
        self.colors: Colors = colors

        self.screen_size: tuple[int, int] = screen.get_size()

        self.menu_options: list[str] = ["Start Game", "Settings", "Quit"]
        self.selected_option: int = 0

        self.settings_menu = SettingsMenu(
            self.screen,
            self.clock,
            self.font_assets,
            self.image_assets,
            self.colors,
        )

        self.colonization_phase = ColonizationPhase(
            self.screen,
            self.clock,
            self.font_assets,
            self.image_assets,
            self.colors,
        )

        self.shop_phase = ShopPhase(
            self.screen,
            self.clock,
            self.font_assets,
            self.image_assets,
            self.colors,
        )

        self.final_screen = FinalScreen(
            self.screen,
            self.clock,
            self.font_assets,
            self.image_assets,
            self.colors,
        )

        self.hexagon_grid = HexagonGrid(self.game_state, self.screen)
        self.frame_count = 0

    def run_main_menu(self) -> None:
        """Run main menu with options to choose from."""

        # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.main_menu_hexagons = self.hexagon_grid.main_menu_grid()
        for coordinate in self.main_menu_hexagons:
            hexagon_nutrient_color = self.main_menu_hexagons[coordinate].color[
                self.game_state.default_hexagon_nutrient_color_index
            ]
            hexagon_nutrient_color = min(hexagon_nutrient_color + 110, 255)
            self.main_menu_hexagons[coordinate].color[
                self.game_state.default_hexagon_nutrient_color_index
            ] = hexagon_nutrient_color

        while True:
            for event in pygame.event.get():
                event_handler.handle_quit(event)

                self.selected_option = event_handler.handle_option_navigation(
                    event, self.selected_option, len(self.menu_options)
                )

                if event_handler.handle_option_selection(event):
                    if self.selected_option == 0:  # Start game
                        self.start_game()
                        self.run_main_menu()
                    elif self.selected_option == 1:  # Settings menu
                        self.game_state = self.settings_menu.run_settings_menu(
                            self.game_state
                        )
                    elif self.selected_option == 2:  # Quit game
                        pygame.quit()
                        sys.exit()

            self.render_main_menu()

    def render_main_menu(self) -> None:
        """Render main menu."""

        # Render background
        self.screen.blit(
            self.image_assets.colonization_phase_background,
            self.image_assets.colonization_phase_background_rectangle,
        )

        # Render background hexagons
        for hexagon in self.main_menu_hexagons.values():
            """
            if self.frame_count % 1 == 0:  # TODO HOW???
                if (
                    hexagon.color[self.game_state.default_hexagon_nutrient_color_index]
                    >= 200
                ):
                    self.oscillation_increase = False
                elif (
                    hexagon.color[self.game_state.default_hexagon_nutrient_color_index]
                    <= 120
                ):
                    self.oscillation_increase = True
                if self.oscillation_increase:
                    hexagon.color[
                        self.game_state.default_hexagon_nutrient_color_index
                    ] += (hexagon.distance_to_center * random.randint(1, 3) * 0.01)
                    hexagon.color[
                        self.game_state.default_hexagon_nutrient_color_index
                    ] = min(
                        hexagon.color[
                            self.game_state.default_hexagon_nutrient_color_index
                        ],
                        255,
                    )
                else:
                    hexagon.color[
                        self.game_state.default_hexagon_nutrient_color_index
                    ] -= (random.randint(1, 3) * 0.01)
                    hexagon.color[
                        self.game_state.default_hexagon_nutrient_color_index
                    ] = max(
                        hexagon.color[
                            self.game_state.default_hexagon_nutrient_color_index
                        ],
                        0,
                    )
            """

            hexagon.render(self.screen, self.colors.black)

        # Shade overlay
        game_over_screen_fade = pygame.Surface(self.screen.get_size())
        game_over_screen_fade.fill((0, 0, 0))
        game_over_screen_fade.set_alpha(60)
        self.screen.blit(game_over_screen_fade, (0, 0))

        # Render the title
        title_text = self.font_assets.huge_font.render(
            "CytoGenesis", True, self.colors.white
        )
        title_rect = title_text.get_rect(
            center=(self.screen_size[0] // 2, self.screen_size[1] // 4)
        )
        self.screen.blit(title_text, title_rect)

        # Render the menu options
        for i, option in enumerate(self.menu_options):
            color = (
                self.colors.white if i == self.selected_option else self.colors.black
            )
            option_text = self.font_assets.title_font.render(option, True, color)
            option_rect = option_text.get_rect(
                center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + i * 50)
            )
            self.screen.blit(option_text, option_rect)

        # Display FPS
        if self.game_state.show_fps:
            display_fps(
                self.screen,
                self.font_assets.small_font,
                self.clock,
                self.colors.black,
            )

        # Update display
        pygame.display.flip()

        # Cap frame rate
        self.clock.tick(self.game_state.fps_maximum)
        self.frame_count += 1

    def start_game(self):
        """Start the game."""

        self.game_state.reset()

        # Main game loop
        for iteration in range(self.game_state.number_levels):
            self.game_state.current_level = iteration
            self.colonization_phase.run_colonization_phase(
                self.game_state,
            )
            if iteration < self.game_state.number_levels - 1:
                self.game_state = self.shop_phase.run_shop_phase(self.game_state)

        # Final overall points display
        self.final_screen.run_final_screen(self.game_state)

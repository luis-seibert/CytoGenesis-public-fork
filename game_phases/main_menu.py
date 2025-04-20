import sys

import pygame
from pygame.time import Clock

from base_elements import event_handler
from base_elements.game_state import GameState
from base_elements.hexagon_grid import HexagonGrid
from base_elements.hexagon_tile import HexagonTile
from base_elements.player_data_manager import load_player_name, save_player_name
from base_elements.render_manager import RenderManager
from game_phases.colonization_phase import ColonizationPhase
from game_phases.final_screen import FinalScreen
from game_phases.settings_menu import SettingsMenu
from game_phases.shop_phase import ShopPhase


class MainMenu:
    """Main menu class that handles the main menu of the game."""

    def __init__(
        self,
        clock: Clock,
        game_state: GameState,
        render_manager: RenderManager,
    ) -> None:
        self.clock: Clock = clock
        self.game_state: GameState = game_state
        self.render_manager: RenderManager = render_manager

        self.menu_options: list[str] = ["Start Game", "Change Name", "Settings", "Quit"]
        self.selected_option: int = 0

        self.hexagon_grid = HexagonGrid(
            self.game_state, self.render_manager.current_screen_size
        )
        self.hexagon_grid.hexagons = self._create_background_hexagon_grid()

        self.settings_menu = SettingsMenu(
            self.clock, self.render_manager, self.hexagon_grid
        )

        self.colonization_phase = ColonizationPhase(
            self.clock,
            self.render_manager,
        )

        self.shop_phase = ShopPhase(
            self.clock,
            self.render_manager,
        )

        self.final_screen = FinalScreen(
            self.clock,
            self.render_manager,
        )

        # Load or prompt for player name
        self.player_name = load_player_name()
        if not self.player_name:
            self.player_name = self._prompt_for_name()
            save_player_name(self.player_name)

    def run_main_menu(self) -> None:
        """Run main menu with options to choose from."""

        while True:
            for event in pygame.event.get():
                event_handler.handle_quit(event)

                self.selected_option = event_handler.handle_option_navigation(
                    event, self.selected_option, len(self.menu_options)
                )

                if event_handler.handle_option_selection(event):
                    if self.selected_option == 0:  # Start game
                        self._start_game()
                        self.run_main_menu()
                    elif self.selected_option == 1:  # Change Name
                        self.player_name = self._prompt_for_name()
                        save_player_name(self.player_name)
                    elif self.selected_option == 2:  # Settings menu
                        self.game_state = self.settings_menu.run_settings_menu(
                            self.game_state
                        )
                    elif self.selected_option == 3:  # Quit game
                        pygame.quit()
                        sys.exit()

            self._render_main_menu()

    def _start_game(self):
        """Start the game and iterate over levels."""

        self.game_state.reset()

        for iteration in range(self.game_state.number_levels):  # Main game loop
            self.game_state.current_level = iteration
            self.colonization_phase.run_colonization_phase(
                self.game_state,
            )
            if iteration < self.game_state.number_levels - 1:
                self.game_state = self.shop_phase.run_shop_phase(self.game_state)

        self.final_screen.run_final_screen(self.game_state)

    def _create_background_hexagon_grid(self) -> dict[tuple[int, int], HexagonTile]:
        """Create a grid of hexagons for the main menu.

        Returns:
            dict[tuple[int, int], HexagonTile]: Dictionary of hexagons with coordinates as keys.
        """

        screen_width, screen_height = self.render_manager.current_screen_size
        number_r_hexagons = (
            round(screen_width / self.hexagon_grid.maximal_radius / 2) + 20
        )
        number_q_hexagons = (
            round(screen_height / self.hexagon_grid.minimal_radius / 2) + 5
        )

        coordinates = []
        r_offset = -round(number_r_hexagons / 2)
        q_offset = -round(number_q_hexagons / 2)
        for r in range(number_r_hexagons):
            for q in range(number_q_hexagons):
                coordinates.append((r_offset + r, q_offset + q))

        hexagons = {}
        for coordinate in coordinates:
            hexagons[coordinate] = self.hexagon_grid.create_hexagon(
                coordinate,
                self.game_state.hexagon_nutrient_variation,
                self.game_state.hexagon_nutrient_richness,
            )

        return hexagons

    def _render_main_menu(self) -> None:
        """Render the main menu screen with hexagons and options."""

        self.render_manager.render_hexagons(self.hexagon_grid)
        self.render_manager.render_shadow_overlay(color="black", alpha=60)

        # Title
        self.render_manager.render_text(
            "CytoGenesis",
            "huge_font",
            "white",
            {"center": (0.5, 0.25)},
        )

        # Main menu options
        self.render_manager.render_options(
            option_items=self.menu_options,
            selected_option=self.selected_option,
            font_name="title_font",
            position_args={"center": (0.5, 0.5)},
            distance_between_options=0.075,
        )

        self.render_manager.render_text(
            f"Player: {self.player_name}",
            "small_font",
            "white",
            {"topleft": (0.02, 0.02)},
        )

        self.render_manager.render_fps(self.game_state, self.clock, "small_font")

        pygame.display.flip()
        self.clock.tick(self.game_state.fps_maximum)

    def _prompt_for_name(self) -> str:
        """Display prompt to enter player name."""

        input_name = ""
        entering = True

        while entering:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_name.strip():
                        entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_name = input_name[:-1]
                    elif event.unicode.isprintable():
                        input_name += event.unicode

            self.render_manager.render_background("very_light_gray")
            self.render_manager.render_text(
                "Enter your name:",
                "title_font",
                "black",
                {"center": (0.5, 0.4)},
            )
            self.render_manager.render_text(
                input_name + "|",
                "title_font",
                "black",
                {"center": (0.5, 0.5)},
            )
            self.render_manager.render_text(
                "Press Enter to confirm.",
                "small_font",
                "black",
                {"center": (0.5, 0.6)},
            )

            pygame.display.flip()
            self.clock.tick(self.game_state.fps_maximum)

        return input_name.strip()

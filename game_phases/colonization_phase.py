"""Game phase for the colonization of hexagons by cells.

In this phase, cells grow and replicate on the hexagonal grid, biomass is generated,
and players can sell their harvest for credits. The phase includes rendering the game
state, handling user input, and managing the game loop.
"""

import sys

import pygame
from pygame.time import Clock

from core_modules import event_handler
from core_modules.cell_line import CellLine
from core_modules.game_state import GameState
from core_modules.hexagon_grid import HexagonGrid
from core_modules.process_plotter import ProcessPlotter
from core_modules.process_tracker import ProcessTracker
from core_modules.render_manager import RenderManager
from game_phases.escape_menu import EscapeMenu, EscapeMenuResult


class ReturnToMainMenuException(Exception):
    """Exception raised when the user wants to return to the main menu."""


class ColonizationPhase:
    """Class to handle the colonization phase of the game.

    Args:
        clock (Clock): The clock to manage the game loop.
        render_manager (RenderManager): The render manager to handle rendering.
    """

    def __init__(
        self, clock: Clock, render_manager: RenderManager, background_hexagon_grid
    ) -> None:
        self.clock: Clock = clock
        self.render_manager: RenderManager = render_manager
        self.background_hexagon_grid = background_hexagon_grid
        self.credits_gained: float = 0
        self.selling_initiated: bool = False
        self.selling_completed: bool = False
        self.process_tracker: ProcessTracker = ProcessTracker()
        self.process_plotter: ProcessPlotter = ProcessPlotter(plot_size=(5, 3))
        self.plot_surface: pygame.Surface | None = None
        self.cached_plot_position: tuple[int, int] | None = None
        self.cached_plot_size: tuple[int, int] | None = None
        self.plot_update_interval: int = 2
        self.frame_count: int = 0
        self.escape_menu: EscapeMenu | None = None

    def run_colonization_phase(
        self,
        game_state: GameState,
    ) -> None:
        """Run the colonization phase logic.

        Args:
            game_state (GameState): The current game state.
        """

        grid_center_offset = (0.28, 0.5)

        hexagon_grid = HexagonGrid(
            game_state, self.render_manager.current_screen_size, grid_center_offset
        )
        cell_line = CellLine(
            hexagon_grid, game_state, self.render_manager.current_screen_size, grid_center_offset
        )

        if self.escape_menu is None:
            self.escape_menu = EscapeMenu(
                self.clock, self.render_manager, self.background_hexagon_grid
            )

        self.process_tracker.initialize_with_initial_state(cell_line, hexagon_grid)

        self.process_plotter.reset_cache()
        self.plot_surface = self.process_plotter.create_simple_plot(self.process_tracker)

        while True:
            level_running = False

            for event in pygame.event.get():
                event_handler.handle_quit(event)

                if event_handler.handle_escape(event):
                    self.process_tracker.pause()
                    result = self.escape_menu.show_escape_menu(game_state)
                    self.process_tracker.resume()

                    if result == EscapeMenuResult.MAIN_MENU:
                        raise ReturnToMainMenuException()
                    elif result == EscapeMenuResult.QUIT:
                        pygame.quit()
                        sys.exit()

            for cell_coordinate, cell in list(
                cell_line.cells.items()
            ):  # iterate over a copy of the cell line to avoid modifying it while iterating
                if cell.growth:
                    level_running = True
                    if cell.energy_value >= game_state.cell_division_threshold:
                        new_cell_coordinate = cell_line.replicate_cell(
                            cell_coordinate,
                            hexagon_grid,
                            game_state,
                            self.render_manager.current_screen_size,
                        )
                        if new_cell_coordinate:
                            hexagon_grid.hexagons[new_cell_coordinate].set_highlight(50)
                    cell.update_radius(hexagon_grid.minimal_radius)
                    hexagon_grid.hexagons[cell_coordinate].update(cell)

            self.process_tracker.update(cell_line, hexagon_grid)
            self._update_process_plot()
            self._render_colonization_phase(game_state, hexagon_grid, cell_line)

            if not level_running:
                break

        current_biomass = cell_line.get_biomass()
        game_state.current_biomass = current_biomass
        game_state.run_biomass += current_biomass

        selling_size = 0.02 * game_state.current_biomass
        while True:
            for event in pygame.event.get():
                event_handler.handle_quit(event)

                if event_handler.handle_escape(event):
                    self.process_tracker.pause()
                    result = self.escape_menu.show_escape_menu(game_state)
                    self.process_tracker.resume()

                    if result == EscapeMenuResult.MAIN_MENU:
                        raise ReturnToMainMenuException()
                    elif result == EscapeMenuResult.QUIT:
                        pygame.quit()
                        sys.exit()

                if event_handler.handle_option_selection(event) and not self.selling_initiated:
                    self.selling_initiated = True

                if event_handler.handle_option_selection(event) and self.selling_completed:
                    game_state.current_credits += round(self.credits_gained, 2)
                    self.credits_gained = 0
                    self.selling_completed = False
                    self.selling_initiated = False
                    return

            if self.selling_initiated:
                biomass_sold = min(0.05 + 0.5 * selling_size, game_state.current_biomass)
                game_state.current_biomass -= biomass_sold
                self.credits_gained += biomass_sold * game_state.biomass_price
                if game_state.current_biomass == 0:
                    self.selling_completed = True

            self._render_point_screen(game_state, hexagon_grid, cell_line)

    def _update_process_plot(self) -> None:
        """Update the process parameters plot periodically for performance."""

        if self.frame_count % self.plot_update_interval == 0:
            self.frame_count = 0
            try:
                new_plot_surface = self.process_plotter.create_simple_plot(self.process_tracker)
                if new_plot_surface is not None:
                    self.plot_surface = new_plot_surface
            except Exception as e:
                print(f"Plot update error: {e}")

        self.frame_count += 1

    def _render_colonization_phase(
        self, game_state: GameState, hexagon_grid: HexagonGrid, cell_line: CellLine
    ) -> None:
        """Render the colonization phase of the game.

        Args:
            game_state (GameState): The current game state.
            hexagon_grid (HexagonGrid): The hexagon grid for the game.
            cell_line (CellLine): The cell line for the game.
        """

        self.render_manager.render_background_color("colonization_background")

        # Static reactor body
        reactor_center_x = 0.28
        self.render_manager.render_image(
            image_name="reactor_background",
            position_args={"center": (reactor_center_x, 0.5)},
            size_args=("height", 0.8),
        )

        # Animated reactor stirrer
        self.render_manager.render_image_animation(
            image_name="reactor_stirrer",
            images_per_second=game_state.fps_maximum,
            position_args={"center": (reactor_center_x, 0.5)},
            size_args=("height", 0.8),
        )

        # Animated reactor liquid
        self.render_manager.render_image_animation(
            image_name="reactor_liquid",
            images_per_second=game_state.fps_maximum // 2,
            position_args={"center": (reactor_center_x, 0.5)},
            size_args=("height", 0.8),
        )

        # Render shadow overlay
        self.render_manager.render_hexagons(hexagon_grid)
        self.render_manager.render_cells(cell_line)

        if self.plot_surface:
            self._render_process_plot_sidebar()

        self.render_manager.update_screen(game_state, self.clock)

    def _render_point_screen(
        self,
        game_state: GameState,
        hexagon_grid: HexagonGrid,
        cell_line: CellLine,
    ) -> None:
        self.render_manager.render_background_color(color="colonization_background")

        reactor_center_x = 0.28

        # Static reactor body
        self.render_manager.render_image(
            image_name="reactor_background",
            position_args={"center": (reactor_center_x, 0.5)},
            size_args=("height", 0.8),
        )

        self.render_manager.render_image_animation(
            image_name="reactor_stirrer",
            images_per_second=game_state.fps_maximum // 3,
            position_args={"center": (reactor_center_x, 0.5)},
            size_args=("height", 0.8),
        )

        self.render_manager.render_image_animation(
            image_name="reactor_liquid",
            images_per_second=game_state.fps_maximum // 6,
            position_args={"center": (reactor_center_x, 0.5)},
            size_args=("height", 0.8),
        )

        self.render_manager.render_hexagons(hexagon_grid)
        self.render_manager.render_cells(cell_line)

        self.render_manager.render_shadow_overlay(color="black", alpha=160)

        # Text Elements
        text_center_x = 0.28
        self.render_manager.render_text(
            "Biomass generated:", "large_font", "white", {"center": (text_center_x, 0.2)}
        )
        self.render_manager.render_text(
            f"{game_state.current_biomass:.2f}",
            "medium_font",
            "light_gray" if self.selling_completed else "white",
            {"center": (text_center_x, 0.3)},
        )
        self.render_manager.render_text(
            "Credits gained:", "large_font", "white", {"center": (text_center_x, 0.4)}
        )
        self.render_manager.render_text(
            f"{self.credits_gained:.2f}",
            "medium_font",
            "white" if self.selling_completed else "light_gray",
            {"center": (text_center_x, 0.5)},
        )

        if not self.selling_initiated:
            message = "Press Enter to sell harvest."
        elif not self.selling_completed:
            message = "Harvesting...."
        else:
            message = "Press Enter to continue."
        self.render_manager.render_text(
            message,
            "medium_font",
            "white",
            {"center": (text_center_x, 0.8)},
        )

        if self.plot_surface:
            self._render_process_plot_sidebar()

        self.render_manager.update_screen(game_state, self.clock)

    def _render_process_plot_sidebar(self) -> None:
        """Render the process parameters plot in the right sidebar."""

        if not self.plot_surface:
            return

        # Use render manager to handle plot rendering with caching
        self.cached_plot_position, self.cached_plot_size, self.plot_surface = (
            self.render_manager.render_plot_surface(
                plot_surface=self.plot_surface,
                cached_position=self.cached_plot_position,
                cached_size=self.cached_plot_size,
                max_width_fraction=0.50,
                max_height_fraction=0.85,
                margin=30,
                border_padding=8,
                background_color=(255, 255, 255),
                border_color=(60, 60, 80),
            )
        )

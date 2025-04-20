import pygame
from pygame.time import Clock

from base_elements import event_handler
from base_elements.cell_line import CellLine
from base_elements.game_state import GameState
from base_elements.hexagon_grid import HexagonGrid
from base_elements.render_manager import RenderManager


class ColonizationPhase:
    """Class to handle the colonization phase of the game."""

    def __init__(self, clock: Clock, render_manager: RenderManager) -> None:
        self.clock: Clock = clock
        self.render_manager: RenderManager = render_manager
        self.credits_gained: float = 0
        self.selling_initiated = False
        self.selling_completed = False

    def run_colonization_phase(
        self,
        game_state: GameState,
    ) -> None:
        """Run the colonization phase of the game.

        Args:
            game_state (GameState): The current game state.
        """

        hexagon_grid = HexagonGrid(game_state, self.render_manager.current_screen_size)
        cell_line = CellLine(
            hexagon_grid, game_state, self.render_manager.current_screen_size
        )

        while True:
            level_running = False

            for event in pygame.event.get():
                event_handler.handle_quit(event)

            for cell_coordinate, cell in list(
                cell_line.cells.items()
            ):  # iterate over a copy of the cell line
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

            self._render_colonization_phase(game_state, hexagon_grid, cell_line)

            if not level_running:
                break

        current_biomass = cell_line.get_biomass()
        # Add biomass and credits to game state
        game_state.current_biomass = current_biomass
        game_state.run_biomass += current_biomass

        # Render final points and wait for continue
        selling_size = 0.02 * game_state.current_biomass
        while True:
            for event in pygame.event.get():
                event_handler.handle_quit(event)

                if (
                    event_handler.handle_option_selection(event)
                    and not self.selling_initiated
                ):
                    self.selling_initiated = True

                if (
                    event_handler.handle_option_selection(event)
                    and self.selling_completed
                ):
                    game_state.current_credits += round(self.credits_gained, 2)
                    self.credits_gained = 0
                    self.selling_completed = False
                    self.selling_initiated = False
                    return

            if self.selling_initiated:
                biomass_sold = min(
                    0.05 + 0.5 * selling_size, game_state.current_biomass
                )
                game_state.current_biomass -= biomass_sold
                self.credits_gained += biomass_sold * game_state.biomass_price
                if game_state.current_biomass == 0:
                    self.selling_completed = True

            self._render_point_screen(game_state, hexagon_grid, cell_line)

    def _render_colonization_phase(
        self, game_state: GameState, hexagon_grid: HexagonGrid, cell_line: CellLine
    ) -> None:
        """Render the colonization phase of the game.

        Args:
            game_state (GameState): The current game state.
            hexagon_grid (HexagonGrid): The hexagon grid for the game.
            cell_line (CellLine): The cell line for the game.
        """

        self.render_manager.render_background("colonization_background")

        # Static background
        self.render_manager.render_image(
            image_name="reactor_background",
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        # Animated stirrer
        self.render_manager.render_animation(
            image_name="reactor_stirrer",
            images_per_second=game_state.fps_maximum,
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        # Animated liquid
        self.render_manager.render_animation(
            image_name="reactor_liquid",
            images_per_second=game_state.fps_maximum // 2,
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        self.render_manager.render_hexagons(hexagon_grid)
        self.render_manager.render_cells(cell_line)
        self.render_manager.render_fps(game_state, self.clock, "small_font")

        pygame.display.flip()
        self.clock.tick(game_state.fps_maximum)

    def _render_point_screen(
        self,
        game_state: GameState,
        hexagon_grid: HexagonGrid,
        cell_line: CellLine,
    ) -> None:
        self.render_manager.render_background("colonization_background")

        self.render_manager.render_image(
            image_name="reactor_background",
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        self.render_manager.render_animation(
            image_name="reactor_stirrer",
            images_per_second=game_state.fps_maximum // 3,
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        self.render_manager.render_animation(
            image_name="reactor_liquid",
            images_per_second=game_state.fps_maximum // 6,
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        self.render_manager.render_hexagons(hexagon_grid)
        self.render_manager.render_cells(cell_line)

        self.render_manager.render_shadow_overlay(color="black", alpha=160)

        # Text Elements
        self.render_manager.render_text(
            "Biomass generated:", "large_font", "white", {"center": (0.5, 0.2)}
        )
        self.render_manager.render_text(
            f"{game_state.current_biomass:.2f}",
            "medium_font",
            "light_gray" if self.selling_completed else "white",
            {"center": (0.5, 0.3)},
        )
        self.render_manager.render_text(
            "Credits gained:", "large_font", "white", {"center": (0.5, 0.4)}
        )
        self.render_manager.render_text(
            f"{self.credits_gained:.2f}",
            "medium_font",
            "white" if self.selling_completed else "light_gray",
            {"center": (0.5, 0.5)},
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
            {"center": (0.5, 0.8)},
        )

        self.render_manager.render_fps(game_state, self.clock, "small_font")

        pygame.display.flip()
        self.clock.tick(game_state.fps_maximum)

import sys

import pygame
from pygame import Surface
from pygame.time import Clock

from assets.colors import Colors
from assets.font_assets import FontAssets
from assets.image_assets import ImageAssets
from base_elements.cell import Cell
from base_elements.cell_line import CellLine
from base_elements.game_state import GameState
from base_elements.hexagon_grid import HexagonGrid
from base_elements.hexagon_tile import HexagonTile

# from settings_menu import SettingsMenu
from base_elements.utils import calculate_frame_delay, display_fps


class ColonizationPhase:
    def __init__(
        self,
        screen: Surface,
        clock: Clock,
        font_assets: FontAssets,
        image_assets: ImageAssets,
        colors: Colors,
    ) -> None:
        self.screen: Surface = screen
        self.clock: Clock = clock
        self.image_assets: ImageAssets = image_assets
        self.font_assets: FontAssets = font_assets
        self.colors: Colors = colors

        self.screen_size: tuple[int, int] = screen.get_size()
        self.frame_count: int = 0
        self.hexagon_size: int = 15

    def run_colonization_phase(
        self,
        game_state: GameState,
    ):
        """Colonization phase of the game: hexagon tiles with number of rings and cells"""

        self.hexagon_grid: HexagonGrid = HexagonGrid(game_state, self.screen)
        self.cell_line: CellLine = CellLine(self.screen)

        hexagons = self.hexagon_grid.initialize_hexagons()
        cells = self.cell_line.create_cells(hexagons, game_state)
        continued = False
        current_points = 0

        # Calculate energy consumption rate
        current_dNutridt = (
            game_state.cell_energy_consumption_rate_maximum
            * 1
            / (1 + game_state.cell_energy_affinity)
        ) * 40

        while True:
            level_running = False

            # User interactions
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if cell replication occurs
            for cell_key, cell in list(cells.items()):
                if cell.growth:
                    level_running = True
                    if cell.energy >= game_state.cell_division_threshold:
                        cells, hexagons = self.cell_line.replicate_cell(
                            cell,
                            cells,
                            hexagons,
                            game_state,
                        )
                    cell.update()

                cells[cell_key] = hexagons[cell_key].update(cells[cell_key])
                current_points += cells[cell_key].energy
            current_credits = int(
                round(game_state.biomass_price * (current_points * current_dNutridt))
            )
            current_points = int(round(current_points))

            self.render_colonization_phase(hexagons, cells, game_state)

            # Break from level loop when all growth has stopped
            if not level_running:
                break

        # Add generated points to account
        game_state.current_points += current_points
        game_state.run_points += game_state.current_points
        game_state.current_credits += current_credits

        # Render final points and wait for continue
        while not continued:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.render_point_screen(hexagons, cells, game_state)

    def render_colonization_phase(
        self,
        hexagons: dict[tuple[int, int], HexagonTile],
        cells: dict[tuple[int, int], Cell],
        game_state: GameState,
    ) -> None:
        """Renders the hexagons"""

        # Render background
        """self.screen.blit(
            self.image_assets.colonization_phase_background,
            self.image_assets.colonization_phase_background_rectangle,
        )"""
        self.screen.fill((230, 230, 230))

        # Blit the current reactor image
        self.screen.blit(
            self.image_assets.reactor_background,
            self.image_assets.reactor_background_rectangle,
        )
        reactor_stirrer_image_counter = calculate_frame_delay(
            self.frame_count,
            game_state.fps_maximum,
            game_state.fps_maximum,
            len(self.image_assets.reactor_stirrer_images),
        )
        self.screen.blit(
            self.image_assets.reactor_stirrer_images[reactor_stirrer_image_counter],
            self.image_assets.reactor_background_rectangle,
        )
        reactor_liquid_image_counter = calculate_frame_delay(
            self.frame_count,
            game_state.fps_maximum,
            game_state.fps_maximum // 2,
            len(self.image_assets.reactor_liquid_images),
        )
        self.screen.blit(
            self.image_assets.reactor_liquid_images[reactor_liquid_image_counter],
            self.image_assets.reactor_background_rectangle,
        )

        # Display FPS
        if game_state.show_fps:
            display_fps(
                self.screen, self.font_assets.small_font, self.clock, self.colors.white
            )

        # Render hexagons
        for hexagon in hexagons.values():
            if hexagon.highlight:
                hexagon.render_highlight(self.screen, border_colour=self.colors.black)
            else:
                hexagon.render(self.screen, border_colour=self.colors.black)

        # Render cells
        for cell in cells.values():
            cell.render(self.screen)

        # Update display
        pygame.display.flip()

        # Cap frame rate
        self.clock.tick(game_state.fps_maximum)

        # Increment the frame count
        self.frame_count += 1

    def render_point_screen(
        self,
        hexagons: dict[tuple[int, int], HexagonTile],
        cell_line: dict[tuple[int, int], Cell],
        game_state: GameState,
    ) -> None:
        """# Render background
        self.screen.blit(
            self.image_assets.colonization_phase_background,
            self.image_assets.colonization_phase_background_rectangle,
        )"""
        self.screen.fill((230, 230, 230))

        # Blit the current reactor image
        self.screen.blit(
            self.image_assets.reactor_background,
            self.image_assets.reactor_background_rectangle,
        )
        reactor_stirrer_image_counter = calculate_frame_delay(
            self.frame_count,
            game_state.fps_maximum,
            game_state.fps_maximum // 3,
            len(self.image_assets.reactor_stirrer_images),
        )
        self.screen.blit(
            self.image_assets.reactor_stirrer_images[reactor_stirrer_image_counter],
            self.image_assets.reactor_background_rectangle,
        )
        reac_liq_counter = calculate_frame_delay(
            self.frame_count,
            game_state.fps_maximum,
            game_state.fps_maximum // 6,
            len(self.image_assets.reactor_liquid_images),
        )
        self.screen.blit(
            self.image_assets.reactor_liquid_images[reac_liq_counter],
            self.image_assets.reactor_background_rectangle,
        )

        # Shade overlay
        game_over_screen_fade = pygame.Surface(self.screen.get_size())
        game_over_screen_fade.fill((0, 0, 0))
        game_over_screen_fade.set_alpha(120)
        self.screen.blit(game_over_screen_fade, (0, 0))

        # for i in range(rings):
        # TODO: remove cells from outside
        for hexagon in hexagons.values():
            hexagon.render(self.screen, border_colour=[0, 0, 0])
        for cell in cell_line.values():
            self.screen.blit(cell.image, cell.rectangle)

        # Points text
        width, height = self.screen_size
        final_points_text = self.font_assets.medium_font.render(
            f"Biomass generated: {game_state.current_points}",
            True,
            self.colors.light_gray,
        )
        final_points_rectangle = final_points_text.get_rect(
            center=(width // 2, height // 6)
        )
        self.screen.blit(final_points_text, final_points_rectangle)

        # Credits text
        final_credits_text = self.font_assets.title_font.render(
            f"Credits earned: {game_state.current_credits}", True, self.colors.hexagon
        )
        final_credits_rectangle = final_credits_text.get_rect(
            center=(width // 2, height // 6 + 50)
        )
        self.screen.blit(final_credits_text, final_credits_rectangle)

        # Enter to continue text
        conti_text = self.font_assets.medium_font.render(
            "Press Enter to continue!", True, self.colors.white
        )
        continue_text_rectangle = conti_text.get_rect(
            center=(width // 2, height // 1.2)
        )
        self.screen.blit(conti_text, continue_text_rectangle)

        # Display FPS
        if game_state.show_fps:
            display_fps(
                self.screen, self.font_assets.small_font, self.clock, self.colors.white
            )

        # Update display
        pygame.display.flip()

        # Cap frame rate
        self.clock.tick(game_state.fps_maximum)

        # Increment the frame count
        self.frame_count += 1

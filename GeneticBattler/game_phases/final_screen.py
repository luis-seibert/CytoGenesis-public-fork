import sys

import pygame
from pygame import Surface
from pygame.time import Clock

from assets.colors import Colors
from assets.font_assets import FontAssets
from assets.image_assets import ImageAssets
from base_elements.game_state import GameState
from base_elements.utils import display_fps


class FinalScreen:
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
        self.font_assets: FontAssets = font_assets
        self.image_assets: ImageAssets = image_assets
        self.colors: Colors = colors

        self.screen_size: tuple[int, int] = screen.get_size()
        self.frame_count: int = 0

    def run_final_screen(self, game_state: GameState) -> None:
        """Show final overall achieved points"""

        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.render_final_screen(game_state)

    def render_final_screen(self, game_state: GameState) -> None:
        """Renders overall achieved points"""

        # Render background
        self.screen.blit(
            self.image_assets.colonization_phase_background,
            self.image_assets.colonization_phase_background_rectangle,
        )

        # Global points text
        final_screen_text = self.font_assets.medium_font.render(
            "Total biomass generated:", True, self.colors.white
        )
        fin_screen_rectangle = final_screen_text.get_rect(
            center=(self.screen_size[0] // 2, self.screen_size[1] // 3.5)
        )
        self.screen.blit(final_screen_text, fin_screen_rectangle)

        run_points_text = self.font_assets.title_font.render(
            str(game_state.run_points), True, self.colors.white
        )
        run_points_rectangle = run_points_text.get_rect(
            center=(self.screen_size[0] // 2, self.screen_size[1] // 3 + 50)
        )
        self.screen.blit(run_points_text, run_points_rectangle)

        # Enter to continue text
        conti_text = self.font_assets.medium_font.render(
            "Press Enter to return to main menu!", True, self.colors.white
        )
        conti_text_rect = conti_text.get_rect(
            center=(self.screen_size[0] // 2, self.screen_size[1] // 1.85)
        )
        self.screen.blit(conti_text, conti_text_rect)

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

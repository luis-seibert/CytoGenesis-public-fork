import sys

import pygame
from pygame import Surface
from pygame.time import Clock

from assets.colors import Colors
from assets.font_assets import FontAssets
from assets.image_assets import ImageAssets
from base_elements.game_state import GameState
from base_elements.utils import display_fps


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
        self.selected_secondary_option: bool = False

    def run_settings_menu(self, game_state: GameState) -> GameState:
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Enter value setting if key is pressed in settings menu
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(
                            self.menu_options
                        )
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(
                            self.menu_options
                        )
                    elif event.key == pygame.K_RETURN:
                        secondary_option_selected = True
                        self.render_settings(
                            game_state, self.selected_option, secondary_option_selected
                        )

                        if self.selected_option == 0:  # Number of levels
                            while True:
                                for secondary_event in pygame.event.get():
                                    if secondary_event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()

                                    if secondary_event.type == pygame.KEYDOWN:
                                        if secondary_event.key == pygame.K_UP:
                                            game_state.default_number_levels += 1
                                        elif secondary_event.key == pygame.K_DOWN:
                                            if game_state.default_number_levels > 1:
                                                game_state.default_number_levels -= 1
                                        elif secondary_event.key == pygame.K_ESCAPE:
                                            secondary_option_selected = False
                                            self.run_settings_menu(game_state)
                                            return game_state

                                        # Re-Render settings screen immediately with the current values
                                        self.render_settings(
                                            game_state,
                                            self.selected_option,
                                            secondary_option_selected,
                                        )

                        elif self.selected_option == 1:  # Number of initial cells
                            while True:
                                for secondary_event in pygame.event.get():
                                    if secondary_event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()

                                    if secondary_event.type == pygame.KEYDOWN:
                                        if secondary_event.key == pygame.K_UP:
                                            game_state.default_number_cells += 1
                                        elif secondary_event.key == pygame.K_DOWN:
                                            if game_state.default_number_cells > 0:
                                                game_state.default_number_cells -= 1
                                        elif secondary_event.key == pygame.K_ESCAPE:
                                            secondary_option_selected = False
                                            self.run_settings_menu(game_state)
                                            return game_state

                                        # Re-Render settings screen immediately with the current values
                                        self.render_settings(
                                            game_state,
                                            self.selected_option,
                                            secondary_option_selected,
                                        )

                        elif self.selected_option == 2:  # Show fps
                            while True:
                                for secondary_event in pygame.event.get():
                                    if secondary_event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()

                                    if secondary_event.type == pygame.KEYDOWN:
                                        if secondary_event.key == pygame.K_UP:
                                            game_state.show_fps = (
                                                not game_state.show_fps
                                            )
                                        elif secondary_event.key == pygame.K_DOWN:
                                            if game_state.default_number_cells > 0:
                                                game_state.show_fps = (
                                                    not game_state.show_fps
                                                )
                                        elif secondary_event.key == pygame.K_ESCAPE:
                                            secondary_option_selected = False
                                            self.run_settings_menu(game_state)
                                            return game_state

                                        # Re-Render settings screen immediately with the current values
                                        self.render_settings(
                                            game_state,
                                            self.selected_option,
                                            secondary_option_selected,
                                        )

                    elif event.key == pygame.K_ESCAPE:
                        return game_state

            # Render settings screen
            self.render_settings(
                game_state, self.selected_option, self.selected_secondary_option
            )

    def render_settings(
        self,
        game_state: GameState,
        selected_option: int,
        selected_secondary_option: bool,
    ):
        """Renders the options menu"""

        global frame_count

        # Render background
        self.screen.blit(
            self.image_assets.colonization_phase_background,
            self.image_assets.colonization_phase_background_rectangle,
        )

        # Render the title
        title_text = self.font_assets.title_font.render(
            "Settings", True, self.colors.white
        )
        title_rect = title_text.get_rect(
            center=(self.screen_size[0] // 2, self.screen_size[1] // 10)
        )
        self.screen.blit(title_text, title_rect)

        # Render the settings menu options
        for i, option in enumerate(self.menu_options):
            color = (
                self.colors.white
                if i == selected_option and not selected_secondary_option
                else self.colors.black
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
                self.colors.white
                if i == selected_option and selected_secondary_option
                else self.colors.black
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
                self.screen, self.font_assets.small_font, self.clock, self.colors.white
            )

        # Update display
        pygame.display.flip()  # Update the display

        # Cap frame rate
        self.clock.tick(game_state.fps_maximum)

        # Increment the frame count
        # frame_count += 1

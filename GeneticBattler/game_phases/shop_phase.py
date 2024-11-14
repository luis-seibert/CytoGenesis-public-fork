import random
import sys
from typing import Any

import pygame
from pygame import Surface
from pygame.time import Clock

from assets.colors import Colors
from assets.font_assets import FontAssets
from assets.image_assets import ImageAssets
from base_elements.game_state import GameState
from base_elements.utils import calculate_frame_delay, display_fps


class ShopPhase:
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
        self.shop_phase_selected_option: int = 0

        self.number_item_rarities = 5
        self.item_rarities_colors: list[str] = [
            key for key in self.colors.item_rarity_colors.keys()
        ]
        self.item_rarities_indices: list[int] = [
            index for index in range(self.number_item_rarities)
        ]

        self.item_stats: list[dict[str, Any]] = [
            {
                "variable_name": "hexagon_nutrient_richness",
                "name": "Substrate richness",
                "modification_type": "increase",
                "default_modification_value": 0.01,
                "minimum_value": 0,
                "maximum_value": 1,
                "default_price": 40,
            },
            {
                "variable_name": "number_cells",
                "name": "Cell Inoculum size",
                "modification_type": "increase",
                "default_modification_value": 1,
                "minimum_value": 1,
                "maximum_value": 5,
                "default_price": 24,
            },
            {
                "variable_name": "hexagon_nutrient_varation",
                "name": "Reactor inhomogeneity",
                "modification_type": "decrease",
                "default_modification_value": 0.01,
                "minimum_value": 0,
                "maximum_value": 1,
                "default_price": 30,
            },
            {
                "variable_name": "cell_energy_affinity",
                "name": "Cell nutrient affinity",
                "modification_type": "increase",
                "default_modification_value": 0.001,
                "minimum_value": 0.001,
                "maximum_value": 0.1,
                "default_price": 16,
            },
            {
                "variable_name": "cell_division_threshold",
                "name": "Cell division threshold",
                "modification_type": "decrease",
                "default_modification_value": 0.1,
                "minimum_value": 0.1,
                "maximum_value": 1,
                "default_price": 25,
            },
            {
                "variable_name": "cell_energy_initial",
                "name": "Cell initial energy",
                "modification_type": "increase",
                "default_modification_value": 0.05,
                "minimum_value": 0.1,
                "maximum_value": 1,
                "default_price": 23,
            },
            {
                "variable_name": "cell_energy_variation",
                "name": "Cell energy variation",
                "modification_type": "decrease",
                "default_modification_value": 0.05,
                "minimum_value": 0,
                "maximum_value": 1,
                "default_price": 7,
            },
            {
                "variable_name": "cell_energy_consumption_rate_maximum",
                "name": "Cell consumption rate",
                "modification_type": "increase",
                "default_modification_value": 0.0025,
                "minimum_value": 0.01,
                "maximum_value": 0.2,
                "default_price": 32,
            },
            {
                "variable_name": "biomass_price",
                "name": "Biomass selling price",
                "modification_type": "increase",
                "default_modification_value": 0.15,
                "minimum_value": 1,
                "maximum_value": 3,
                "default_price": 48,
            },
        ]

    def run_shop_phase(self, game_state: GameState) -> GameState:
        """Shop phase to modify conditions for next iteration of the colonization phase"""

        self.shop_phase_options: list[dict[str, Any]] = [{"name": "Start batch"}]
        self.shop_phase_options += self.random_items(
            game_state.default_number_shop_items, game_state
        )

        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.shop_phase_selected_option = (
                            self.shop_phase_selected_option - 1
                        ) % len(self.shop_phase_options)
                    elif event.key == pygame.K_DOWN:
                        self.shop_phase_selected_option = (
                            self.shop_phase_selected_option + 1
                        ) % len(self.shop_phase_options)
                    elif event.key == pygame.K_RETURN:
                        if self.shop_phase_selected_option == 0:  # Continue the game
                            return game_state
                        else:  # Buy item
                            item = self.shop_phase_options[
                                self.shop_phase_selected_option
                            ]
                            if item["price"] > game_state.current_credits:
                                break

                            game_state.current_credits -= item["price"]
                            variable_value = getattr(game_state, item["variable_name"])
                            self.shop_phase_options.remove(item)
                            self.shop_phase_selected_option = 0

                            if item["modification_type"] == "increase":
                                if (
                                    variable_value + item["modification_value"]
                                    > item["maximum_value"]
                                ):
                                    new_variable_value = item["maximum_value"]
                                else:
                                    new_variable_value = (
                                        variable_value + item["modification_value"]
                                    )
                                setattr(
                                    game_state,
                                    item["variable_name"],
                                    new_variable_value,
                                )
                            if item["modification_type"] == "decrease":
                                if (
                                    variable_value - item["modification_value"]
                                    < item["minimum_value"]
                                ):
                                    new_variable_value = item["minimum_value"]
                                else:
                                    new_variable_value = (
                                        variable_value - item["modification_value"]
                                    )
                                setattr(
                                    game_state,
                                    item["variable_name"],
                                    new_variable_value,
                                )

                            self.render_shop_phase(game_state)

            # Render the shop
            self.render_shop_phase(game_state)

    def render_shop_phase(self, game_state: GameState):
        """Renders the shop/laboratory"""

        # Render background
        # self.screen.blit(
        #    self.image_assets.shop_background,
        #    self.image_assets.shop_background_rectangle,
        # )
        self.screen.fill((255, 255, 255))

        # Blit the current reactor image
        self.screen.blit(
            self.image_assets.reactor_background,
            self.image_assets.reactor_background_rectangle,
        )
        reactor_stirrer_image_counter = calculate_frame_delay(
            self.frame_count,
            game_state.fps_maximum,
            game_state.fps_maximum // 4,
            len(self.image_assets.reactor_stirrer_images),
        )
        self.screen.blit(
            self.image_assets.reactor_stirrer_images[reactor_stirrer_image_counter],
            self.image_assets.reactor_background_rectangle,
        )
        reactor_liquid_image_counter = calculate_frame_delay(
            self.frame_count,
            game_state.fps_maximum,
            game_state.fps_maximum // 8,
            len(self.image_assets.reactor_liquid_images),
        )
        self.screen.blit(
            self.image_assets.reactor_liquid_images[reactor_liquid_image_counter],
            self.image_assets.reactor_background_rectangle,
        )

        # Render statistics computer background
        self.screen.blit(
            self.image_assets.shop_computer_image,
            self.image_assets.shop_computer_image_rectangle,
        )

        # Render the shop title
        title_text = self.font_assets.large_font.render(
            "Welcome to the lab - prepare for your next cultivation!",
            True,
            self.colors.black,
            self.colors.white,
        )
        title_rectangle = title_text.get_rect(
            center=(self.screen_size[0] // 2, self.screen_size[1] // 10)
        )

        self.screen.blit(title_text, title_rectangle)

        # Credits calculation info
        info_text = self.font_assets.small_font.render(
            "Credits = Biomass price * Growth rate",
            True,
            self.colors.black,
            self.colors.white,
        )
        info_rectangle = info_text.get_rect(
            center=(self.screen_size[0] // 1.23, self.screen_size[1] // 5.5)
        )

        self.screen.blit(info_text, info_rectangle)

        # Render current credits
        credits_text = self.font_assets.large_font.render(
            f"Credits: {game_state.current_credits}",
            True,
            self.colors.orange,
        )
        credits_rectangle = title_text.get_rect(
            topleft=(self.screen_size[0] // 1.27, self.screen_size[1] // 4.5)
        )
        self.screen.blit(credits_text, credits_rectangle)

        # Render the shop options
        for i, option in enumerate(self.shop_phase_options):
            # Define colors

            if option["name"] == "Start batch":
                highlight_color = self.colors.gray
            else:
                highlight_color = self.colors.item_rarity_colors[
                    self.item_rarities_colors[option["rarity"]]
                ]
            unselected_color = (
                min(max(0, highlight_color[0] - 65), 255),
                min(max(0, highlight_color[1] - 65), 255),
                min(max(0, highlight_color[2] - 65), 255),
            )
            if self.shop_phase_selected_option == i:
                color = highlight_color
            else:
                color = unselected_color

            # Render shop options
            if option["name"] == "Start batch":
                option_text = self.font_assets.title_font.render(
                    option["name"], True, color
                )
            else:
                option_text = self.font_assets.medium_small_font.render(
                    option["name"] + f" [{str(option['price'])}]",
                    True,
                    color,
                )
            option_rect = option_text.get_rect(
                topright=(self.screen_size[0] - 30, self.screen_size[1] // 3 + i * 70)
            )

            self.screen.blit(option_text, option_rect)

        # Render statistics

        current_number_hexagons = (
            3 * game_state.current_level**2 + 3 * game_state.current_level + 1
        )

        specs = {
            "Biomass price": game_state.biomass_price,
            "Cell Inoculum size": game_state.number_cells,
            "Reactor capacity": current_number_hexagons,
            "Reactor mixing inhomogeneity": round(
                game_state.hexagon_nutrient_varation, 3
            ),
            "Substrate richness": round(game_state.hexagon_nutrient_richness, 3),
            "Cell division threshold": round(game_state.cell_division_threshold, 3),
            "Cell initial energy": round(game_state.cell_energy_initial, 3),
            "Cell energy inhomogeneity": round(game_state.cell_energy_variation, 3),
            "Substrate consumption rate": round(
                game_state.cell_energy_consumption_rate_maximum, 3
            ),
            "Cell nutrient affinity": round(game_state.cell_energy_affinity, 3),
        }
        for i, option in enumerate(specs):
            option_text = self.font_assets.small_font.render(
                f"{option}: {specs[option]}", True, self.colors.black
            )
            option_rect = option_text.get_rect(
                topleft=(
                    self.screen_size[0] // 28,
                    self.screen_size[1] // 3 + i * 30,
                )
            )
            self.screen.blit(option_text, option_rect)

        # Display FPS
        if game_state.show_fps:
            display_fps(
                self.screen, self.font_assets.small_font, self.clock, self.colors.white
            )

        # Update the display
        pygame.display.flip()

        # Cap frame rate
        self.clock.tick(game_state.fps_maximum)

        # Increment the frame count
        self.frame_count += 1

    def random_items(self, number_of_items: int, game_state: GameState):
        """Returns random item stats with rarity according to lvl"""

        item_indices = [
            random.randint(0, len(self.item_stats) - 1) for i in range(number_of_items)
        ]
        item_rarities_chances = [
            (1 + game_state.current_level) / (1 + chance**3)
            for chance in self.item_rarities_indices
        ]
        item_rarities = random.choices(
            self.item_rarities_indices,
            item_rarities_chances,
            k=number_of_items,
        )

        items = []
        for index, item_index in enumerate(item_indices):
            item = self.item_stats[item_index]
            item["modification_value"] = item["default_modification_value"] * (
                item_rarities[index] + 1
            )
            item["price"] = int(
                round(item["default_price"] * 2 * (item_rarities[index] + 1))
            )
            item["rarity"] = item_rarities[index]
            items.append(item)

        return items

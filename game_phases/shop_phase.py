import os
import random
from typing import Any

import pygame
from pygame.time import Clock

from base_elements import event_handler
from base_elements.game_state import GameState
from base_elements.render_manager import RenderManager
from base_elements.utils import get_config_from_yaml


class ShopPhase:
    """Shop phase class that manages the shop phase of the game."""

    def __init__(
        self,
        clock: Clock,
        render_manager: RenderManager,
    ) -> None:
        self.clock = clock
        self.render_manager = render_manager

        self.selected_option = 0
        self.item_rarity_indices: list[int] = list(range(5))
        self.item_stats: list[dict[str, Any]] = get_config_from_yaml(
            os.path.join(os.getcwd(), "assets", "shop_items.yaml")
        )

    def run_shop_phase(self, game_state: GameState) -> GameState:
        """Shop phase to modify conditions for next iteration of the colonization phase.

        Args:
            game_state (GameState): Game state object.

        Returns:
            GameState: Updated game state.
        """

        item_rarity_probabilities = self._calculate_rarity_probabilities(
            game_state.current_level
        )
        items_list = self._get_random_items(
            game_state.default_number_shop_items, item_rarity_probabilities
        )
        self.selected_option = 0

        while True:
            for event in pygame.event.get():
                event_handler.handle_quit(event)

                self.selected_option = event_handler.handle_option_navigation(
                    event,
                    self.selected_option,
                    len(items_list) + 1,
                )

                if event_handler.handle_option_selection(event):
                    if self.selected_option == 0:  # Continue to next phase
                        return game_state

                    if (
                        items_list[self.selected_option - 1]["price"]
                        <= game_state.current_credits
                    ):
                        game_state, items_list = self._buy_item(
                            self.selected_option - 1, items_list, game_state
                        )

            self.render_shop_phase(game_state, items_list)

    def _buy_item(
        self, item_index: int, items_list: list[dict[str, Any]], game_state: GameState
    ) -> tuple[GameState, list[dict[str, Any]]]:
        """Buys an item from the shop.

        Args:
            item_index (int): Index of the item to buy.
            items_list (list[dict[str, Any]]): List of items in the shop.
            game_state (GameState): Game state object.

        Returns:
            tuple[GameState, list[dict[str, Any]]]: Updated game state and items list.
        """

        item = items_list[item_index]
        game_state.current_credits = round(
            game_state.current_credits - item["price"], 2
        )
        variable_value = getattr(game_state, item["variable_name"])
        items_list.pop(item_index)

        # Update selection to the previous item if possible
        if len(items_list) == 0:
            self.selected_option = 0
        elif self.selected_option > len(items_list):
            self.selected_option = len(items_list)
        else:
            # Stay on the same index (which now points to the next item down)
            pass

        # Apply modification
        if item["modification_type"] == "increase":
            new_variable_value = min(
                variable_value + item["modification_value"], item["maximum_value"]
            )
        elif item["modification_type"] == "decrease":
            new_variable_value = max(
                variable_value - item["modification_value"], item["minimum_value"]
            )
        else:
            new_variable_value = variable_value  # No modification

        setattr(game_state, item["variable_name"], new_variable_value)

        return game_state, items_list

    def _get_random_items(
        self,
        number_of_items: int,
        item_rarity_probabilities: list[float],
    ) -> list[dict[str, Any]]:
        """Returns random items with level dependent rarity from the shop items list.

        Args:
            number_of_items (int): Number of items to return.
            item_rarity_probabilities (list[float]): Rarity probabilities for each item.

        Returns:
            list[dict[str, Any]]: List of random items with rarity and modification value.
        """

        random_items = random.choices(self.item_stats, k=number_of_items)
        random_items_rarities = random.choices(
            self.item_rarity_indices,
            item_rarity_probabilities,
            k=number_of_items,
        )

        rarity_adjusted_items = []
        for item in random_items:
            item["rarity"] = random_items_rarities[random_items.index(item)]
            item["modification_value"] = item["default_modification_value"] * (
                item["rarity"] + 1
            )
            item["price"] = round(item["default_price"] * 2 * (item["rarity"] + 1))
            rarity_adjusted_items.append(item)

        return rarity_adjusted_items

    def _calculate_rarity_probabilities(self, current_level: int) -> list[float]:
        """Calculates the rarity probabilities based on the current level.

        Args:
            current_level (int): Current level of the game.
        """

        return [
            (1 + current_level) / (1 + rarity**3) for rarity in self.item_rarity_indices
        ]

    def _check_item_modification_validity_color(
        self,
        item: dict[str, Any],
        game_state: GameState,
    ) -> str | None:
        """Checks if the item modification is valid.

        Args:
            item (dict[str, Any]): Item to check.
            game_state (GameState): Game state object.

        Returns:
            str: Color indicating the validity of the item modification.
        """

        current_variable_value = getattr(game_state, item["variable_name"])

        if item["modification_type"] == "increase":
            if current_variable_value < item["maximum_value"]:
                if (
                    round(current_variable_value + item["modification_value"], 2)
                    <= item["maximum_value"]
                ):
                    return "green"
                return "yellow"
            return "red"

        if item["modification_type"] == "decrease":
            if current_variable_value > item["minimum_value"]:
                if (
                    round(current_variable_value - item["modification_value"], 2)
                    >= item["minimum_value"]
                ):
                    return "green"
                return "yellow"
            return "red"

    def render_shop_phase(
        self, game_state: GameState, items_list: list[dict[str, Any]]
    ) -> None:
        """Renders the shop phase.

        Args:
            game_state (GameState): Game state object.
            items_list (list[dict[str, Any]]): List of items in the shop.
        """

        # Background
        self.render_manager.render_background("white")

        # Reactor background image
        self.render_manager.render_image(
            image_name="reactor_background",
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        # Stirrer animation
        self.render_manager.render_animation(
            image_name="reactor_stirrer",
            images_per_second=game_state.fps_maximum // 4,
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        # Liquid animation
        self.render_manager.render_animation(
            image_name="reactor_liquid",
            images_per_second=game_state.fps_maximum // 8,
            position_args={"center": (0.5, 0.5)},
            size_args=("height", 0.9),
        )

        # Shadow overlay
        self.render_manager.render_shadow_overlay(alpha=140)

        # Shop computer image
        self.render_manager.render_image(
            image_name="shop_computer_image",
            position_args={"bottomleft": (0, 1)},
            size_args=("height", 0.72),
        )

        # Gather statistics
        current_statistics = {
            "biomass_price": {
                "text": "Biomass price",
                "value": round(game_state.biomass_price, 3),
            },
            "number_cells": {
                "text": "Cell Inoculum size",
                "value": game_state.number_cells,
            },
            "hexagon_nutrient_variation": {
                "text": "Reactor mixing inhomogeneity",
                "value": round(game_state.hexagon_nutrient_variation, 3),
            },
            "hexagon_nutrient_richness": {
                "text": "Substrate richness",
                "value": round(game_state.hexagon_nutrient_richness, 3),
            },
            "cell_division_threshold": {
                "text": "Cell division threshold",
                "value": round(game_state.cell_division_threshold, 3),
            },
            "cell_energy_initial": {
                "text": "Cell initial energy",
                "value": round(game_state.cell_energy_initial, 3),
            },
            "cell_energy_variation": {
                "text": "Cell energy inhomogeneity",
                "value": round(game_state.cell_energy_variation, 3),
            },
            "cell_energy_consumption_rate_maximum": {
                "text": "Substrate consumption rate",
                "value": round(game_state.cell_energy_consumption_rate_maximum, 3),
            },
            "cell_energy_affinity": {
                "text": "Cell nutrient affinity",
                "value": round(game_state.cell_energy_affinity, 3),
            },
        }

        selected_item_index = self.selected_option - 1
        if self.selected_option != 0:
            item_variable_name = items_list[selected_item_index]["variable_name"]
            highlight_color = self._check_item_modification_validity_color(
                items_list[selected_item_index], game_state
            )
        else:
            item_variable_name = None
            highlight_color = "black"

        # Render options/statistics
        self.render_manager.render_options_values(
            option_items=current_statistics,
            position_args={"topleft": (0.036, 0.33)},
            selected_item_name=item_variable_name,
            font_name="small_font",
            distance_between_options=0.05,
            highlight_color=highlight_color,
            option_color="black",
        )

        # Title
        self.render_manager.render_text(
            "Welcome to the lab - prepare for your next cultivation!",
            "large_font",
            "white",
            {"center": (0.5, 0.1)},
        )

        # Current credits
        self.render_manager.render_text(
            text=f"Current credits: {game_state.current_credits:.2f}",
            font_name="medium_font",
            font_color_name="black",
            position_args={"topright": (0.975, 0.5)},
        )

        # Shop items
        selected_item = selected_item_index if selected_item_index >= 0 else None
        self.render_manager.render_shop_items(
            shop_items=items_list,
            selected_item=selected_item,
            font_name="large_font",
            position_args={"topleft": (0.575, 0.6)},
            distance_between_items=0.1,
        )

        # Continue button
        self.render_manager.render_text(
            text="Start next batch",
            font_name="large_font",
            font_color_name="light_gray",
            position_args={"topright": (0.975, 0.4)},
            highlight=(self.selected_option == 0),
        )

        self.render_manager.render_fps(game_state, self.clock, "small_font")

        pygame.display.flip()
        self.clock.tick(game_state.fps_maximum)

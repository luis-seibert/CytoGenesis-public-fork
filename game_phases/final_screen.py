"""Game phase for handling the final screen of the game.

This phase displays the final score and high scores, allowing the player to return to the main menu.
It includes rendering the final screen, updating high scores, and handling user input.
"""

import pygame
from pygame.time import Clock

from core_modules import event_handler
from core_modules.game_state import GameState
from core_modules.highscore_manager import update_highscores
from core_modules.player_data_manager import load_player_name
from core_modules.render_manager import RenderManager


class FinalScreen:
    """Class to handle the final run highscore screen of the game.

    Args:
        clock (Clock): The clock to manage the game loop.
        render_manager (RenderManager): The render manager to handle rendering.
    """

    def __init__(
        self,
        clock: Clock,
        render_manager: RenderManager,
    ) -> None:
        self.clock: Clock = clock
        self.render_manager: RenderManager = render_manager

    def run_final_screen(self, game_state: GameState) -> None:
        """Main loop for the final screen, displaying the final score and highscores.

        Args:
            game_state (GameState): The current state of the game.
        """

        player_name = load_player_name()
        if player_name is None:
            raise ValueError("Player name and highscore mismatch.")

        updated_scores, new_high_score_index = update_highscores(
            game_state.number_levels,
            game_state.run_biomass,
            player_name,
        )

        while True:
            for event in pygame.event.get():
                event_handler.handle_quit(event)

                if event_handler.handle_option_selection(event):
                    return

            self.render_final_screen(game_state, updated_scores, new_high_score_index)

    def render_final_screen(
        self,
        game_state: GameState,
        high_scores: list[dict],
        new_high_score_index: int | None,
    ) -> None:
        """Renders final score and top highscores for the given number of levels.

        Args:
            game_state (GameState): The current state of the game.
            high_scores (list[dict]): List of high scores to display.
            new_high_score_index (int | None): Index of the new high score, if any.
        """

        # Background color
        self.render_manager.render_background_color("very_light_gray")

        # Final score of the generated biomass
        self.render_manager.render_text(
            "Total biomass generated:",
            "title_font",
            "black",
            {"center": (0.5, 0.1)},
        )
        self.render_manager.render_text(
            f"{game_state.run_biomass:.2f}",
            "title_font",
            "black",
            {"center": (0.5, 0.175)},
        )

        # Highscores title
        self.render_manager.render_text(
            f"Highscores for {game_state.number_levels} levels:",
            "medium_font",
            "black",
            {"center": (0.5, 0.25)},
        )

        # Display each highscore with name, highlight new one in blue
        for i, entry in enumerate(high_scores):
            name = entry["name"]
            score = entry["score"]
            color = (
                "blue"
                if new_high_score_index is not None and i == new_high_score_index
                else "black"
            )

            self.render_manager.render_text(
                f"{i + 1}. {name}: {score:.2f}",
                "medium_font",
                color,
                {"center": (0.5, 0.35 + i * 0.05)},
            )

        # Message to return to main menu
        self.render_manager.render_text(
            "Press Enter to return to main menu!",
            "medium_font",
            "black",
            {"center": (0.5, 0.9)},
        )

        self.render_manager.update_screen(game_state, self.clock)

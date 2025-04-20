import pygame
from pygame.time import Clock

from base_elements import event_handler
from base_elements.game_state import GameState
from base_elements.highscore_manager import update_highscores
from base_elements.player_data_manager import load_player_name
from base_elements.render_manager import RenderManager


class FinalScreen:
    """Class to handle the final run highscore screen of the game."""

    def __init__(
        self,
        clock: Clock,
        render_manager: RenderManager,
    ) -> None:
        self.clock = clock
        self.render_manager = render_manager

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
        """Renders final score and top highscores.

        Args:
            game_state (GameState): The current state of the game.
            high_scores (list[dict]): List of high scores to display.
            new_high_score_index (int | None): Index of the new high score, if any.
        """

        self.render_manager.render_background("very_light_gray")

        # Final score
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

            # If it's the new high score, highlight it in blue
            # If new_high_score_index is None, it will not highlight anything
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

        # Prompt
        self.render_manager.render_text(
            "Press Enter to return to main menu!",
            "medium_font",
            "black",
            {"center": (0.5, 0.9)},
        )

        # FPS info
        self.render_manager.render_fps(game_state, self.clock, "small_font")

        pygame.display.flip()
        self.clock.tick(game_state.fps_maximum)

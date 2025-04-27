"""Core module for managing high scores in a game.

This module provides functionality to load, save, and update high scores. It handles the high
scores in a YAML file and ensures that duplicates are avoided when adding new scores. It also
sorts the scores in descending order and keeps only the top 10 scores.
"""

import yaml


def update_highscores(levels: int, score: float, player_name: str) -> tuple[list[dict], int | None]:
    """Update high scores with a new score.

    Args:
        levels (int): The number of levels completed.
        score (float): The score to be added.
        player_name (str): The name of the player.

    Returns:
        tuple[dict[int, list[dict], int | None]: A tuple containing the updated high scores
            list and the index of the new score if it was added, otherwise None.
    """

    highscores = _load_highscores()

    new_score_entry = {"name": player_name, "score": score}
    if levels not in highscores:
        highscores[levels] = []
    highscores[levels].append(new_score_entry)

    highscores[levels] = _remove_duplicates(highscores[levels])
    highscores[levels] = sorted(highscores[levels], key=lambda x: x["score"], reverse=True)
    highscores[levels] = highscores[levels][:10]

    _save_highscores(highscores)

    new_high_score_index = None
    if new_score_entry in highscores[levels]:
        new_high_score_index = highscores[levels].index(new_score_entry)

    return (highscores[levels], new_high_score_index)


def _load_highscores() -> dict[int, list[dict]]:
    """Load high scores from a YAML file.

    Returns:
        dict[int, list[dict]]: A dictionary where keys are levels played and values are lists of
            dictionaries containing high scores.
    """

    try:
        with open("highscores.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    except FileNotFoundError:
        return {}


def _save_highscores(highscores: dict[int, list[dict]]) -> None:
    """Save high scores to a YAML file.

    Args:
        highscores (dict[int, list[dict]]): A dictionary where keys are levels played and values
            are lists of dictionaries containing high scores.
    """

    with open("highscores.yaml", "w", encoding="utf-8") as file:
        yaml.dump(highscores, file)


def _remove_duplicates(scores: list[dict]) -> list[dict]:
    """Remove duplicate score entries from a list of dictionaries.

    Args:
        scores (list[dict]): A list of score dictionaries.

    Returns:
        list[dict]: A list with duplicates removed.
    """

    seen = set()
    unique_scores = []

    for score in scores:
        identifier = (score["name"], score["score"])
        if identifier not in seen:
            seen.add(identifier)
            unique_scores.append(score)

    return unique_scores

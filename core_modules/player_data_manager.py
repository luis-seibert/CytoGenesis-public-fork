"""Core module for handling player data in a game.

This module provides functionality to load and save player names. It uses a YAML file to store
the player name and ensures that the file is created if it does not exist. The player name can
be loaded from the file, and if it is not found, it returns None. The player name can also be
saved to the file, overwriting any existing name.
"""

from core_modules.utils import load_config_from_yaml, save_config_to_yaml

PLAYER_FILE = "player.yaml"


def load_player_name() -> str | None:
    """Load the player name from a YAML file.

    Returns:
        str | None: The player name if found, otherwise None.
    """

    player_data = load_config_from_yaml(PLAYER_FILE)

    if player_data:
        player_data = player_data.get("name")

    return player_data


def save_player_name(name: str):
    """Save the player name to a YAML file.

    Args:
        name (str): The player name to save.
    """

    save_config_to_yaml(PLAYER_FILE, {"name": name})

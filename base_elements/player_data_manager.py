import os

import yaml

PLAYER_FILE = "player.yaml"


def load_player_name() -> str | None:
    if os.path.exists(PLAYER_FILE):
        with open(PLAYER_FILE, "r") as f:
            data = yaml.safe_load(f)
            return data.get("name")
    return None


def save_player_name(name: str):
    with open(PLAYER_FILE, "w") as f:
        yaml.dump({"name": name}, f)

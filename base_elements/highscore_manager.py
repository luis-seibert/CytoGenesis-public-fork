import yaml


# Helper function to load the high scores from the file
def load_highscores() -> list[dict]:
    try:
        with open("highscores.yaml", "r") as file:
            return yaml.safe_load(file) or []
    except FileNotFoundError:
        return []


# Helper function to save the high scores to the file
def save_highscores(highscores: list[dict]) -> None:
    with open("highscores.yaml", "w") as file:
        yaml.dump(highscores, file)


# Function to update the highscores and avoid duplicates


# Function to update the highscores and avoid duplicates
def update_highscores(
    levels: int, score: float, player_name: str
) -> tuple[list[dict], int | None]:
    # Load the current high scores
    highscores = load_highscores()

    # Create a new score entry
    new_score_entry = {"name": player_name, "score": score}

    # Remove any duplicate scores for the same player
    highscores = [
        entry
        for entry in highscores
        if not (entry["name"] == player_name and entry["score"] == score)
    ]

    # Add the new score to the high scores list
    highscores.append(new_score_entry)

    # Sort the scores (highest first)
    highscores.sort(key=lambda x: x["score"], reverse=True)

    # Trim the list to ensure only the top 10 are kept
    highscores = highscores[:10]

    # Save the updated high scores back to the file
    save_highscores(highscores)

    # Find the index of the new score (if added)
    new_high_score_index = None
    if new_score_entry in highscores:
        new_high_score_index = highscores.index(new_score_entry)

    return (
        highscores,
        new_high_score_index,
    )  # Return both the updated list and the index

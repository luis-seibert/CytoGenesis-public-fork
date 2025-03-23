class Colors:
    """Color constants for the game."""

    white: tuple[int, int, int] = (255, 255, 255)
    black: tuple[int, int, int] = (0, 0, 0)
    gray: tuple[int, int, int] = (100, 100, 100)
    light_gray: tuple[int, int, int] = (150, 150, 150)
    green: tuple[int, int, int] = (51, 204, 51)
    blue: tuple[int, int, int] = (0, 102, 204)
    purple: tuple[int, int, int] = (110, 0, 240)
    orange: tuple[int, int, int] = (255, 153, 51)

    hexagon: tuple[int, int, int] = (255, 194, 65)

    item_rarity_colors: dict[str, tuple[int, int, int]] = {
        "gray": (155, 155, 155),
        "green": (51, 204, 51),
        "blue": (0, 102, 204),
        "purple": (110, 0, 240),
        "orange": (255, 153, 51),
    }

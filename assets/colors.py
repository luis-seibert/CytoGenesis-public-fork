class Colors:
    """Color constants for the game."""

    white: tuple[int, int, int] = (255, 255, 255)
    black: tuple[int, int, int] = (0, 0, 0)
    dark_gray: tuple[int, int, int] = (50, 50, 50)
    gray: tuple[int, int, int] = (100, 100, 100)
    light_gray: tuple[int, int, int] = (150, 150, 150)
    very_light_gray = (230, 230, 230)
    green: tuple[int, int, int] = (51, 204, 51)
    blue: tuple[int, int, int] = (0, 102, 204)
    purple: tuple[int, int, int] = (110, 0, 240)
    orange: tuple[int, int, int] = (255, 153, 51)
    yellow: tuple[int, int, int] = (255, 255, 0)
    red: tuple[int, int, int] = (255, 0, 0)

    hexagon_body: tuple[int, int, int] = (255, 194, 65)
    cell_body: tuple[int, int, int] = (243, 175, 61)

    colonization_background: tuple[int, int, int] = (230, 230, 230)

    # Item rarity colors
    item_common: tuple[int, int, int] = (155, 155, 155)  # Gray
    item_uncommon: tuple[int, int, int] = (51, 204, 51)  # Green
    item_rare: tuple[int, int, int] = (0, 102, 204)  # Blue
    item_epic: tuple[int, int, int] = (110, 0, 240)  # Purple
    item_legendary: tuple[int, int, int] = (255, 153, 51)  # Orange

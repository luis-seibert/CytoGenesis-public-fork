import sys

import pygame
from pygame.event import Event


def handle_quit(
    event: Event,
) -> None:
    """Quit the game if the user closes the window.

    Args:
        event (Event): Pygame event.
    """

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def handle_escape(event: Event) -> bool:
    """Handle escape key press.

    Args:
        event (Event): Pygame event.

    Returns:
        bool: True if the escape key was pressed, False otherwise.
    """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True

    return False


def handle_option_navigation(
    event: Event,
    selected_option: int,
    number_of_options: int,
) -> int:
    """Handle up and down key presses to navigate between options.

    Args:
        event (Event): Pygame event.
        selected_option (int): Option that is currently selected.
        number_of_options (int): Number of options.

    Returns:
        int: New selected option.
    """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected_option = (selected_option - 1) % number_of_options
        elif event.key == pygame.K_DOWN:
            selected_option = (selected_option + 1) % number_of_options

    return selected_option


def handle_change_option_value_with_circling(
    event: Event,
    value: int,
    maximum_value: int,
    minimum_value: int | None = None,
) -> int:
    """Handle option value change and circle back to the minimum value or zero.

    Args:
        event (Event): Pygame event.
        value (int): Option value that is currently selected.
        maximum_value (int): Maximum value before returning.
        minimum_value (int, optional): Minimum value. Defaults to None.

    Returns:
        int: New value.
    """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            value = (value + 1) % maximum_value
        if event.key == pygame.K_DOWN:
            value = (value - 1) % maximum_value
            if value < minimum_value:
                value = maximum_value

    return value if minimum_value is None else max(minimum_value, value)


def handle_change_bool_option(event: Event, selected_option: bool) -> bool:

    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_UP, pygame.K_DOWN]:
            return not selected_option

    return selected_option


def handle_secondary_option_selection(
    event: Event, secondary_option_selected: bool
) -> bool:

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if secondary_option_selected:
                return False
            return True

        if event.key == pygame.K_ESCAPE:
            return False

    return secondary_option_selected


def handle_option_selection(event: Event) -> bool:

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            return True

    return False

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
    minimum_value: int = 0,
) -> int:
    """Handle option value change and circle back to the minimum value.

    Args:
        event (Event): Pygame event.
        value (int): Option value that is currently selected.
        maximum_value (int): Maximum value (inclusive).
        minimum_value (int, optional): Minimum value. Defaults to 0.

    Returns:
        int: New value.
    """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            value += 1
            if value > maximum_value:
                value = minimum_value
        elif event.key == pygame.K_DOWN:
            value -= 1
            if value < minimum_value:
                value = maximum_value

    return value


def handle_change_bool_option(event: Event, selected_option: bool) -> bool:
    """Handle option value change and circle back to the minimum value.

    Args:
        event (Event): Pygame event.
        selected_option (bool): Option value that is currently selected.

    Returns:
        bool: New value.
    """

    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_UP, pygame.K_DOWN]:
            return not selected_option

    return selected_option


def handle_secondary_option_selection(
    event: Event, secondary_option_selected: bool
) -> bool:
    """Handle secondary option selection.

    Args:
        event (Event): Pygame event.
        secondary_option_selected (bool): Secondary option selected.

    Returns:
        bool: New value.
    """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if secondary_option_selected:
                return False
            return True

        if event.key == pygame.K_ESCAPE:
            return False

    return secondary_option_selected


def handle_option_selection(event: Event) -> bool:
    """Handle option selection.

    Args:
        event (Event): Pygame event.

    Returns:
        bool: True if the option is selected, False otherwise.
    """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            return True

    return False

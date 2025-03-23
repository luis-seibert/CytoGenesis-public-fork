import sys

import pygame
from pygame.event import Event


def handle_quit(
    event: Event,
) -> None:

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def handle_escape(event: Event) -> bool:

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True

    return False


def handle_up_down_navigation(
    event: Event,
    selected_option: int,
    number_of_options: int,
) -> int:

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected_option = (selected_option - 1) % number_of_options
        elif event.key == pygame.K_DOWN:
            selected_option = (selected_option + 1) % number_of_options

    return selected_option


def handle_change_number_option_with_return(
    event: Event,
    selected_option: int,
    number_of_options: int,
) -> int:

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected_option = (selected_option + 1) % number_of_options
        elif event.key == pygame.K_DOWN:
            selected_option = (selected_option - 1) % number_of_options

    return selected_option


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

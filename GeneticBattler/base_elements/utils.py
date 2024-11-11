import math

import pygame
from pygame import Surface


def round_to_odd(value):
    """Round to the nearest integer and force it to be odd if it's even"""

    rounded = round(value)

    # If even, adjust by 1 to make it odd
    return (
        rounded if rounded % 2 != 0 else rounded + 1 if value > rounded else rounded - 1
    )


def round_to_even(value):
    """Round to the nearest integer and force it to be even if it's odd"""

    rounded = round(value)

    # If even, adjust by 1 to make it odd
    return (
        rounded if rounded % 2 == 0 else rounded + 1 if value > rounded else rounded - 1
    )


def display_fps(screen: Surface, font, clock, color) -> None:
    fps_text = {
        "text": font.render("FPS: " + str(int(clock.get_fps())), True, color),
        "pos": (20, 20),
    }
    screen.blit(fps_text["text"], fps_text["pos"])


def calculate_frame_delay(
    frame_count: int,
    fps_maximum: int,
    imgage_fps: int,
    number_of_images: int,
) -> int:
    """Calculates image index for given image FPS"""

    frame_delay = fps_maximum // imgage_fps

    return int((frame_count // frame_delay) % number_of_images)


def calculate_pixel_from_axial(
    center: tuple[int, int], minimal_radius: int, axial_coordinates: tuple[int, int]
) -> tuple[int, int]:
    """Converts relative skewed hexagonal position to absolute pixel coordinates"""

    r, q = axial_coordinates

    pix_x: int = int(center[0] + r * 2 * minimal_radius + minimal_radius * q)
    pix_y: int = int(
        center[1] + q * math.sqrt((2 * minimal_radius) ** 2 - minimal_radius**2)
    )

    return (pix_x, pix_y)


def blit_text_box(
    screen: Surface,
    size_left_top_width_height,
    text_items,
    font,
    text_color,
    background_color,
):
    """Renders a box with text at specified position with size and color of box and text"""

    # Create rectangle with distance to left and top, and size width, height
    box_rectangle = pygame.Rect(
        size_left_top_width_height[0],
        size_left_top_width_height[1],
        size_left_top_width_height[2],
        size_left_top_width_height[3],
    )

    # Draw the box
    pygame.draw.rect(screen, background_color, box_rectangle)

    # Blit multiple text items inside the box
    for i, text in enumerate(text_items):
        # Render the text
        text_surface = font.render(text, True, text_color)
        # Calculate the position to blit the text
        text_rectangle = text_surface.get_rect()
        text_rectangle.topleft = (
            box_rectangle.x + 10,
            box_rectangle.y + 10 + i * 40,
        )

        # Blit the text
        screen.blit(text_surface, text_rectangle)

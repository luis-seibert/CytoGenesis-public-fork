"""Core module for rendering objects on the screen.

This module contains the RenderManager class, which is responsible for rendering various game
elements such as backgrounds, animations, images, hexagons, cells, text, and options on the screen.
The class provides methods to handle rendering in both full screen and windowed modes, as well as
to manage the rendering of different game states and objects.
"""

from typing import Any

import pygame
from pygame.font import Font
from pygame.time import Clock

from assets.colors import Colors
from assets.font_assets import FontAssets
from assets.image_assets import ImageAssets
from core_modules.cell_line import CellLine
from core_modules.game_state import GameState
from core_modules.hexagon_grid import HexagonGrid


class RenderManager:
    """Manages rendering objects on the screen.

    Args:
        initial_screen_size (tuple[int, int]): Initial size of the screen.
        full_screen (bool, optional): True full screen, False windowed mode. Defaults to False.
    """

    def __init__(self, initial_screen_size: tuple[int, int], full_screen: bool = False) -> None:
        self.windowed_screen_size: tuple[int, int] = (1024, 576)
        self.current_screen_size: tuple[int, int] = initial_screen_size
        self.toggle_full_screen(full_screen)

        self.image_assets: ImageAssets = ImageAssets(self.current_screen_size)
        self.font_assets: FontAssets = FontAssets(self.current_screen_size)
        self.colors: Colors = Colors()

    def update_screen(self, game_state: GameState, clock: Clock) -> None:
        """Updates the screen with the current game state and clock.

        THis method is responsible for updating the screen with rendered objects,
        including FPS display, background color, and any other game elements.

        Args:
            game_state (GameState): The current game state.
            clock (Clock): The clock to manage the game loop.
        """

        self.render_fps(game_state, clock, "small_font")
        pygame.display.flip()
        clock.tick(game_state.fps_maximum)

    def toggle_full_screen(self, full_screen: bool) -> None:
        """Toggles between full screen and windowed mode.

        Args:
            full_screen (bool): True for full screen, False for windowed mode.
        """

        if full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.windowed_screen_size)

        self.current_screen_size = self.screen.get_size()
        self.image_assets = ImageAssets(self.current_screen_size)
        self.font_assets = FontAssets(self.current_screen_size)

    def render_background_color(self, color: str) -> None:
        """Renders a background color on the screen.

        Args:
            color (str): Color of the background.
        """

        self.screen.fill(getattr(self.colors, color))

    def render_image_animation(
        self,
        image_name: str,
        images_per_second: int,
        position_args: dict[str, tuple[float, float]],
        size_args: tuple[str, float],
    ) -> None:
        """Renders an animation on the screen.

        Position args are in the form of a dictionary with keys as
        "topleft", "topright", "bottomleft", "bottomright", "center"
        and values as tuples of fractions of the screen size.

        Size args are in the form of a tuple with the first element
        being either "width" or "height" and the second element being
        the fraction of the screen size to scale the image to.

        Args:
            image_name (str): Name of the animation to render.
            images_per_second (int): Number of frames per second.
            position_args (dict[str, tuple[float, float]]): Position of the animation as fractions.
            size_args (tuple[str, float]): Size of the animation as a fraction of the screen size.
        """

        image_list = self.image_assets.get_animation_frames(image_name)
        if not image_list:
            raise ValueError(f"Animation '{image_name}' not found in assets.")

        number_of_images = len(image_list)
        image_index = int(pygame.time.get_ticks() / (1000 / images_per_second) % number_of_images)

        self._render_surface(
            surface=image_list[image_index],
            position_args=position_args,
            size_args=size_args,
        )

    def render_image(
        self,
        image_name: str,
        position_args: dict[str, tuple[float, float]],
        size_args: tuple[str, float],
    ) -> None:
        """Renders a static image on the screen.

        Position args are in the form of a dictionary with keys as
        "topleft", "topright", "bottomleft", "bottomright", "center"
        and values as tuples of fractions of the screen size.

        Size args are in the form of a tuple with the first element
        being either "width" or "height" and the second element being
        the fraction of the screen size to scale the image to.

        Args:
            image_name (str): Name of the image to render.
            position_args (dict[str, tuple[float, float]]): Position of the image as fractions.
            size_args (tuple[str, float]): Size of the image as a fraction of the screen size.
        """

        image = self.image_assets.get_image(image_name)
        if image is None:
            raise ValueError(f"Image '{image_name}' not found in assets.")

        self._render_surface(
            surface=image,
            position_args=position_args,
            size_args=size_args,
        )

    def _render_surface(
        self,
        surface: pygame.Surface,
        position_args: dict[str, tuple[float, float]],
        size_args: tuple[str, float],
    ) -> None:
        """Scales and renders a given surface.

        Position args are in the form of a dictionary with keys as
        "topleft", "topright", "bottomleft", "bottomright", "center"
        and values as tuples of fractions of the screen size.

        Size args are in the form of a tuple with the first element
        being either "width" or "height" and the second element being
        the fraction of the screen size to scale the image to.

        Args:
            surface (pygame.Surface): The surface to render.
            position_args (dict[str, tuple[float, float]]): Position of the surface as fractions.
            size_args (tuple[str, float]): Size of the surface as a fraction of the screen size.
        """

        # Scaling
        base_dimension, fraction = size_args
        if base_dimension == "width":
            new_width = int(self.current_screen_size[0] * fraction)
            aspect_ratio = surface.get_height() / surface.get_width()
            new_height = int(new_width * aspect_ratio)
        elif base_dimension == "height":
            new_height = int(self.current_screen_size[1] * fraction)
            aspect_ratio = surface.get_width() / surface.get_height()
            new_width = int(new_height * aspect_ratio)
        else:
            raise ValueError("size_args must be ('width' or 'height', float)")
        scaled_surface = pygame.transform.scale(surface, (new_width, new_height))

        # Positioning
        pos_key = next(iter(position_args))
        fraction_x, fraction_y = position_args[pos_key]
        pixel_position = (
            int(fraction_x * self.current_screen_size[0]),
            int(fraction_y * self.current_screen_size[1]),
        )

        surface_rect = scaled_surface.get_rect(**{pos_key: pixel_position})
        self.screen.blit(scaled_surface, surface_rect)

    def render_shadow_overlay(self, color: str = "black", alpha: int = 60) -> None:
        """Renders a shadow overlay on the screen.

        This method creates a semi-transparent overlay on the screen to
        simulate a shadow effect. The overlay is filled with the specified
        color and has a specified alpha value for transparency.

        Args:
            color (str, optional): Color of the shade overlay. Defaults to "black".
            alpha (int, optional): Opaqueness value of shade overlay. Defaults to 60.
        """

        shade_overlay = pygame.Surface(self.current_screen_size)
        shade_overlay.fill(getattr(self.colors, color))
        shade_overlay.set_alpha(alpha)
        self.screen.blit(shade_overlay, (0, 0))

    def render_hexagons(self, hexagon_grid: HexagonGrid) -> None:
        """Renders hexagons on the screen.

        Args:
            hexagon_grid (HexagonGrid): The grid containing hexagons to render.
        """

        for hexagon in hexagon_grid.hexagons.values():
            if hexagon.highlight_ticks > 0:
                hexagon.highlight_ticks -= 1
                hexagon_body_color = [
                    min(round(hexagon.body_color[0] + 50), 255),
                    min(round(hexagon.body_color[1] + 50), 255),
                    min(round(hexagon.body_color[2] + 50), 255),
                ]
            else:
                hexagon_body_color = hexagon.body_color
            pygame.draw.polygon(self.screen, hexagon_body_color, hexagon.vertices)
            pygame.draw.aalines(
                self.screen, self.colors.black, closed=True, points=hexagon.vertices
            )

    def render_cells(self, cell_line: CellLine) -> None:
        """Renders cells on the screen.

        Args:
            cells (dict[tuple[int, int], Any]): Cells to render.
        """

        for cell in cell_line.cells.values():
            pygame.draw.circle(  # Cell body
                self.screen, self.colors.cell_body, cell.coordinate_pixel, cell.radius
            )
            pygame.draw.circle(  # Cell border
                self.screen,
                self.colors.black,
                cell.coordinate_pixel,
                cell.radius,
                1,
            )

    def render_text(
        self,
        text: str,
        font_name: str,
        font_color_name: str,
        position_args: dict[str, tuple[float, float]],
        highlight: bool = False,
        highlight_color: str | None = None,
    ) -> None:
        """Renders text on the screen.

        Position args are in the form of a dictionary with keys as
        "topleft", "topright", "bottomleft", "bottomright", "center"
        and values as tuples of fractions of the screen size.

        Args:
            text (str): Text to render.
            font_name (str): Name of the font to use.
            font_color (str): Color of the font.
            position_args (dict[str, tuple[float, float]]): Position of the text as fractions.
            highlight (bool, optional): Whether to highlight the text. Defaults to False.
            highlight_color (str | None, optional): Color of the highlighted text. Defaults to None.
        """

        # Convert position_args to pixel values
        positioning = next(iter(position_args))
        position_args = {
            positioning: (
                round(position_args[positioning][0] * self.current_screen_size[0]),
                round(position_args[positioning][1] * self.current_screen_size[1]),
            )
        }

        font_color: tuple[int, int, int] = getattr(self.colors, font_color_name)
        if highlight:
            if not highlight_color:
                font_color = (
                    min(round(font_color[0] * 1.5), 255),
                    min(round(font_color[1] * 1.5), 255),
                    min(round(font_color[2] * 1.5), 255),
                )
            else:
                font_color = getattr(self.colors, highlight_color)
        font: Font = getattr(self.font_assets, font_name)
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect(**position_args)
        self.screen.blit(text_surface, text_rect)

    def render_options_values(
        self,
        option_items: dict[str, dict[str, Any]],
        position_args: dict[str, tuple[float, float]],
        selected_item_name: str | None,
        font_name: str,
        distance_between_options: float = 0.05,
        highlight_color: str | None = "white",
        option_color: str = "black",
    ) -> None:
        """Renders a list of options and values on the screen.

        Position args are in the form of a dictionary with keys as
        "topleft", "topright", "bottomleft", "bottomright", "center"
        and values as tuples of fractions of the screen size.

        Args:
            option_items (list[Any]): List of options and corresponding values to render.
            position_args (dict[str, tuple[float, float]]): Position of the options as fractions.
            selected_item_name (str | None): Name of the selected item.
            font_name (str): Name of the font to use.
            distance_between_options (float, optional): Distance between options as fraction.
            highlight_color (str, optional): Color of the highlighted option. Defaults to "white".
            option_color (str, optional): Color of the options. Defaults to "black".
        """

        if highlight_color is None:
            highlight_color = option_color

        position_key = next(iter(position_args))
        base_position = position_args[position_key]

        for i, key in enumerate(option_items):
            option_position = {
                position_key: (
                    base_position[0],
                    base_position[1] + i * distance_between_options,
                )
            }
            self.render_text(
                f"{option_items[key]['text']}: {option_items[key]['value']}",
                font_name,
                (highlight_color if key == selected_item_name else option_color),
                option_position,
            )

    def render_options(
        self,
        option_items: list[Any],
        selected_option: int | None,
        font_name: str,
        position_args: dict[str, tuple[float, float]],
        distance_between_options: float = 0.05,
        highlight_color: str = "white",
        option_color: str = "black",
    ) -> None:
        """Renders a list of options on the screen.

        Position args are in the form of a dictionary with keys as
        "topleft", "topright", "bottomleft", "bottomright", "center"
        and values as tuples of fractions of the screen size.

        Args:
            option_items (list[str]): List of options to render.
            selected_option (int | None): Index of the selected option.
            font_name (str): Name of the font to use.
            position_args (dict[str, tuple[float, float]]): Position of the options as fractions.
            distance_between_options (int, optional): Distance between options. Defaults to 50.
            highlight_color (str, optional): Color of the highlighted option. Defaults to "white".
            option_color (str, optional): Color of the options. Defaults to "black".
        """

        position_key = next(iter(position_args))
        base_position = position_args[position_key]

        for i, item in enumerate(option_items):
            option_position = {
                position_key: (
                    base_position[0],
                    base_position[1] + i * distance_between_options,
                )
            }
            self.render_text(
                str(item),
                font_name,
                (highlight_color if i == selected_option else option_color),
                option_position,
            )

    def render_fps(
        self,
        game_state: GameState,
        clock: pygame.time.Clock,
        font_name: str = "small_font",
    ) -> None:
        """Renders the FPS on the screen.

        This method displays the current frames per second (FPS) on the screen
        if the game state allows it. The FPS is calculated using the provided
        pygame clock object.

        Args:
            game_state (GameState): Game state object.
            font (Font): Font to use.
            clock (pygame.time.Clock): Pygame clock object.
        """

        if game_state.show_fps:
            fps = str(round(clock.get_fps()))
            self.render_text(
                f"FPS: {fps}",
                font_name,
                "black",
                {"topleft": (0.02, 0.02)},
            )

    def render_shop_items(
        self,
        shop_items: list[dict[str, Any]],
        selected_item: int | None,
        font_name: str,
        position_args: dict[str, tuple[float, float]],
        distance_between_items: float = 0.05,
    ) -> None:
        """Renders a list of shop items on the screen.

        Position args are in the form of a dictionary with keys as
        "topleft", "topright", "bottomleft", "bottomright", "center"
        and values as tuples of fractions of the screen size.

        Args:
            shop_items (list[dict[str, Any]]): List of shop items to render.
            selected_item (int | None): Index of the selected item.
            font_name (str): Name of the font to use.
            position_args (dict[str, tuple[float, float]]): Position of the options.
            distance_between_options (int, optional): Distance between options. Defaults to 50.
        """

        position_key = next(iter(position_args))
        base_position = position_args[position_key]

        item_rarity_colors = [
            "item_common",
            "item_uncommon",
            "item_rare",
            "item_epic",
            "item_legendary",
        ]

        for i, item in enumerate(shop_items):
            item_position = {
                position_key: (
                    base_position[0],
                    base_position[1] + i * distance_between_items,
                )
            }
            item_color = item_rarity_colors[item["rarity"]]
            self.render_text(
                text=f"{item["name"]}: {item["price"]}",
                font_name=font_name,
                font_color_name=item_color,
                position_args=item_position,
                highlight=i == selected_item,
            )

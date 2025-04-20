import os

import pygame


class ImageAssets:
    """Class to manage image assets for the game."""

    def __init__(self, screen_size: tuple[int, int]) -> None:
        pygame.init()
        self.screen_size = screen_size

        # Load all assets
        self.static_images = self._load_static_images()
        self.animated_images = self._load_animated_images()

    def _load_image(self, filename: str) -> pygame.Surface:
        path = os.path.join(os.getcwd(), "assets", "images", filename)
        return pygame.image.load(path).convert_alpha()

    def _load_static_images(self) -> dict[str, pygame.Surface]:
        """Load all static images used in the game."""
        return {
            "shop_background": self._load_image("shop_background.png"),
            "colonization_background": self._load_image("shop_background.png"),
            "point_screen_background": self._load_image("shop_background.png"),
            "reactor_background": self._load_image("reactor_background.png"),
            "shop_computer_image": self._load_image("computer_transparent_2.png"),
        }

    def _load_animated_images(self) -> dict[str, list[pygame.Surface]]:
        """Load all frame sequences for animated assets."""
        return {
            "reactor_liquid": self._load_animation_sequence("liquid", 31),
            "reactor_stirrer": self._load_animation_sequence("stirrer", 3),
        }

    def _load_animation_sequence(
        self, folder_name: str, frame_count: int
    ) -> list[pygame.Surface]:
        """Helper to load animation frames from a folder."""

        base_path = os.path.join(os.getcwd(), "assets", "images", folder_name)
        return [
            pygame.image.load(os.path.join(base_path, f"{i + 1}.png")).convert_alpha()
            for i in range(frame_count)
        ]

    def get_image(self, image_name: str) -> pygame.Surface:
        """Get a static image by name.

        Args:
            image_name (str): The name of the image to retrieve.

        Returns:
            pygame.Surface: The requested image surface.

        Raises:
            ValueError: If the image is not found in the static images.
        """

        image = self.static_images.get(image_name)
        if image is None:
            raise ValueError(f"Image '{image_name}' not found in static images.")
        return image

    def get_animation_frames(self, animation_name: str) -> list[pygame.Surface]:
        """Get animation frames by name.

        Args:
            animation_name (str): The name of the animation to retrieve.

        Returns:
            list[pygame.Surface]: A list of frames for the requested animation.

        Raises:
            ValueError: If the animation is not found in the animated images.
        """

        frames = self.animated_images.get(animation_name)
        if frames is None:
            raise ValueError(
                f"Animation '{animation_name}' not found in animated images."
            )
        return frames

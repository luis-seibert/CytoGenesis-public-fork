import os

import pygame


class ImageAssets:
    def __init__(
        self, screen_size: tuple[int, int]
    ) -> None:  # screen_size: tuple[width, height]
        pygame.init()

        # Phase background images
        self.shop_background = pygame.transform.scale(
            pygame.image.load(
                os.path.join(os.getcwd(), "assets", "images", "shop_background.png")
            ),
            (screen_size[0], screen_size[1]),
        )
        self.shop_background_rectangle = self.shop_background.get_rect()

        self.colonization_phase_background = pygame.transform.scale(
            pygame.image.load(
                os.path.join(os.getcwd(), "assets", "images", "shop_background.png")
            ),
            (screen_size[0], screen_size[1]),
        )
        self.colonization_phase_background_rectangle = (
            self.colonization_phase_background.get_rect()
        )

        self.point_screen_size_background = pygame.transform.scale(
            pygame.image.load(
                os.path.join(os.getcwd(), "assets", "images", "shop_background.png")
            ),
            (screen_size[0], screen_size[1]),
        )
        self.point_screen_size_background_rectangle = (
            self.point_screen_size_background.get_rect()
        )

        # Reactor body images
        reactor_image_path = os.path.join(
            os.getcwd(), "assets", "images", "reactor_background.png"
        )
        reactor_liquid_path = os.path.join(os.getcwd(), "assets", "images", "liquid")
        reactor_stirrer_path = os.path.join(os.getcwd(), "assets", "images", "stirrer")
        reactor_image_factor = 6
        self.reactor_background = pygame.transform.scale(
            pygame.image.load(reactor_image_path),
            (49 * reactor_image_factor, 83 * reactor_image_factor),
        )
        self.reactor_background_rectangle = self.reactor_background.get_rect()
        self.reactor_background_rectangle.center = (
            screen_size[0] // 2,
            screen_size[1] // 2,
        )

        # Reactor liquid images
        self.reactor_liquid_images = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(reactor_liquid_path, f"{i + 1}.png")),
                (49 * reactor_image_factor, 83 * reactor_image_factor),
            )
            for i in range(31)
        ]

        # Reactor stirrer images
        self.reactor_stirrer_images = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(reactor_stirrer_path, f"{i + 1}.png")),
                (49 * reactor_image_factor, 83 * reactor_image_factor),
            )
            for i in range(3)
        ]

        # Shop images
        computer_image_scaling_factor = 400
        temporary_computer_image = pygame.image.load(
            os.path.join(os.getcwd(), "assets", "images", "computer2.png")
        )
        self.shop_computer_image = pygame.transform.scale(
            temporary_computer_image,
            (
                computer_image_scaling_factor * 0.95,
                computer_image_scaling_factor * 1.2,
            ),
        )
        self.shop_computer_image_rectangle = self.shop_computer_image.get_rect()
        self.shop_computer_image_rectangle.center = (
            int(round(screen_size[0] // 5.5)),
            int(round(screen_size[1] // 1.455)),
        )

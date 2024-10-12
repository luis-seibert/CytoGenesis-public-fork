import pygame
import random
import gen_methods


# Define the Cell class
class Cell(pygame.sprite.Sprite):
    def __init__(self, center_skew, game_state, cell_state):
        super().__init__()
        self.game_state = game_state
        self.cell_state = cell_state
        self.center_skew = center_skew
        self.energy = self.cell_state.ENRG_INI * (1 + self.cell_state.ENRG_VAR * random.uniform(-1, 1))
        self.growth = True
        self.image = pygame.image.load("images\\COCCUS.png")
        self.rect = self.image.get_rect()
        self.rect.center = center_skew
        self.temp_image = pygame.image.load("images\\COCCUS3.png")

    def update(self):
        """Calculate factor of displayed cell size"""

        vis_size = self.energy / self.cell_state.DIV_TH
        scaled_size = vis_size * self.cell_state.CELL_SIZE   # scale image to energy
        adj_size = gen_methods.round_to_even(scaled_size)   # scale only if even (according to hexagon dimensions)
        self.image = pygame.transform.scale(self.temp_image, (adj_size, adj_size))

        self.rect = self.image.get_rect()
        self.rect.center = gen_methods.compute_skew_to_pix(CENTER=self.cell_state.CENTER,
                                                           min_radius=self.cell_state.CELL_SIZE/2,
                                                           skew_coords=self.center_skew)

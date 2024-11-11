class GameState:
    def __init__(
        self,
        screen_size: tuple[int, int],
    ):
        # Variables that are specific to each game run
        self.default_number_levels: int = 8  # number of levels in one run

        self.default_current_level: int = 0
        self.default_current_points: int = 0
        self.default_run_points: int = 0

        # Hexagon configs
        self.default_hexagon_size: int = int(screen_size[1] // 40)
        self.default_hexagon_body_color: tuple[int, int, int] = (255, 194, 65)
        self.default_hexagon_nutrient_color_index: int = 1
        self.default_hexagon_nutrient_varation: float = 0.35
        self.default_hexagon_nutrient_richness: float = 0.1

        # Cell configs
        self.default_number_cells: int = 1
        self.default_cell_body_size: float = 2 * self.default_hexagon_size
        self.default_cell_body_color: list[int] = [255, 255, 255]
        self.default_cell_division_threshold: float = 1
        self.default_cell_energy_consumption_rate_maximum: float = 0.05
        self.default_cell_energy_affinity: float = 0.02
        self.default_cell_energy_color_index: int = 1
        self.default_cell_energy_initial: float = 0.5
        self.default_cell_energy_variation: float = 0.2

        # Game configs
        self.default_user: str = "Unknown"
        self.fps_maximum: int = 50
        self.show_fps: bool = False
        self.default_number_shop_items: int = 3
        self.default_biomass_price: float = 1
        self.default_credits: int = 0

        self.reset()

    def reset(self):
        # Game configs
        self.number_levels = self.default_number_levels
        self.current_points = self.default_current_points
        self.current_level = self.default_current_level
        self.run_points = self.default_run_points
        self.biomass_price = self.default_biomass_price
        self.current_credits = self.default_credits

        # Hexagon configs
        self.hexagon_nutrient_varation = self.default_hexagon_nutrient_varation
        self.hexagon_nutrient_richness = self.default_hexagon_nutrient_richness

        # Cell configs
        self.number_cells = self.default_number_cells

        self.cell_body_size = self.default_cell_body_size
        self.cell_body_color = self.default_cell_body_color
        self.cell_division_threshold = self.default_cell_division_threshold
        self.cell_energy_consumption_rate_maximum = (
            self.default_cell_energy_consumption_rate_maximum
        )
        self.cell_energy_affinity = self.default_cell_energy_affinity
        self.cell_energy_color_index = self.default_cell_energy_color_index
        self.cell_energy_initial = self.default_cell_energy_initial
        self.cell_energy_variation = self.default_cell_energy_variation

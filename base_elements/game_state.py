class GameState:
    def __init__(
        self,
    ):
        # Variables that are specific to each game run
        self.default_number_levels: int = 5  # default number of levels in one run

        # Hexagon configs
        self.default_hexagon_minimal_radius_fraction: int = (
            40  # default minimal radius fraction of screen height
        )
        self.default_hexagon_nutrient_variation: float = 0.35
        self.default_hexagon_nutrient_richness: float = 0.1

        # Cell configs
        self.default_number_cells: int = 1
        self.default_cell_body_size: float = (
            2 * self.default_hexagon_minimal_radius_fraction
        )
        self.default_cell_body_color: list[int] = [255, 255, 255]
        self.default_cell_division_threshold: float = 1
        self.default_cell_energy_consumption_rate_maximum: float = 0.05
        self.default_cell_energy_affinity: float = 0.02
        self.default_cell_energy_color_index: int = 1
        self.default_cell_energy_initial: float = 0.5
        self.default_cell_energy_variation: float = 0.2

        # Game configs
        self.full_screen: bool = False
        self.default_user: str = "Unknown"
        self.fps_maximum: int = 50
        self.show_fps: bool = False
        self.default_number_shop_items: int = 3
        self.default_biomass_price: float = 100
        self.default_credits: float = 0.0

        # Settings
        self.max_number_levels: int = 10  # Maximum number of levels one can set
        self.max_number_initial_cells: int = (
            10  # Maximum number of initial cells one can set
        )

        self.reset()

    def reset(self):
        """Resets the game state to its initial values."""

        # Game configs
        self.number_levels = self.default_number_levels
        self.current_level = 0
        self.current_biomass = 0.0
        self.run_biomass = 0.0
        self.biomass_price = self.default_biomass_price
        self.current_credits = self.default_credits

        # Hexagon configs
        self.hexagon_nutrient_variation = self.default_hexagon_nutrient_variation
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

import random

import pygame
import gen_methods
import sys


### PYGAME INITIALIZATION ###


pygame.init()
pygame.display.set_caption("CytoGenesis")   # window title
clock = pygame.time.Clock()


### PERSISTENT DATA ###


# Display settings
SCREEN = {'WIDTH': 1024, 'HEIGHT': 576}
CENTER = (SCREEN['WIDTH']//2, SCREEN['HEIGHT']//2)
FPS = 50
screen = pygame.display.set_mode((SCREEN['WIDTH'], SCREEN['HEIGHT']))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
HEX_COL = [255, 194, 65]   # color of hexagon tiles
# HEX_COL = [44, 119, 55]   # old color of hexagon tiles (green)
NUT_COL = 1  # index of rgb which corresponds to nutrient value

# Global fonts
# font_name = pygame.font.get_default_font()
huge_font = pygame.font.Font("fonts\\Grand9K Pixel.ttf", 85)
title_font = pygame.font.Font("fonts\\Grand9K Pixel.ttf", 40)
medium_font = pygame.font.Font("fonts\\Grand9K Pixel.ttf", 25)
small_font = pygame.font.Font("fonts\\Grand9K Pixel.ttf", 16)

run_variables = { # TODO: adjust run variables, one global dict for vars that can be used for init, shop etc.
                'tot_points',
                'glob_points',
                'no_lvls',
                'no_cells',
                'NUT_VAR',
                'NUT_COL',
                'CELL_ARGS'}

# Hexagon tiles settings
SIZE = 15   # minimal radius of hexagon

# Set up frame counter for animation control
frame_count = 0


### ASSETS ###


shop_background_img = pygame.transform.scale(pygame.image.load("images\\shop_background.png"),
                                         (SCREEN['WIDTH'], SCREEN['HEIGHT']))
shop_background_rect = shop_background_img.get_rect()

col_phase_background_img = pygame.transform.scale(pygame.image.load("images\\shop_background.png"),
                                         (SCREEN['WIDTH'], SCREEN['HEIGHT']))
col_phase_background_rect = col_phase_background_img.get_rect()

point_screen_background_img = pygame.transform.scale(pygame.image.load("images\\shop_background.png"),
                                         (SCREEN['WIDTH'], SCREEN['HEIGHT']))
point_screen_background_rect = point_screen_background_img.get_rect()

# Reactor image
reac_img_factor = 6
reac_back = pygame.transform.scale(pygame.image.load("images\\reactor_background.png"), (49*reac_img_factor, 83*reac_img_factor))
reac_rect = reac_back.get_rect()
reac_rect.center = (SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 2)   # set rectangle position from first element

# Reactor liquid animation images
reac_img_liq_lst = [pygame.transform.scale(pygame.image.load(f"images\\liquid\\{i+1}.png"), (49*reac_img_factor, 83*reac_img_factor)) for i in range(31)]

# Reactor stirrer animation images
reac_img_stir_lst = [pygame.transform.scale(pygame.image.load(f"images\\stirrer\\{i+1}.png"), (49*reac_img_factor, 83*reac_img_factor)) for i in range(3)]


### GAME STATE ###


class GameState:
    def __init__(self):
        # Variables that are specific to each game run
        self.tot_points = int   # biomass credit account
        self.glob_points = int  # cumulative biomass credits gained
        self.no_lvls = int   # number of levels to play in one run
        self.no_cells = int   # number of initial cells each round is started with
        # Hexagon settings
        self.NUT_VAR = int  # initial relative variation in initial nutrient abundance (higher, more variation)

        self.reset()

    def reset(self):
        # Reset game state variables at the start of a new run
        self.tot_points = 0
        self.glob_points = 0
        self.no_lvls = 5
        self.no_cells = 1
        # Hexagon settings
        self.NUT_VAR = 1


### CELL STATE ###


class CellState:
    def __init__(self):
        # Cell settings
        self.CELL_SIZE = float  # max cell size 2 * minimal radius of hexagons
        self.CELLCOL = [int, int, int]
        self.NUTCONS = float  # maximum nut consumption rate
        self.NUTAFF = float  # nutrient affinity constant
        self.DIV_TH = float  # cell division energy threshold
        self.NUT_COL = int  # position [0,2] of rgb that is nutrient color
        self.NUT_INI = float  # initial value of nutrient based on hexagon nutrient color
        self.ENRG_INI = float  # initial value of energy of a cell
        self.ENRG_VAR = float  # cell initial energy variation factor (higher more variation)
        self.NO_LVLS = int  # number of levels to play

        self.reset()

    def reset(self):
        # Reset cell state variables at the start of a new run
        self.CELL_SIZE = 2 * SIZE,  # max cell size 2 * minimal radius of hexagons
        self.CELLCOL = [255, 255, 255]
        self.NUTCONS = 0.05  # maximum nut consumption rate
        self.NUTAFF = 0.02  # nutrient affinity constant
        self.DIV_TH = 1  # cell division energy threshold
        self.NUT_COL = NUT_COL  # position [0,2] of rgb that is nutrient color
        self.NUT_INI = HEX_COL[NUT_COL]  # initial value of nutrient based on hexagon nutrient color
        self.ENRG_INI = 0.25  # initial value of energy of a cell
        self.ENRG_VAR = 0.2  # cell initial energy variation factor (higher more variation)
        self.NO_LVLS = 5  # number of levels to play


### GAME STAGE SETTINGS ###


# MAIN MENU
main_menu_options = ["Start Game", "Settings", "Quit"]
mm_selected_option = 0

# SHOP PHASE
sp_options = ["Continue", "Item_1", "Item_2", "Item_3"]
sp_selected_option = 0

item_stats = {'nutrient_concentration': {'text': 'Substrate concentration', 'min': 1, 'max': 50, 'rarity': 0},
              'inoculum_number': {'text': 'Inoculum size', 'min': 1, 'max': 50, 'rarity': 0},
              'mixing_speed': {'text': 'Stirring speed', 'min': 1, 'max': 10, 'rarity': 0},
              'nutrient_affinity': {'text': 'Substrate affinity', 'min': 1, 'max': 10, 'rarity': 0},
              'nutrient_efficiency': {'text': 'Substrate efficiency', 'min': 1, 'max': 50, 'rarity': 0},
              'mutation_rate': {'text': 'Mutation rate', 'min': 1, 'max': 10, 'rarity': 0},
              }

# SETTINGS MENU
options = {'show_fps': False}
settings_menu_options = ["Nr. levels", "Inoculum", "Show FPS"]
settings_selected_option = 0
settings_selected_sec_option = False


def blit_text_box(pos_size_ltwh, text_items, font, text_color, back_color):
    """Renders a box with text at specified position with size and color of box and text"""

    # Create rectangle with distance to left and top, and size width, height
    box_rect = pygame.Rect(pos_size_ltwh[0], pos_size_ltwh[1], pos_size_ltwh[2], pos_size_ltwh[3])

    # Draw the box (a blue rectangle)
    pygame.draw.rect(screen, back_color, box_rect)

    # Blit multiple text items inside the box
    for i, text in enumerate(text_items):
        # Render the text
        text_surface = font.render(text, True, text_color)
        # Calculate the position to blit the text
        text_rect = text_surface.get_rect()
        text_rect.topleft = (box_rect.x + 10, box_rect.y + 10 + i * 40)  # Adjust spacing

        # Blit the text
        screen.blit(text_surface, text_rect)


def render_main_menu(selected_option):
    """Renders the main menu"""

    global frame_count

    # Render background
    screen.blit(col_phase_background_img, col_phase_background_rect)

    # Render the title
    title_text = huge_font.render("CytoGenesis", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 4))
    screen.blit(title_text, title_rect)

    # Render the menu options
    for i, option in enumerate(main_menu_options):
        color = WHITE if i == selected_option else BLACK
        option_text = title_font.render(option, True, color)
        option_rect = option_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 2 + i * 50))
        screen.blit(option_text, option_rect)

    # Display FPS
    if options['show_fps']:
        gen_methods.disp_fps(screen, small_font, clock, WHITE)

    # Update display
    pygame.display.flip()  # Update the display

    # Cap frame rate
    clock.tick(FPS)

    # Increment the frame count
    frame_count += 1


def render_settings(selected_option, selected_sec_option):
    """Renders the options menu"""

    global frame_count

    # Render background
    screen.blit(col_phase_background_img, col_phase_background_rect)

    # Render the title
    title_text = title_font.render("Settings", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 10))
    screen.blit(title_text, title_rect)

    # Render the settings menu options
    for i, option in enumerate(settings_menu_options):
        color = WHITE if i == selected_option and not selected_sec_option else BLACK
        option_text = title_font.render(option, True, color)
        option_rect = option_text.get_rect(topleft=(SCREEN['WIDTH'] // 10, SCREEN['HEIGHT'] // 4 + i * 50))
        screen.blit(option_text, option_rect)

    # Render the settings menu option values
    settings_menu_option_values = [no_lvls, no_cells, options['show_fps']]

    for i, option in enumerate(settings_menu_option_values):
        color = WHITE if i == selected_option and selected_sec_option else BLACK
        option_text = title_font.render(str(option), True, color)
        option_rect = option_text.get_rect(topright=(SCREEN['WIDTH'] - SCREEN['WIDTH'] // 10, SCREEN['HEIGHT'] // 4 + i * 50))
        screen.blit(option_text, option_rect)

    # Display FPS
    if options['show_fps']:
        gen_methods.disp_fps(screen, small_font, clock, WHITE)

    # Update display
    pygame.display.flip()  # Update the display

    # Cap frame rate
    clock.tick(FPS)

    # Increment the frame count
    frame_count += 1


def render_shop_phase(selected_option, curr_lvl, no_cells):
    """Renders the shop/laboratory"""

    global frame_count

    # Render background
    screen.blit(shop_background_img, shop_background_rect)

    # Render the shop title
    title_text = medium_font.render("Welcome to the lab - prepare for your next cultivation!", True, WHITE, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 10))
    # Render box
    border = 20
    rect_specs = (title_rect.topleft[0] - border,
                  title_rect.topleft[1] - border,
                  title_rect.width + 2 * border,
                  title_rect.height + 2 * border)
    blit_text_box(rect_specs, [], medium_font, WHITE, BLACK)

    screen.blit(title_text, title_rect)

    # Render the shop options
    # Render box
    rect_specs = (SCREEN['WIDTH'] - SCREEN['WIDTH'] * 0.25 + 30,
                  SCREEN['HEIGHT'] // 2.5 - 20,
                  SCREEN['WIDTH'] * 0.25 - 40,
                  300)
    blit_text_box(rect_specs, [], medium_font, WHITE, BLACK)

    for i, option in enumerate(sp_options):
        color = WHITE if i == selected_option else GRAY
        option_text = title_font.render(option, True, color, BLACK)
        option_rect = option_text.get_rect(topright=(SCREEN['WIDTH'] - 30,
                                                     SCREEN['HEIGHT'] // 2.5 + i * 70))

        screen.blit(option_text, option_rect)

    # Render points
    # Render box
    rect_specs = (SCREEN['WIDTH'] - SCREEN['WIDTH'] * 0.25 + 30,
                  SCREEN['HEIGHT'] // 6 + 10,
                  SCREEN['WIDTH'] * 0.25 - 40,
                  95)
    blit_text_box(rect_specs, [], medium_font, WHITE, BLACK)

    specs = {'Biomass': tot_points, 'Inoculum': no_cells, 'Reactor capacity': gen_methods.calc_no_hex(curr_lvl)}
    for i, option in enumerate(specs):
        option_text = small_font.render(f'{option}: {specs[option]}', True, WHITE)
        option_rect = option_text.get_rect(topright=(SCREEN['WIDTH'] - SCREEN['WIDTH'] // 30,
                                                     SCREEN['HEIGHT'] // 5 + i * 30))
        screen.blit(option_text, option_rect)

    # Display FPS
    if options['show_fps']:
        gen_methods.disp_fps(screen, small_font, clock, WHITE)

    # Update the display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(FPS)

    # Increment the frame count
    frame_count += 1


def render_col_phase(hexagons, cell_line, curr_points):
    """Renders the hexagons"""

    global frame_count

    # Render background
    screen.blit(col_phase_background_img, col_phase_background_rect)

    # Blit the current reactor image
    screen.blit(reac_back, reac_rect)   # background
    reac_stir_counter = gen_methods.calc_frame_delay(frame_count, FPS, FPS, len(reac_img_stir_lst))
    screen.blit(reac_img_stir_lst[reac_stir_counter], reac_rect)  # stirrer
    reac_liq_counter = gen_methods.calc_frame_delay(frame_count, FPS, FPS//2, len(reac_img_liq_lst))
    screen.blit(reac_img_liq_lst[reac_liq_counter], reac_rect)   # liquid

    # Render current points
    points_text = {
        'text': small_font.render('Biomass: ' + str(curr_points), True, WHITE),
        'pos': (SCREEN['WIDTH'] - 120, 20)}
    screen.blit(points_text['text'], points_text['pos'])

    # Display FPS
    if options['show_fps']:
        gen_methods.disp_fps(screen, small_font, clock, WHITE)

    # Render hexagons
    for hexagon in hexagons.values():
        hexagon.render(screen, border_colour=[0, 0, 0])
        if hexagon.new_cell:
            hexagon.render_highlight(screen, border_colour=[0, 0, 0])

    # Render cells
    for cell in cell_line.values():
        screen.blit(cell.image, cell.rect)

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(FPS)

    # Increment the frame count
    frame_count += 1


def render_point_screen(hexagons, cell_line, curr_points, rings):

    global frame_count

    # Render background
    screen.blit(col_phase_background_img, col_phase_background_rect)

    # Blit the current reactor image
    screen.blit(reac_back, reac_rect)  # background
    reac_stir_counter = gen_methods.calc_frame_delay(frame_count, FPS, FPS//3, len(reac_img_stir_lst))
    screen.blit(reac_img_stir_lst[reac_stir_counter], reac_rect)  # stirrer
    reac_liq_counter = gen_methods.calc_frame_delay(frame_count, FPS, FPS // 6, len(reac_img_liq_lst))
    screen.blit(reac_img_liq_lst[reac_liq_counter], reac_rect)  # liquid

    # Shade overlay
    game_over_screen_fade = pygame.Surface((SCREEN['WIDTH'], SCREEN['HEIGHT']))
    game_over_screen_fade.fill((0, 0, 0))
    game_over_screen_fade.set_alpha(80)
    screen.blit(game_over_screen_fade, (0, 0))

    #for i in range(rings):
    # TODO: remove cells from outside
    for hexagon in hexagons.values():
        hexagon.render(screen, border_colour=[0, 0, 0])
    for cell in cell_line.values():
        screen.blit(cell.image, cell.rect)

    # Points text
    fin_points_text = title_font.render(f"Biomass generated: {curr_points}", True, WHITE)
    fin_points_rect = fin_points_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 6))
    screen.blit(fin_points_text, fin_points_rect)

    # Enter to continue text
    conti_text = medium_font.render(f"Press Enter to continue!", True, WHITE)
    conti_text_rect = conti_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 1.2))
    screen.blit(conti_text, conti_text_rect)

    # Display FPS
    if options['show_fps']:
        gen_methods.disp_fps(screen, small_font, clock, WHITE)

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(FPS)

    # Increment the frame count
    frame_count += 1


def render_fin_screen():
    """Renders overall achieved points"""

    global frame_count

    # Render background
    screen.blit(col_phase_background_img, col_phase_background_rect)

    # Global points text
    fin_screen_text = medium_font.render("Total biomass generated:", True, WHITE)
    fin_screen_rect = fin_screen_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 3.5))
    screen.blit(fin_screen_text, fin_screen_rect)

    glob_points_text = title_font.render(str(glob_points), True, WHITE)
    glob_points_rect = glob_points_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 3 + 50))
    screen.blit(glob_points_text, glob_points_rect)

    # Enter to continue text
    conti_text = medium_font.render(f"Press Enter to return to main menu!", True, WHITE)
    conti_text_rect = conti_text.get_rect(center=(SCREEN['WIDTH'] // 2, SCREEN['HEIGHT'] // 1.85))
    screen.blit(conti_text, conti_text_rect)

    # Display FPS
    if options['show_fps']:
        gen_methods.disp_fps(screen, small_font, clock, WHITE)

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(FPS)

    # Increment the frame count
    frame_count += 1


def main_menu():
    """Main menu with several options to choose from"""

    global mm_selected_option

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mm_selected_option = (mm_selected_option - 1) % len(main_menu_options)
                elif event.key == pygame.K_DOWN:
                    mm_selected_option = (mm_selected_option + 1) % len(main_menu_options)
                elif event.key == pygame.K_RETURN:
                    if mm_selected_option == 0:
                        # Start the game
                        print("start game selected and confirmed")
                        start_game()
                    elif mm_selected_option == 1:
                        # Open settings menu
                        settings_menu()
                    elif mm_selected_option == 2:
                        # Quit the game
                        pygame.quit()
                        sys.exit()

        # Render the main menu
        render_main_menu(mm_selected_option)


def settings_menu():
    """Settings menu"""

    global settings_selected_option, settings_selected_sec_option, no_lvls, no_cells

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If key is pressed in settings menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    settings_selected_option = (settings_selected_option - 1) % len(main_menu_options)
                elif event.key == pygame.K_DOWN:
                    settings_selected_option = (settings_selected_option + 1) % len(main_menu_options)
                elif event.key == pygame.K_RETURN:
                    settings_selected_sec_option = True
                    # Re-Render settings screen immediately with the current values
                    render_settings(settings_selected_option, settings_selected_sec_option)

                    if settings_selected_option == 0:  # Number of levels
                        while True:
                            for sec_event in pygame.event.get():
                                if sec_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                if sec_event.type == pygame.KEYDOWN:
                                    if sec_event.key == pygame.K_UP:
                                        no_lvls += 1
                                    elif sec_event.key == pygame.K_DOWN:
                                        if no_lvls > 1:
                                            no_lvls -= 1
                                    elif sec_event.key == pygame.K_ESCAPE:
                                        settings_selected_sec_option = False
                                        settings_menu()  # Exit the inner loop

                                    # Re-Render settings screen immediately with the current values
                                    render_settings(settings_selected_option, settings_selected_sec_option)

                    elif settings_selected_option == 1:  # Number of initial cells
                        while True:
                            for sec_event in pygame.event.get():
                                if sec_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                if sec_event.type == pygame.KEYDOWN:
                                    if sec_event.key == pygame.K_UP:
                                        no_cells += 1
                                    elif sec_event.key == pygame.K_DOWN:
                                        if no_cells > 0:
                                            no_cells -= 1
                                    elif sec_event.key == pygame.K_ESCAPE:
                                        settings_selected_sec_option = False
                                        settings_menu()  # Exit the inner loop

                                    # Re-Render settings screen immediately with the current values
                                    render_settings(settings_selected_option, settings_selected_sec_option)

                    elif settings_selected_option == 2:  # Show fps
                        options['show_fps'] = not options['show_fps']

                elif event.key == pygame.K_ESCAPE:
                    main_menu()

        # Render settings screen
        render_settings(settings_selected_option, settings_selected_sec_option)


def col_phase(game_state, cell_state, rings, cells, curr_lvl):
    """Colonization phase of the game: hexagon tiles with number of rings and cells"""

    hexagons = gen_methods.init_hexagons(HEX_COL, CENTER, SIZE, rings, no_lvls)
    cell_line = gen_methods.create_cell_line(game_state, cell_state, hexagons, cells, curr_lvl)
    continued = False

    while True:
        # Loop running flag
        lvl_running = False

        # User interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()

        # Check if cell replication occurs
        for cell in list(cell_line.values()):  # Iterate over a copy of the keys
            if cell.energy >= cell_state.DIV_TH and cell.growth:
                cell_line, hexagons = gen_methods.replicate(cell, cell_line, hexagons)

        # Update cells
        for cell in cell_line.values():
            # Check if growth has stopped
            if cell.growth is True:
                lvl_running = True
            cell.update()

        # Update hexagons where cells are
        for cell_key in cell_line:
            hexagons[cell_key], cell_line[cell_key] = hexagons[cell_key].update(cell_line[cell_key])

        # Calculate and display points
        curr_points = 0
        for cell_key in cell_line:
            curr_points += cell_line[cell_key].energy
        curr_points = int(round(curr_points))   # round points

        render_col_phase(hexagons, cell_line, curr_points)

        # Break from level loop when growth has stopped
        if not lvl_running:
            break

    # Add generated points to account
    game_state.tot_points += curr_points
    game_state.glob_points += game_state.tot_points

    # Render final points and wait for continue
    while not continued:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        render_point_screen(hexagons, cell_line, curr_points, rings)


def shop_phase(curr_lvl, no_cells):
    """Shop phase to increase and set conditions for next iter of col_phase"""

    global sp_selected_option

    def rand_item(lvl):
        """"Returns random item stats with rarity according to lvl"""

        global item_stats

        item_idx_key = [(i, key) for i, key in enumerate(item_stats)]
        random_item_idx = random.randint(0, len(item_idx_key)-1)  # choose random item index

        return item_stats[item_idx_key[random_item_idx][1]]

    shop_items = [rand_item(curr_lvl), rand_item(curr_lvl), rand_item(curr_lvl)]   # choose 3 random items

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sp_selected_option = (sp_selected_option - 1) % len(sp_options)
                elif event.key == pygame.K_DOWN:
                    sp_selected_option = (sp_selected_option + 1) % len(sp_options)
                elif event.key == pygame.K_RETURN:
                    if sp_selected_option == 0:
                        # Continue the game
                        # print("Continue Game selected")
                        return
                    else:
                        # Buy item no. X

                        print(f"Buying item {shop_items[sp_selected_option-1]}")


        # Render the shop
        render_shop_phase(sp_selected_option, curr_lvl, no_cells)


def final_screen():
    """SHow final overall achieved points"""

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_menu()

        render_fin_screen()


def start_game():
    """Start a run"""

    # Create instances
    game_state = GameState()
    cell_state = CellState()

    # Main game loop
    for i in range(no_lvls):
        col_phase(game_state, cell_state, rings=i, cells=no_cells, curr_lvl=i+1)
        if i < no_lvls-1:
            shop_phase(i, no_cells)

    # Final overall points display
    final_screen()


def main():
    """Main function"""

    # Start with main menu
    main_menu()


if __name__ == "__main__":
    main()

# TODO:  Base functions

# IMPORTANT:
# add loosing condition: ?
    # production/research aim, failure -< loosing "health" / game
    # increasing input costs (inoculum) -> loose if points not enough for next round
    # economic pressure, market fluctuations?

# End of game, enter -> return to main menu
# switch fonts to pixel font
# unite global variables into one data object (perks)
# adjust speed of scaling level speed with number of cell growth cycles until all hex are full
# make more reactor images, scale fps with mixing perk, which is connected to randomness of nutrient
# add evolution system, mutation rate probability to produce mutations that can be used to buy cellular perks
# biomass/product can be used to buy and upgrade lab devices, nutrient broth etc.

# LESS IMPORTANT:
# fps counter not working correctly in slow fps -> still shows high

# OPTIONAL:
# Fix FPS font flickering
# maybe begin with 1 ring -> petri dish, upgrade to bioractor with capacity upgrades

# FAR FUTURE:
# display cultivation parameters (plot cultivation data during col phase)
# emergency buttons for temp bonus?

# increasing difficulty with rounds:
    # environmental changes: temperature, pH, contaminations, nutrient, ...
    # increasing maintenance costs

# make lategame (after 10 or so rounds), add production of protein of interest, that gives different type of points that can be used for advanced upgrades
# Add tech tree for lab devices, cell line
# add meta progression: ?
# add compendium to main menu, "Basics of bioprocess engineering" - that explain most important mechanics

# TODO: Ideas for shop
# PERKS:
    # start tile energy -> could be increased by perk
    # increase inoculum, temp and permanent as a perk
    # mixing speed -> randomness of nutrient decreases
    # nutrient consumption rate
    # nutrient affinity?
    # mutation rate?
    # certificates (quality), contracts -> increase biomass gain

# add refresh of shop
# adjust optics and layout of shop, could be same as lab space, with basic devices to buy and upgrade, adjust col_phase accordingly

# FAR FUTURE:
# different strains with unique appearance and traits
# perks have different qualities (common, rare, etc.)
# perks have "set boni", synergies

# TODO: Improve user experience
# implement nice background/overlay for microscope/over

# FAR FUTURE:
# implement background music
# fine-tune text positions

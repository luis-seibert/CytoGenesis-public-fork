import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle Animation")

# Load background and particle images
background_image = pygame.image.load('background.png').convert()
particle_image = pygame.image.load('particle.png').convert_alpha()

# Particle settings
particle_speed = 5  # How fast the particles move
particle_x = 0  # Initial position (left side of the screen)
particle_y = 300  # Y position for particles (fixed for now)

# Set the FPS (frames per second)
clock = pygame.time.Clock()
FPS = 60


# Function to move and blit particles
def animate_particles():
    global particle_x

    # Main loop for the game
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Blit the background image
        screen.blit(background_image, (0, 0))

        # Update the particle's position (moving to the right)
        particle_x += particle_speed

        # If the particle goes off the right edge of the screen, reset to the left
        if particle_x > SCREEN_WIDTH:
            particle_x = -particle_image.get_width()  # Reset particle's position

        # Blit the particle image at the updated position
        screen.blit(particle_image, (particle_x, particle_y))

        # Update the display
        pygame.display.update()

        # Cap the frame rate
        clock.tick(FPS)


# Call the animation function
animate_particles()

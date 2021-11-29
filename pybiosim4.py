#!/usr/bin/env python3

# pybiosim4

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500

# Import pygame 
import pygame

from src.simulator import Simulator

def main():

    global SCREEN, CLOCK
    pygame.init()

    # Set up the clock for a decent framerate
    CLOCK = pygame.time.Clock()

    # Set up the drawing window
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Fill the background
    SCREEN.fill(BLACK)


    # Run until the user quits
    running = True
    while running:

        s = Simulator()
        #s.drawGrid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Flip the display
        pygame.display.update()

        # rate x frames per second
        CLOCK.tick(30)


    # quit
    pygame.quit()

if  __name__ == "__main__":
    main()

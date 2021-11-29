
from src.peeps import Peeps

POPULATION = 300


# /********************************************************************************
# Start of simulator
#
# All the agents are randomly placed with random genomes at the start. The outer
# loop is generation, the inner loop is simStep. There is a fixed number of
# simSteps in each generation. Agents can die at any simStep and their corpses
# remain until the end of the generation. At the end of the generation, the
# dead corpses are removed, the survivors reproduce and then die. The newborns
# are placed at random locations, signals (pheromones) are updated, simStep is
# reset to 0, and a new generation proceeds
class Simulator:
    """ Simulator class"""


    # grid.init
    #def drawGrid():
    #    blocksize = 20
    #    for x in range(0, WINDOW_WIDTH, blocksize):
    #        for y in range(0, WINDOW_HEIGHT, blocksize):
    #            rect = pygame.Rect(x, y, blocksize, blocksize)
    #            pygame.draw.rect(SCREEN, WHITE, rect, 1)

    # signals.init

    peeps = Peeps(POPULATION)

    print("INFO: pop: {}".format(peeps.ret_population()))
    print("INFO: indivs: {}".format(peeps.ret_individuals()))

    generation = 0
    #initGenerationZero()


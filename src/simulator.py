# simulator.py - Main thread

# This file contains Simulator(), the top-level entry point of the simulator.

from src.peeps import Peeps
from src.spawnNewGeneration import initializeGenerationZero

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
    # signals.init

    # peeps init
    p = Peeps(POPULATION)

    #p.queueForDeath('12')
    #p.queueForMove('42', (12,13))
    #p.queueForDeath('2')
    #p.queueForDeath('14')
    #p.queueForDeath('16')
    #p.queueForDeath('1112')
    #p.queueForDeath('19992')
    #p.queueForMove('43', (12,19))
    #p.queueForMove('45', (13,43))
    #p.queueForMove('47', (15,15))
    #p.queueForMove('92', (17,53))

    print("INFO: pop: {}".format(p.ret_population()))
    #print("INFO: indivs: {}".format(p.ret_individuals()))
    #print("INFO: death queue length: {}".format(p.dq.size()))
    #print("INFO: move queue length: {}".format(p.mq.size()))

    generation = 0
    initializeGenerationZero(p)

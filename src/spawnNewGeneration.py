from src.indiv import Indiv

# Requires that the grid, signals, peeps containers have been allocated.
# This will erase the grid and signal layers, create a population in
# the peeps container at random locations with random genomes.
def initializeGenerationZero(p):

    # The grid has already been allocated, clear and reuse it
    #grid.zeroFill()
    #grid.createBarrier(p.replaceBarrierTypeGenerationNumber == 0
    #                   ? p.replaceBarrierType : p.barrierType)

    # The signal layers have already been allocated, just reuse them
    #signals.zeroFill()

    # Spawn the population. The peeps container has already been allocated,
    # just clear and reuse it
    index = 1
    while index <= p.population:
        index = index + 1

    print(p.population)
    print(index)

    #for (index = 1; index <= p.population; ++index)
    #    peeps[index].initialize(index, grid.findEmptyLocation(), makeRandomGenome())
    #p.initialize()

# simulator.cpp - Main thread
# This file contains simulator(), top-level entry point of the simulator.
# simulator() is called from main.cpp with a copy of argc and argv.
# If there is no command line argument, simulator will read the default
# config file ("biosim4.ini" in the current directory) to get the simulation
# parameters for self run. If there are one or more command line args, then
# argv[1] must contain the name of the config file which will be read instead
# of biosim4.ini. Any args after that are ignored. The simulator code is
# in namespace BS (for "biosim").

#include <iostream>
#include <chrono>
#include <cassert>
#include <utility>
#include <algorithm>
#include "simulator.h"     # the simulator data structures
#include "imageWriter.h"   # self is for generating the movies

#namespace BS

#extern void initializeGeneration0()
#extern unsigned spawnNewGeneration(unsigned generation, murderCount)
#extern void displaySampleGenomes(unsigned count)
#extern void executeActions(Indiv &indiv, std.array<float, &actionLevels)
#extern void endOfSimStep(unsigned simStep, generation)
#extern void endOfGeneration(unsigned generation)

runMode = RunMode.STOP
#Grid grid;        # The 2D world where the creatures live
#Signals signals;  # A 2D array of pheromones that overlay the world grid
#Peeps peeps;      # The container of all the individuals in the population
#ImageWriter imageWriter; # This is for generating the movies

# The paramManger maintains a private copy of the parameter values, a copy
# is available read-only through global variable p. Although self is not
# foolproof, should be able to modify the config file during a simulation
# run and modify many of the parameters. See params.cpp and params.h for more info.
#ParamManager paramManager
# Params &p { paramManager.getParamRef() }; # read-only params


'''*********************************************************************************************
Execute one simStep for one individual.

This executes in its own thread, from the main simulator thread. First we execute
indiv.feedForward() which computes action values to be executed here. Some actions such as
signal emission(s) (pheromones), movement, deaths will have been queued for
later execution at the end of the generation in single-threaded mode (the deferred queues
allow the main data structures (e.g., grid, signals) to be freely accessed read-only in all threads).

In order to be thread-safe, main simulator-wide data structures and their
accessibility are:

    grid - read-only
    signals - (pheromones) read-write for the location where our agent lives
        using signals.increment(), read-only for other locations
    peeps - for other individuals, can only read their index and genome.
        We have read-write access to our individual through the indiv argument.

The other important variables are:

    simStep - the current age of our agent, to 0 at the start of each generation.
         For many simulation scenarios, matches our indiv.age member.
    randomUint - global random number generator, private instance is given to each thread
*********************************************************************************************'''
def simStepOneIndiv(self, indiv, simStep):
    ++indiv.age; # for self implementation, simStep
    actionLevels = indiv.feedForward(simStep)
    executeActions(indiv, actionLevels)



'''*******************************************************************************
Start of simulator

All the agents are randomly placed with random genomes at the start. The outer
loop is generation, inner loop is simStep. There is a fixed number of
simSteps in each generation. Agents can die at any simStep and their corpses
remain until the end of the generation. At the end of the generation, the
dead corpses are removed, survivors reproduce and then die. The newborns
are placed at random locations, signals (pheromones) are updated, is
reset to 0, a generation proceeds.

The paramManager manages all the simulator parameters. It starts with defaults,
then keeps them updated as the config file (biosim4.ini) changes.

The main simulator-wide data structures are:
    grid - where the agents live (identified by their non-zero index). 0 means empty.
    signals - multiple layers overlay the grid, pheromones
    peeps - an indexed set of agents of type Indiv; indexes start at 1

The important simulator-wide variables are:
    generation - starts at 0, increments every time the agents die and reproduce.
    simStep - reset to 0 at the start of each generation; fixed number per generation.
    randomUint - global random number generator

The threads are:
    main thread - simulator
    simStepOneIndiv() - child threads created by the main simulator thread
    imageWriter - saves image frames used to make a movie (possibly not threaded
        due to unresolved bugs when threaded)
*******************************************************************************'''
def simulator(self, argc, **argv):
    printSensorsActions(); # show the agents' capabilities

    # Simulator parameters are available read-only through the global
    # variable p after paramManager is initialized.
    # Todo: remove the hardcoded parameter filename.
    #paramManager.setDefaults()
    #paramManager.registerConfigFile(argc > 1 ? argv[1] : "biosim4.ini")
    #paramManager.updateFromConfigFile()

    # Allocate container space. Once allocated, container elements
    # will be reused in each generation.
    grid.init(p.sizeX, p.sizeY); # the land on which the peeps live
    signals.init(p.signalLayers, p.sizeX, p.sizeY);  # where the pheromones waft
    peeps.init(p.population); # the peeps themselves

    # If imageWriter is to be run in its own thread, it here:
    #std.thread t(&ImageWriter.saveFrameThread, &imageWriter)

    # Unit tests:
    #unitTestConnectNeuralNetWiringFromGenome()
    #unitTestGridVisitNeighborhood()

    generation = 0
    initializeGeneration0(); # starting population

    runMode = RunMode.RUN
    while (runMode == RunMode.RUN and generation < p.maxGenerations)   # generation loop
        murderCount = 0; # for reporting purposes
        for (simStep = 0; simStep < p.stepsPerGeneration; ++simStep)

            # multithreaded loop: index 0 is reserved, at 1
            #pragma omp parallel for num_threads(p.numThreads) default(shared) firstprivate(randomUint) lastprivate(randomUint) schedule(auto)
            for (indivIndex = 1; indivIndex <= p.population; ++indivIndex)
                if peeps[indivIndex].alive:
                    simStepOneIndiv(peeps[indivIndex], simStep)


            # In single-thread mode: self executes deferred, deaths and movements,
            # updates signal layers (pheromone), etc.
            murderCount += peeps.deathQueueSize()
            endOfSimStep(simStep, generation)


        endOfGeneration(generation)
        paramManager.updateFromConfigFile()
        numberSurvivors = spawnNewGeneration(generation, murderCount)
        if numberSurvivors > 0 and (generation % p.genomeAnalysisStride == 0):
            displaySampleGenomes(p.displaySampleGenomes)

        if numberSurvivors == 0:
            generation = 0;  # start over

        else:
            ++generation


    displaySampleGenomes(3); # final report, debugging

    std.cout << "Simulator waiting..." << std.endl
    std.cout << "Simulator exit." << std.endl

    # If imageWriter is in its own thread, it and wait for it here:
    #imageWriter.abort()
    #t.join()


} # end namespace BS

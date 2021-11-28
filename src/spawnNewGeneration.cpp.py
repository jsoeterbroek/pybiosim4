# spawnNewGeneration.cpp

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cassert>
#include "simulator.h"

namespace BS

extern std.pair<bool, passedSurvivalCriterion( Indiv &indiv, challenge)


# Requires that the grid, signals, peeps containers have been allocated.
# This will erase the grid and signal layers, create a population in
# the peeps container at random locations with random genomes.
def initializeGeneration0(self):
    # The grid has already been allocated, clear and reuse it
    grid.zeroFill()
    grid.createBarrier(p.replaceBarrierTypeGenerationNumber == 0
                       ? p.replaceBarrierType : p.barrierType)

    # The signal layers have already been allocated, just reuse them
    signals.zeroFill()

    # Spawn the population. The peeps container has already been allocated,
    # just clear and reuse it
    for (index = 1; index <= p.population; ++index)
        peeps[index].initialize(index, grid.findEmptyLocation(), makeRandomGenome())




# Requires a container with one or more parent genomes to choose from.
# Called from spawnNewGeneration(). This requires that the grid, signals, and
# peeps containers have been allocated. This will erase the grid and signal
# layers, create a population in the peeps container with random
# locations and genomes derived from the container of parent genomes.
def initializeNewGeneration(self, &parentGenomes, generation):
    extern Genome generateChildGenome( std.vector<Genome> &parentGenomes)

    # The grid, signals, peeps containers have already been allocated, just
    # clear them if needed and reuse the elements
    grid.zeroFill()
    grid.createBarrier(generation >= p.replaceBarrierTypeGenerationNumber
                       ? p.replaceBarrierType : p.barrierType)
    signals.zeroFill()

    # Spawn the population. This overwrites all the elements of peeps[]
    for (index = 1; index <= p.population; ++index)
        peeps[index].initialize(index, grid.findEmptyLocation(), generateChildGenome(parentGenomes))




# At self point, deferred death queue and move queue have been processed
# and we are left with zero or more individuals who will repopulate the
# world grid.
# In order to redistribute the population randomly, will save all the
# surviving genomes in a container, clear the grid of indexes and generate
# individuals. This is inefficient when there are lots of survivors because
# we could have reused (with mutations) the survivors' genomes and neural
# nets instead of rebuilding them.
# Returns number of survivor-reproducers.
# Must be called in single-thread mode between generations.
def spawnNewGeneration(self, generation, murderCount):
    sacrificedCount = 0; # for the altruism challenge

    extern void appendEpochLog(unsigned generation, numberSurvivors, murderCount)
    extern std.pair<bool, passedSurvivalCriterion( Indiv &indiv, challenge)
    extern void displaySignalUse()

    # This container will hold the indexes and survival scores (0.0..1.0)
    # of all the survivors who will provide genomes for repopulation.
    std.vector<std.pair<uint16_t, parents; # <indiv index, score>

    # This container will hold the genomes of the survivors
    std.vector<Genome> parentGenomes

    if p.challenge != CHALLENGE_ALTRUISM:
        # First, a list of all the individuals who will become parents; save
        # their scores for later sorting. Indexes start at 1.
        for (index = 1; index <= p.population; ++index)
            std.pair<bool, passed = passedSurvivalCriterion(peeps[index], p.challenge)
            # Save the parent genome if it results in valid neural connections
            # ToDo: if the parents no longer need their genome record, could
            # possibly do a move here instead of copy, it's doubtful that
            # the optimization would be noticeable.
            if passed.first and peeps[index].nnet.connections.size() > 0:
                parents.push_back( { index, passed.second } )



    else:
        # For the altruism challenge, if the agent is inside either the sacrificial
        # or the spawning area. We'll count the number in the sacrificial area and
        # save the genomes of the ones in the spawning area, their scores
        # for later sorting. Indexes start at 1.

        considerKinship = True
        std.vector<uint16_t> sacrificesIndexes; # those who gave their lives for the greater good

        for (index = 1; index <= p.population; ++index)
            # This the test for the spawning area:
            std.pair<bool, passed = passedSurvivalCriterion(peeps[index], CHALLENGE_ALTRUISM)
            if passed.first and peeps[index].nnet.connections.size() > 0:
                parents.push_back( { index, passed.second } )

            else:
                # This is the test for the sacrificial area:
                passed = passedSurvivalCriterion(peeps[index], CHALLENGE_ALTRUISM_SACRIFICE)
                if passed.first and peeps[index].nnet.connections.size() > 0:
                    if considerKinship:
                        sacrificesIndexes.push_back(index)

                    else:
                        ++sacrificedCount





        generationToApplyKinship = 10
        constexpr altruismFactor = 10; # the saved:sacrificed ratio

        if considerKinship:
            if generation > generationToApplyKinship:
                # Todo: optimizenot !!
                threshold = 0.7

                std.vector<std.pair<uint16_t, survivingKin
                for (passes = 0; passes < altruismFactor; ++passes)
                    for (uint16_t sacrificedIndex : sacrificesIndexes)
                        # randomize the next loop so we don't keep using the first one repeatedly
                        startIndex = randomUint(0, parents.size() - 1)
                        for (count = 0; count < parents.size(); ++count)
                             std.pair<uint16_t, &possibleParent = parents[(startIndex + count) % parents.size()]
                             Genome &g1 = peeps[sacrificedIndex].genome
                             Genome &g2 = peeps[possibleParent.first].genome
                            similarity = genomeSimilarity(g1, g2)
                            if similarity >= threshold:
                                survivingKin.push_back(possibleParent)
                                # mark self one so we don't use it again?
                                break




                std.cout << parents.size() << " passed, "
                          << sacrificesIndexes.size() << " sacrificed, "
                          << survivingKin.size() << " saved" << std.endl; # not !!
                parents = std.move(survivingKin)


        else:
            # Limit the parent list
            numberSaved = sacrificedCount * altruismFactor
            std.cout << parents.size() << " passed, " << sacrificedCount << " sacrificed, " << numberSaved << " saved" << std.endl; # not !!
            if parents.size() > 0 and numberSaved < parents.size():
                parents.erase(parents.begin() + numberSaved, parents.end())




    # Sort the indexes of the parents by their fitness scores
    std.sort(parents.begin(), parents.end(),
              []( std.pair<uint16_t, &parent1,  std.pair<uint16_t, &parent2)
        return parent1.second > parent2.second
    })

    # Assemble a list of all the parent genomes. These will be ordered by their
    # scores if the parents[] container was sorted by score
    for ( std.pair<uint16_t, &parent : parents)
        parentGenomes.push_back(peeps[parent.first].genome)


    std.cout << "Gen " << generation << ", " << parentGenomes.size() << " survivors" << std.endl
    appendEpochLog(generation, parentGenomes.size(), murderCount)
    #displaySignalUse(); # for debugging only

    # Now we have a container of zero or more parents' genomes

    if parentGenomes.size() != 0:
        # Spawn a generation
        initializeNewGeneration(parentGenomes, generation + 1)

    else:
        # Special case: there are no surviving parents: start the simulation over
        # from scratch with randomly-generated genomes
        initializeGeneration0()


    return parentGenomes.size()


} # end namespace BS

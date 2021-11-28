# peeps.cpp
# Manages a container of individual agents of type Indiv and their
# locations in the grid container

#include <iostream>
#include <cassert>
#include <numeric>
#include <utility>
#include "simulator.h"

namespace BS


Peeps.Peeps()



def init(self, population):
    # Index 0 is reserved, add one:
    individuals.resize(population + 1)



# Safe to call during multithread mode.
# Indiv will remain alive and in-world until end of sim step when
# drainDeathQueue() is called.
def queueForDeath(self, &indiv):
    #pragma omp critical
        deathQueue.push_back(indiv.index)




# Called in single-thread mode at end of sim step. This executes all the
# queued deaths, the dead agents from the grid.
def drainDeathQueue(self):
    for (uint16_t index : deathQueue)
        auto indiv = peeps[index]
        grid.set(indiv.loc, 0)
        indiv.alive = False

    deathQueue.clear()



# Safe to call during multithread mode. Indiv won't move until end
# of sim step when drainMoveQueue() is called.
def queueForMove(self, &indiv, newLoc):
    #pragma omp critical
        record = std.make_pair<uint16_t, Coord>(uint16_t(indiv.index), Coord(newLoc))
        moveQueue.push_back(record)




# Called in single-thread mode at end of sim step. This executes all the
# queued movements. Each movement is typically one 8-neighbor cell distance
# but self function can move an individual any arbitrary distance.
def drainMoveQueue(self):
    for (auto moveRecord : moveQueue)
        auto indiv = peeps[moveRecord.first]
        newLoc = moveRecord.second
        moveDir = (newLoc - indiv.loc).asDir()
        if grid.isEmptyAt(newLoc):
            grid.set(indiv.loc, 0)
            grid.set(newLoc, indiv.index)
            indiv.loc = newLoc
            indiv.lastMoveDir = moveDir


    moveQueue.clear()


} # end namespace BS

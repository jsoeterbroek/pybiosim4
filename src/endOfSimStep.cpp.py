# endOfSimStep.cpp

#include <iostream>
#include <cmath>
#include "simulator.h"
#include "imageWriter.h"

namespace BS

'''
At the end of each sim step, function is called in single-thread
mode to take care of several things:

1. We may kill off some agents if a "radioactive" scenario is in progress.
2. We may flag some agents as meeting some challenge criteria, such
   a scenario is in progress.
3. We then drain the deferred death queue.
4. We then drain the deferred movement queue.
5. We fade the signal layer(s) (pheromones).
6. We save the resulting world condition as a single image frame (if
   p.saveVideo is True).
'''

def endOfSimStep(self, simStep, generation):
    if p.challenge == CHALLENGE_RADIOACTIVE_WALLS:
        # During the first half of the generation, west wall is radioactive,
        # where X == 0. In the last half of the generation, east wall is
        # radioactive, X = the area width - 1. There's an exponential
        # falloff of the danger, off to zero at the arena half line.
        radioactiveX = (simStep < p.stepsPerGeneration / 2) ? 0 : p.sizeX - 1

        for (index = 1; index <= p.population; ++index)   # index 0 is reserved
            Indiv &indiv = peeps[index]
            distanceFromRadioactiveWall = std.abs(indiv.loc.x - radioactiveX)
            if distanceFromRadioactiveWall < p.sizeX / 2:
                chanceOfDeath = 1.0 / distanceFromRadioactiveWall
                if randomUint() / (float)RANDOM_UINT_MAX < chanceOfDeath:
                    peeps.queueForDeath(indiv)





    # If the individual is touching any wall, set its challengeFlag to True.
    # At the end of the generation, those with the flag True will reproduce.
    if p.challenge == CHALLENGE_TOUCH_ANY_WALL:
        for (index = 1; index <= p.population; ++index)   # index 0 is reserved
            Indiv &indiv = peeps[index]
            if (indiv.loc.x == 0 or indiv.loc.x == p.sizeX - 1
                    or indiv.loc.y == 0 or indiv.loc.y == p.sizeY - 1)
                indiv.challengeBits = True




    # If self challenge is enabled, individual gets a bit set in their challengeBits
    # member if they are within a specified radius of a barrier center. They have to
    # visit the barriers in sequential order.
    if p.challenge == CHALLENGE_LOCATION_SEQUENCE:
        radius = 9.0
        for (index = 1; index <= p.population; ++index)   # index 0 is reserved
            Indiv &indiv = peeps[index]
            for (n = 0; n < grid.getBarrierCenters().size(); ++n)
                bit = 1 << n
                if (indiv.challengeBits & bit) == 0:
                    if (indiv.loc - grid.getBarrierCenters()[n]).length() <= radius:
                        indiv.challengeBits |= bit

                    break





    peeps.drainDeathQueue()
    peeps.drainMoveQueue()
    signals.fade(0); # takes layerNum  todonot !!

    # saveVideoFrameSync() is the synchronous version of saveVideFrame()
    if (p.saveVideo and
            ((generation % p.videoStride) == 0
             or generation <= p.videoSaveFirstFrames
             or (generation >= p.replaceBarrierTypeGenerationNumber
                 and generation <= p.replaceBarrierTypeGenerationNumber + p.videoSaveFirstFrames)))
        if not imageWriter.saveVideoFrameSync(simStep, generation):
            std.cout << "imageWriter busy" << std.endl




} # end namespace BS

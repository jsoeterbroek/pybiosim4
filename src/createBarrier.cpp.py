# createBarrier.cpp

#include <cassert>
#include "simulator.h"

namespace BS

# This generates barrier points, are grid locations with value
# BARRIER. A list of barrier locations is saved in private member
# Grid.barrierLocations and, some scenarios, Grid.barrierCenters.
# Those members are available read-only with Grid.getBarrierLocations().
# This function assumes an empty grid. This is typically called by
# the main simulator thread after Grid.init() or Grid.zeroFill().

# This file typically is under constant development and change for
# specific scenarios.

def createBarrier(self, barrierType):
    barrierLocations.clear()
    barrierCenters.clear();  # used only for some barrier types

    drawBox = [&](int16_t minX, minY, maxX, maxY)
        for (x = minX; x <= maxX; ++x)
            for (y = minY; y <= maxY; ++y)
                grid.set(x, y, BARRIER)
                barrierLocations.push_back( {x, y} )




    switch(barrierType)
    case 0:
        return

    # Vertical bar in constant location
    case 1:
        minX = p.sizeX / 2
        maxX = minX + 1
        minY = p.sizeY / 4
        maxY = minY + p.sizeY / 2

        for (x = minX; x <= maxX; ++x)
            for (y = minY; y <= maxY; ++y)
                grid.set(x, y, BARRIER)
                barrierLocations.push_back( {x, y} )



    break

    # Vertical bar in random location
    case 2:
        minX = randomUint(20, p.sizeX - 20)
        maxX = minX + 1
        minY = randomUint(20, p.sizeY / 2 - 20)
        maxY = minY + p.sizeY / 2

        for (x = minX; x <= maxX; ++x)
            for (y = minY; y <= maxY; ++y)
                grid.set(x, y, BARRIER)
                barrierLocations.push_back( {x, y} )



    break

    # five blocks staggered
    case 3:
        blockSizeX = 2
        blockSizeY = p.sizeX / 3

        x0 = p.sizeX / 4 - blockSizeX / 2
        y0 = p.sizeY / 4 - blockSizeY / 2
        x1 = x0 + blockSizeX
        y1 = y0 + blockSizeY

        drawBox(x0, y0, x1, y1)
        x0 += p.sizeX / 2
        x1 = x0 + blockSizeX
        drawBox(x0, y0, x1, y1)
        y0 += p.sizeY / 2
        y1 = y0 + blockSizeY
        drawBox(x0, y0, x1, y1)
        x0 -= p.sizeX / 2
        x1 = x0 + blockSizeX
        drawBox(x0, y0, x1, y1)
        x0 = p.sizeX / 2 - blockSizeX / 2
        x1 = x0 + blockSizeX
        y0 = p.sizeY / 2 - blockSizeY / 2
        y1 = y0 + blockSizeY
        drawBox(x0, y0, x1, y1)
        return

    break

    # Horizontal bar in constant location
    case 4:
        minX = p.sizeX / 4
        maxX = minX + p.sizeX / 2
        minY = p.sizeY / 2 + p.sizeY / 4
        maxY = minY + 2

        for (x = minX; x <= maxX; ++x)
            for (y = minY; y <= maxY; ++y)
                grid.set(x, y, BARRIER)
                barrierLocations.push_back( {x, y} )



    break

    # Three floating islands -- different locations every generation
    case 5:
        radius = 3.0
        margin = 2 * (int)radius

        randomLoc = [&]()
#                return Coord( (int16_t)randomUint((int)radius + margin, p.sizeX - ((float)radius + margin)),
#                              (int16_t)randomUint((int)radius + margin, p.sizeY - ((float)radius + margin)) )
            return Coord( (int16_t)randomUint(margin, p.sizeX - margin),
                          (int16_t)randomUint(margin, p.sizeY - margin) )


        center0 = randomLoc()
        Coord center1
        Coord center2

        do
            center1 = randomLoc()

        while ((center0 - center1).length() < margin)

        do
            center2 = randomLoc()

        while ((center0 - center2).length() < margin or (center1 - center2).length() < margin)

        barrierCenters.push_back(center0)
        #barrierCenters.push_back(center1)
        #barrierCenters.push_back(center2)

        f = [&](Coord loc)
            grid.set(loc, BARRIER)
            barrierLocations.push_back(loc)


        visitNeighborhood(center0, radius, f)
        #visitNeighborhood(center1, radius, f)
        #visitNeighborhood(center2, radius, f)

    break

    # Spots, number, radius, locations
    case 6:
        numberOfLocations = 5
        radius = 5.0

        f = [&](Coord loc)
            grid.set(loc, BARRIER)
            barrierLocations.push_back(loc)


        verticalSliceSize = p.sizeY / (numberOfLocations + 1)

        for (n = 1; n <= numberOfLocations; ++n)
            loc = { (int16_t)(p.sizeX / 2),
                          (int16_t)(n * verticalSliceSize)

            visitNeighborhood(loc, radius, f)
            barrierCenters.push_back(loc)


    break

    default:
        assert(False)



} # end namespace BS

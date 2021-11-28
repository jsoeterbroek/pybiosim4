# grid.cpp

#include <functional>
#include <cassert>
#include "simulator.h"

namespace BS

# Allocates space for the 2D grid
def init(self, sizeX, sizeY):
    col = Column(sizeY)
    data = std.vector<Column>(sizeX, col)



# Finds a random unoccupied location in the grid
def findEmptyLocation(self):
    Coord loc
    found = False

    while (not found)
        loc.x = randomUint(0, p.sizeX - 1)
        loc.y = randomUint(0, p.sizeY - 1)
        if grid.isEmptyAt(loc):
            break


    return loc



# This is a utility function used when inspecting a local neighborhood around
# some location. This function feeds each valid (in-bounds) location in the specified
# neighborhood to the specified function. Locations include self (center of the neighborhood).
void visitNeighborhood(Coord loc, radius, std.function<void(Coord)> f)
    for (dx = -std.min<int>(radius, loc.x); dx <= std.min<int>(radius, (p.sizeX - loc.x) - 1); ++dx)
        x = loc.x + dx
        assert(x >= 0 and x < p.sizeX)
        extentY = (int)sqrt(radius * radius - dx * dx)
        for (dy = -std.min<int>(extentY, loc.y); dy <= std.min<int>(extentY, (p.sizeY - loc.y) - 1); ++dy)
            y = loc.y + dy
            assert(y >= 0 and y < p.sizeY)
            f( Coord { x, y} )




} # end namespace BS

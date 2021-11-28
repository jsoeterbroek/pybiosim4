# signals.cpp
# Manages layers of pheremones

#include <cstdint>
#include "simulator.h"

namespace BS

def init(self, numLayers, sizeX, sizeY):
    data = std.vector<Layer>(numLayers, Layer(sizeX, sizeY))



# Increases the specified location by centerIncreaseAmount,
# and increases the neighboring cells by neighborIncreaseAmount

# Is it ok that multiple readers are reading self container while
# self single thread is writing to it?  todonot !!
def increment(self, layerNum, loc):
    constexpr radius = 1.5
    constexpr centerIncreaseAmount = 2
    constexpr neighborIncreaseAmount = 1

    #pragma omp critical
        visitNeighborhood(loc, radius, [layerNum](Coord loc)
            if signals[layerNum][loc.x][loc.y] < SIGNAL_MAX:
                signals[layerNum][loc.x][loc.y] =
                    std.min<unsigned>(SIGNAL_MAX,
                                       signals[layerNum][loc.x][loc.y] + neighborIncreaseAmount)

        })

        if signals[layerNum][loc.x][loc.y] < SIGNAL_MAX:
            signals[layerNum][loc.x][loc.y] =
                std.min<unsigned>(SIGNAL_MAX,
                                   signals[layerNum][loc.x][loc.y] + centerIncreaseAmount)





# Fades the signals
def fade(self, layerNum):
    constexpr fadeAmount = 1

    for (x = 0; x < p.sizeX; ++x)
        for (y = 0; y < p.sizeY; ++y)
            if signals[layerNum][x][y] >= fadeAmount:
                signals[layerNum][x][y] -= fadeAmount;  # fade center cell

            else:
                signals[layerNum][x][y] = 0





} # end namespace BS

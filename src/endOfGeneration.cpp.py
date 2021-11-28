# endOfGeneration.cpp

#include <iostream>
#include <utility>
#include <cassert>
#include <cstdlib>
#include <algorithm>
#include "simulator.h"
#include "imageWriter.h"

namespace BS

# At the end of each generation, save a video file (if p.saveVideo is True) and
# print some genomic statistics to stdout (if p.updateGraphLog is True).

def endOfGeneration(self, generation):
        if (p.saveVideo and
                ((generation % p.videoStride) == 0
                 or generation <= p.videoSaveFirstFrames
                 or (generation >= p.replaceBarrierTypeGenerationNumber
                     and generation <= p.replaceBarrierTypeGenerationNumber + p.videoSaveFirstFrames)))
            imageWriter.saveGenerationVideo(generation)



        if p.updateGraphLog and (generation == 1 or ((generation % p.updateGraphLogStride) == 0)):
#pragma GCC diagnostic ignored "-Wunused-result"
            std.system(p.graphLogUpdateCommand.c_str())




} # end namespace BS

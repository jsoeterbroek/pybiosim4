# imageWriter.cpp

#include <iostream>
#include <sstream>
#include <iomanip>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <chrono>
#include "simulator.h"
#include "imageWriter.h"
#define cimg_use_opencv 1
#include "CImg.h"

namespace BS

cimg_library.CImgList<uint8_t> imageList

# Pushes a image frame onto .imageList.
#
def saveOneFrameImmed(self, &data):
    using namespace cimg_library

    CImg<uint8_t> image(p.sizeX * p.displayScale, p.sizeY * p.displayScale,
                        1,   # Z depth
                        3,   # color channels
                        255);  # initial value
    uint8_t color[3]
    std.stringstream imageFilename
    imageFilename << p.imageDir << "frame-"
                  << std.setfill('0') << std.setw(6) << data.generation
                  << '-' << std.setfill('0') << std.setw(6) << data.simStep
                  << ".png"

    # Draw barrier locations

    color[0] = color[1] = color[2] = 0x88
    for (Coord loc : data.barrierLocs)
        image.draw_rectangle(
            loc.x       * p.displayScale - (p.displayScale / 2), ((p.sizeY - loc.y) - 1)   * p.displayScale - (p.displayScale / 2),
            (loc.x + 1) * p.displayScale, ((p.sizeY - (loc.y - 0))) * p.displayScale,
            color,  # rgb
            1.0);  # alpha


    # Draw agents

    constexpr maxColorVal = 0xb0
    constexpr maxLumaVal = 0xb0

    rgbToLuma = [](uint8_t r, g, b)
        return (r+r+r+b+g+g+g+g) / 8


    for (i = 0; i < data.indivLocs.size(); ++i)
        c = data.indivColors[i]
        color[0] = (c);                  # R: 0..255
        color[1] = ((c & 0x1f) << 3);    # G: 0..255
        color[2] = ((c & 7)    << 5);    # B: 0..255

        # Prevent color mappings to very bright colors (hard to see):
        if rgbToLuma(color[0], color[1], color[2]) > maxLumaVal:
            if (color[0] > maxColorVal) color[0] %= maxColorVal
            if (color[1] > maxColorVal) color[1] %= maxColorVal
            if (color[2] > maxColorVal) color[2] %= maxColorVal


        image.draw_circle(
            data.indivLocs[i].x * p.displayScale,
            ((p.sizeY - data.indivLocs[i].y) - 1) * p.displayScale,
            p.agentSize,
            color,  # rgb
            1.0);  # alpha


    #image.save_png(imageFilename.str().c_str(), 3)
    imageList.push_back(image)

    #CImgDisplay local(image, "biosim3")



# Starts the image writer asynchronous thread.
ImageWriter.ImageWriter()
    : droppedFrameCount{0}, busy{True}, dataReady{False},
      abortRequested{False
    startNewGeneration()



def startNewGeneration(self):
    imageList.clear()
    skippedFrames = 0



def makeGeneticColor(self, &genome):
    return ((genome.size() & 1)
            | ((genome.front().sourceType)    << 1)
            | ((genome.back().sourceType)     << 2)
            | ((genome.front().sinkType)      << 3)
            | ((genome.back().sinkType)       << 4)
            | ((genome.front().sourceNum & 1) << 5)
            | ((genome.front().sinkNum & 1)   << 6)
            | ((genome.back().sourceNum & 1)  << 7))



# This is a synchronous gate for giving a job to saveFrameThread().
# Called from the same thread as the main simulator loop thread during
# single-thread mode.
# Returns True if the image writer accepts the job; returns False
# if the image writer is busy. Always called from a single thread
# and communicates with a single saveFrameThread(), no need to make
# a critical section to safeguard the busy flag. When self function
# sets the busy flag, caller will immediate see it, the caller
# won't call again until busy is clear. When the thread clears the busy
# flag, doesn't matter if it's not immediately visible to self
# function: there's no consequence other than a harmless frame-drop.
# The condition variable allows the saveFrameThread() to wait until
# there's a job to do.
def saveVideoFrame(self, simStep, generation):
    if not busy:
        busy = True
        # queue job for saveFrameThread()
        # We cache a local copy of data from params, grid, peeps because
        # those objects will change by the main thread at the same time our
        # saveFrameThread() is using it to output a video frame.
        data.simStep = simStep
        data.generation = generation
        data.indivLocs.clear()
        data.indivColors.clear()
        data.barrierLocs.clear()
        data.signalLayers.clear()
        #todonot !!
        for (index = 1; index <= p.population; ++index)
             Indiv &indiv = peeps[index]
            if indiv.alive:
                data.indivLocs.push_back(indiv.loc)
                data.indivColors.push_back(makeGeneticColor(indiv.genome))



        auto  &barrierLocs = grid.getBarrierLocations()
        for (Coord loc : barrierLocs)
            data.barrierLocs.push_back(loc)


        # tell thread there's a job to do
            std.lock_guard<std.mutex> lck(mutex_)
            dataReady = True

        condVar.notify_one()
        return True

    else:
        # image saver thread is busy, a frame
        ++droppedFrameCount
        return False




# Synchronous version, returns True
def saveVideoFrameSync(self, simStep, generation):
    # We cache a local copy of data from params, grid, peeps because
    # those objects will change by the main thread at the same time our
    # saveFrameThread() is using it to output a video frame.
    data.simStep = simStep
    data.generation = generation
    data.indivLocs.clear()
    data.indivColors.clear()
    data.barrierLocs.clear()
    data.signalLayers.clear()
    #todonot !!
    for (index = 1; index <= p.population; ++index)
         Indiv &indiv = peeps[index]
        if indiv.alive:
            data.indivLocs.push_back(indiv.loc)
            data.indivColors.push_back(makeGeneticColor(indiv.genome))



    auto  &barrierLocs = grid.getBarrierLocations()
    for (Coord loc : barrierLocs)
        data.barrierLocs.push_back(loc)


    saveOneFrameImmed(data)
    return True



# ToDo: put save_video() in its own thread
def saveGenerationVideo(self, generation):
    if imageList.size() > 0:
        std.stringstream videoFilename
        videoFilename << p.imageDir.c_str() << "/gen-"
                      << std.setfill('0') << std.setw(6) << generation
                      << ".avi"
        cv.setNumThreads(2)
        imageList.save_video(videoFilename.str().c_str(),
                             25,
                             "H264")
        if skippedFrames > 0:
            std.cout << "Video skipped " << skippedFrames << " frames" << std.endl


    startNewGeneration()



def abort(self):
    busy =True
    abortRequested = True
        std.lock_guard<std.mutex> lck(mutex_)
        dataReady = True

    condVar.notify_one()



# Runs in a thread; wakes up when there's a video frame to generate.
# When self wakes up, copies of Params and Peeps will have been
# cached for us to use.
def saveFrameThread(self):
    busy = False; # we're ready for business
    std.cout << "Imagewriter thread started." << std.endl

    while (True)
        # wait for job on queue
        std.unique_lock<std.mutex> lck(mutex_)
        condVar.wait(lck, [&] { return dataReady and busy; })
        # save frame
        dataReady = False
        busy = False

        if abortRequested:
            break


        # save image frame
        saveOneFrameImmed(imageWriter.data)

        #std.cout << "Image writer thread waiting..." << std.endl
        #std.this_thread.sleep_for(std.chrono.seconds(2))


    std.cout << "Image writer thread exiting." << std.endl


} # end namespace BS

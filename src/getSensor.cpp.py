# getSensor.cpp

#include <iostream>
#include <cassert>
#include <cmath>
#include "simulator.h"

namespace BS

def getPopulationDensityAlongAxis(self, loc, dir):
    # Converts the population along the specified axis to the sensor range. The
    # locations of neighbors are scaled by the inverse of their distance times
    # the positive absolute cosine of the difference of their angle and the
    # specified axis. The maximum positive or negative magnitude of the sum is
    # about 2*radius. We don't adjust for being close to a border, populations
    # along borders and in corners are commonly sparser than away from borders.
    # An empty neighborhood results in a sensor value exactly midrange; below
    # midrange if the population density is greatest in the reverse direction,
    # above midrange if density is greatest in forward direction.

    sum = 0.0
    f = [&](Coord tloc)
        if tloc != loc and grid.isOccupiedAt(tloc):
            offset = tloc - loc
            anglePosCos = offset.raySameness(dir)
            dist = std.sqrt((double)offset.x * offset.x + (double)offset.y * offset.y)
            contrib = (1.0 / dist) * anglePosCos
            sum += contrib



    visitNeighborhood(loc, p.populationSensorRadius, f)
    maxSumMag = 6.0 * p.populationSensorRadius
    assert(sum >= -maxSumMag and sum <= maxSumMag)

    double sensorVal
    sensorVal = sum / maxSumMag; # convert to -1.0..1.0
    sensorVal = (sensorVal + 1.0) / 2.0; # convert to 0.0..1.0

    return sensorVal



# Converts the number of locations (not including loc) to the next barrier location
# along opposite directions of the specified axis to the sensor range. If no barriers
# are found, result is sensor mid-range. Ignores agents in the path.
def getShortProbeBarrierDistance(self, loc0, dir, probeDistance):
    countFwd = 0
    countRev = 0
    loc = loc0 + dir
    numLocsToTest = probeDistance
    # Scan positive direction
    while (numLocsToTest > 0 and grid.isInBounds(loc) and not grid.isBarrierAt(loc))
        ++countFwd
        loc = loc + dir
        --numLocsToTest

    if numLocsToTest > 0 and not grid.isInBounds(loc):
        countFwd = probeDistance

    # Scan negative direction
    numLocsToTest = probeDistance
    loc = loc0 - dir
    while (numLocsToTest > 0 and grid.isInBounds(loc) and not grid.isBarrierAt(loc))
        ++countRev
        loc = loc - dir
        --numLocsToTest

    if numLocsToTest > 0 and not grid.isInBounds(loc):
        countRev = probeDistance


    sensorVal = ((countFwd - countRev) + probeDistance); # convert to 0..2*probeDistance
    sensorVal = (sensorVal / 2.0) / probeDistance; # convert to 0.0..1.0
    return sensorVal



def getSignalDensity(self, layerNum, loc):
    # returns magnitude of the specified signal layer in a neighborhood, with
    # 0.0..maxSignalSum converted to the sensor range.

    countLocs = 0
    unsigned sum = 0
    center = loc

    f = [&](Coord tloc)
        ++countLocs
        sum += signals.getMagnitude(layerNum, tloc)


    visitNeighborhood(center, p.signalSensorRadius, f)
    maxSum = (float)countLocs * SIGNAL_MAX
    sensorVal = sum / maxSum; # convert to 0.0..1.0

    return sensorVal



def getSignalDensityAlongAxis(self, layerNum, loc, dir):
    # Converts the signal density along the specified axis to sensor range. The
    # values of cell signal levels are scaled by the inverse of their distance times
    # the positive absolute cosine of the difference of their angle and the
    # specified axis. The maximum positive or negative magnitude of the sum is
    # about 2*radius*SIGNAL_MAX (?). We don't adjust for being close to a border,
    # so signal densities along borders and in corners are commonly sparser than
    # away from borders.

    sum = 0.0
    f = [&](Coord tloc)
        if tloc != loc:
            offset = tloc - loc
            anglePosCos = offset.raySameness(dir)
            dist = std.sqrt((double)offset.x * offset.x + (double)offset.y * offset.y)
            contrib = (1.0 / dist) * anglePosCos * signals.getMagnitude(layerNum, loc)
            sum += contrib



    visitNeighborhood(loc, p.signalSensorRadius, f)
    maxSumMag = 6.0 * p.signalSensorRadius * SIGNAL_MAX
    assert(sum >= -maxSumMag and sum <= maxSumMag)
    sensorVal = sum / maxSumMag; # convert to -1.0..1.0
    sensorVal = (sensorVal + 1.0) / 2.0; # convert to 0.0..1.0

    return sensorVal



# Returns the number of locations to the next agent in the specified
# direction, including loc. If the probe encounters a boundary or a
# barrier before reaching the longProbeDist distance, longProbeDist.
# Returns 0..longProbeDist.
def longProbePopulationFwd(self, loc, dir, longProbeDist):
    assert(longProbeDist > 0)
    count = 0
    loc = loc + dir
    numLocsToTest = longProbeDist
    while (numLocsToTest > 0 and grid.isInBounds(loc) and grid.isEmptyAt(loc))
        ++count
        loc = loc + dir
        --numLocsToTest

    if numLocsToTest > 0 and (not grid.isInBounds(loc) or grid.isBarrierAt(loc)):
        return longProbeDist

    else:
        return count




# Returns the number of locations to the next barrier in the
# specified direction, including loc. Ignores agents in the way.
# If the distance to the border is less than the longProbeDist distance
# and no barriers are found, longProbeDist.
# Returns 0..longProbeDist.
def longProbeBarrierFwd(self, loc, dir, longProbeDist):
    assert(longProbeDist > 0)
    count = 0
    loc = loc + dir
    numLocsToTest = longProbeDist
    while (numLocsToTest > 0 and grid.isInBounds(loc) and not grid.isBarrierAt(loc))
        ++count
        loc = loc + dir
        --numLocsToTest

    if numLocsToTest > 0 and not grid.isInBounds(loc):
        return longProbeDist

    else:
        return count




# Returned sensor values range SENSOR_MIN..SENSOR_MAX
def getSensor(self, sensorNum, simStep):
    sensorVal = 0.0

    switch (sensorNum)
    case Sensor.AGE:
        # Converts age (units of simSteps compared to life expectancy)
        # linearly to normalized sensor range 0.0..1.0
        sensorVal = (float)age / p.stepsPerGeneration
        break
    case Sensor.BOUNDARY_DIST:
        # Finds closest boundary, that to the max possible dist
        # to a boundary from the center, converts that linearly to the
        # sensor range 0.0..1.0
        distX = std.min<int>(loc.x, (p.sizeX - loc.x) - 1)
        distY = std.min<int>(loc.y, (p.sizeY - loc.y) - 1)
        closest = std.min<int>(distX, distY)
        maxPossible = std.max<int>(p.sizeX / 2 - 1, p.sizeY / 2 - 1)
        sensorVal = (float)closest / maxPossible
        break

    case Sensor.BOUNDARY_DIST_X:
        # Measures the distance to nearest boundary in the east-west axis,
        # max distance is half the grid width; scaled to sensor range 0.0..1.0.
        minDistX = std.min<int>(loc.x, (p.sizeX - loc.x) - 1)
        sensorVal = minDistX / (p.sizeX / 2.0)
        break

    case Sensor.BOUNDARY_DIST_Y:
        # Measures the distance to nearest boundary in the south-north axis,
        # max distance is half the grid height; scaled to sensor range 0.0..1.0.
        minDistY = std.min<int>(loc.y, (p.sizeY - loc.y) - 1)
        sensorVal = minDistY / (p.sizeY / 2.0)
        break

    case Sensor.LAST_MOVE_DIR_X:
        # X component -1,0, maps to sensor values 0.0, 0.5, 1.0
        lastX = lastMoveDir.asNormalizedCoord().x
        sensorVal = lastX == 0 ? 0.5 :
                    (lastX == -1 ? 0.0 : 1.0)
        break

    case Sensor.LAST_MOVE_DIR_Y:
        # Y component -1,0, maps to sensor values 0.0, 0.5, 1.0
        lastY = lastMoveDir.asNormalizedCoord().y
        sensorVal = lastY == 0 ? 0.5 :
                    (lastY == -1 ? 0.0 : 1.0)
        break

    case Sensor.LOC_X:
        # Maps current X location 0..p.sizeX-1 to sensor range 0.0..1.0
        sensorVal = (float)loc.x / (p.sizeX - 1)
        break
    case Sensor.LOC_Y:
        # Maps current Y location 0..p.sizeY-1 to sensor range 0.0..1.0
        sensorVal = (float)loc.y / (p.sizeY - 1)
        break
    case Sensor.OSC1:
        # Maps the oscillator sine wave to sensor range 0.0..1.0
        # cycles starts at simStep 0 for everbody.
        phase = (simStep % oscPeriod) / (float)oscPeriod; # 0.0..1.0
        factor = -std.cos(phase * 2.0f * 3.1415927f)
        assert(factor >= -1.0f and factor <= 1.0f)
        factor += 1.0f;    # convert to 0.0..2.0
        factor /= 2.0;     # convert to 0.0..1.0
        sensorVal = factor
        # Clip any round-off error
        sensorVal = std.min<float>(1.0, std.max<float>(0.0, sensorVal))
        break

    case Sensor.LONGPROBE_POP_FWD:
        # Measures the distance to the nearest other individual in the
        # forward direction. If non found, the maximum sensor value.
        # Maps the result to the sensor range 0.0..1.0.
        sensorVal = longProbePopulationFwd(loc, lastMoveDir, longProbeDist) / (float)longProbeDist; # 0..1
        break

    case Sensor.LONGPROBE_BAR_FWD:
        # Measures the distance to the nearest barrier in the forward
        # direction. If non found, the maximum sensor value.
        # Maps the result to the sensor range 0.0..1.0.
        sensorVal = longProbeBarrierFwd(loc, lastMoveDir, longProbeDist) / (float)longProbeDist; # 0..1
        break

    case Sensor.POPULATION:
        # Returns population density in neighborhood converted linearly from
        # 0..100% to sensor range
        countLocs = 0
        countOccupied = 0
        center = loc

        f = [&](Coord tloc)
            ++countLocs
            if grid.isOccupiedAt(tloc):
                ++countOccupied



        visitNeighborhood(center, p.populationSensorRadius, f)
        sensorVal = (float)countOccupied / countLocs
        break

    case Sensor.POPULATION_FWD:
        # Sense population density along axis of last movement direction, mapped
        # to sensor range 0.0..1.0
        sensorVal = getPopulationDensityAlongAxis(loc, lastMoveDir)
        break
    case Sensor.POPULATION_LR:
        # Sense population density along an axis 90 degrees from last movement direction
        sensorVal = getPopulationDensityAlongAxis(loc, lastMoveDir.rotate90DegCW())
        break
    case Sensor.BARRIER_FWD:
        # Sense the nearest barrier along axis of last movement direction, mapped
        # to sensor range 0.0..1.0
        sensorVal = getShortProbeBarrierDistance(loc, lastMoveDir, p.shortProbeBarrierDistance)
        break
    case Sensor.BARRIER_LR:
        # Sense the nearest barrier along axis perpendicular to last movement direction, mapped
        # to sensor range 0.0..1.0
        sensorVal = getShortProbeBarrierDistance(loc, lastMoveDir.rotate90DegCW(), p.shortProbeBarrierDistance)
        break
    case Sensor.RANDOM:
        # Returns a random sensor value in the range 0.0..1.0.
        sensorVal = randomUint() / (float)UINT_MAX
        break
    case Sensor.SIGNAL0:
        # Returns magnitude of signal0 in the local neighborhood, with
        # 0.0..maxSignalSum converted to sensorRange 0.0..1.0
        sensorVal = getSignalDensity(0, loc)
        break
    case Sensor.SIGNAL0_FWD:
        # Sense signal0 density along axis of last movement direction
        sensorVal = getSignalDensityAlongAxis(0, loc, lastMoveDir)
        break
    case Sensor.SIGNAL0_LR:
        # Sense signal0 density along an axis perpendicular to last movement direction
        sensorVal = getSignalDensityAlongAxis(0, loc, lastMoveDir.rotate90DegCW())
        break
    case Sensor.GENETIC_SIM_FWD:
        # Return minimum sensor value if nobody is alive in the forward adjacent location,
        # else returns a similarity match in the sensor range 0.0..1.0
        loc2 = loc + lastMoveDir
        if grid.isInBounds(loc2) and grid.isOccupiedAt(loc2):
             Indiv &indiv2 = peeps.getIndiv(loc2)
            if indiv2.alive:
                sensorVal = genomeSimilarity(genome, indiv2.genome); # 0.0..1.0


        break

    default:
        assert(False)
        break


    if std.isnan(sensorVal) or sensorVal < -0.01 or sensorVal > 1.01:
        std.cout << "sensorVal=" << (int)sensorVal << " for " << sensorName((Sensor)sensorNum) << std.endl
        sensorVal = std.max(0.0f, std.min(sensorVal, 1.0f)); # clip


    assert(not std.isnan(sensorVal) and sensorVal >= -0.01 and sensorVal <= 1.01)

    return sensorVal


} # end namespace BS

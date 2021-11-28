# survival-criteria.cpp

#include <cassert>
#include <utility>
#include "simulator.h"

namespace BS

# Returns True and a score 0.0..1.0 if passed, if failed
std.pair<bool, passedSurvivalCriterion( Indiv &indiv, challenge)
    if not indiv.alive:
        return { False, 0.0


    switch(challenge)

    # Survivors are those inside the circular area defined by
    # safeCenter and radius
    case CHALLENGE_CIRCLE:
        Coord safeCenter { (int16_t)(p.sizeX / 4.0), (int16_t)(p.sizeY / 4.0)
        radius = p.sizeX / 4.0

        offset = safeCenter - indiv.loc
        distance = offset.length()
        return distance <= radius ?
               std.pair<bool, float> { True, (radius - distance) / radius
               :
               std.pair<bool, float> { False, 0.0


    # Survivors are all those on the right side of the arena
    case CHALLENGE_RIGHT_HALF:
        return indiv.loc.x > p.sizeX / 2 ?
               std.pair<bool, float> { True, 1.0
               :
               std.pair<bool, float> { False, 0.0

    # Survivors are all those on the right quarter of the arena
    case CHALLENGE_RIGHT_QUARTER:
        return indiv.loc.x > p.sizeX / 2 + p.sizeX / 4 ?
               std.pair<bool, float> { True, 1.0
               :
               std.pair<bool, float> { False, 0.0

    # Survivors are all those on the left eighth of the arena
    case CHALLENGE_LEFT_EIGHTH:
        return indiv.loc.x < p.sizeX / 8 ?
               std.pair<bool, float> { True, 1.0
               :
               std.pair<bool, float> { False, 0.0

    # Survivors are those not touching the border and with exactly the number
    # of neighbors defined by neighbors and radius, neighbors includes self
    case CHALLENGE_STRING:
        minNeighbors = 22
        maxNeighbors = 2
        radius = 1.5

        if grid.isBorder(indiv.loc):
            return { False, 0.0


        count = 0
        f = [&](Coord loc2)
            if (grid.isOccupiedAt(loc2)) ++count


        visitNeighborhood(indiv.loc, radius, f)
        if count >= minNeighbors and count <= maxNeighbors:
            return { True, 1.0

        else:
            return { False, 0.0



    # Survivors are those within the specified radius of the center. The score
    # is linearly weighted by distance from the center.
    case CHALLENGE_CENTER_WEIGHTED:
        Coord safeCenter { (int16_t)(p.sizeX / 2.0), (int16_t)(p.sizeY / 2.0)
        radius = p.sizeX / 3.0

        offset = safeCenter - indiv.loc
        distance = offset.length()
        return distance <= radius ?
               std.pair<bool, float> { True, (radius - distance) / radius
               :
               std.pair<bool, float> { False, 0.0


    # Survivors are those within the specified radius of the center
    case CHALLENGE_CENTER_UNWEIGHTED:
        Coord safeCenter { (int16_t)(p.sizeX / 2.0), (int16_t)(p.sizeY / 2.0)
        radius = p.sizeX / 3.0

        offset = safeCenter - indiv.loc
        distance = offset.length()
        return distance <= radius ?
               std.pair<bool, float> { True, 1.0
               :
               std.pair<bool, float> { False, 0.0


    # Survivors are those within the specified outer radius of the center and with
    # the specified number of neighbors in the specified inner radius.
    # The score is not weighted by distance from the center.
    case CHALLENGE_CENTER_SPARSE:
        Coord safeCenter { (int16_t)(p.sizeX / 2.0), (int16_t)(p.sizeY / 2.0)
        outerRadius = p.sizeX / 4.0
        innerRadius = 1.5
        minNeighbors = 5;  # includes self
        maxNeighbors = 8

        offset = safeCenter - indiv.loc
        distance = offset.length()
        if distance <= outerRadius:
            count = 0
            f = [&](Coord loc2)
                if (grid.isOccupiedAt(loc2)) ++count


            visitNeighborhood(indiv.loc, innerRadius, f)
            if count >= minNeighbors and count <= maxNeighbors:
                return { True, 1.0


        return { False, 0.0


    # Survivors are those within the specified radius of any corner.
    # Assumes square arena.
    case CHALLENGE_CORNER:
        assert(p.sizeX == p.sizeY)
        radius = p.sizeX / 8.0

        distance = (Coord(0, 0) - indiv.loc).length()
        if distance <= radius:
            return { True, 1.0

        distance = (Coord(0, p.sizeY - 1) - indiv.loc).length()
        if distance <= radius:
            return { True, 1.0

        distance = (Coord(p.sizeX - 1, 0) - indiv.loc).length()
        if distance <= radius:
            return { True, 1.0

        distance = (Coord(p.sizeX - 1, p.sizeY - 1) - indiv.loc).length()
        if distance <= radius:
            return { True, 1.0

        return { False, 0.0


    # Survivors are those within the specified radius of any corner. The score
    # is linearly weighted by distance from the corner point.
    case CHALLENGE_CORNER_WEIGHTED:
        assert(p.sizeX == p.sizeY)
        radius = p.sizeX / 4.0

        distance = (Coord(0, 0) - indiv.loc).length()
        if distance <= radius:
            return { True, (radius - distance) / radius

        distance = (Coord(0, p.sizeY - 1) - indiv.loc).length()
        if distance <= radius:
            return { True, (radius - distance) / radius

        distance = (Coord(p.sizeX - 1, 0) - indiv.loc).length()
        if distance <= radius:
            return { True, (radius - distance) / radius

        distance = (Coord(p.sizeX - 1, p.sizeY - 1) - indiv.loc).length()
        if distance <= radius:
            return { True, (radius - distance) / radius

        return { False, 0.0


    # This challenge is handled in endOfSimStep(), individuals may die
    # at the end of any sim step. There is nothing else to do here at the
    # end of a generation. All remaining alive become parents.
    case CHALLENGE_RADIOACTIVE_WALLS:
        return { True, 1.0

    # Survivors are those touching any wall at the end of the generation
    case CHALLENGE_AGAINST_ANY_WALL:
        onEdge = indiv.loc.x == 0 or indiv.loc.x == p.sizeX - 1
                      or indiv.loc.y == 0 or indiv.loc.y == p.sizeY - 1

        if onEdge:
            return { True, 1.0

        else:
            return { False, 0.0



    # This challenge is partially handled in endOfSimStep(), individuals
    # that are touching a wall are flagged in their Indiv record. They are
    # allowed to continue living. Here at the end of the generation, that
    # never touch a wall will die. All that touched a wall at any time during
    # their life will become parents.
    case CHALLENGE_TOUCH_ANY_WALL:
        if indiv.challengeBits != 0:
            return { True, 1.0

        else:
            return { False, 0.0


    # Everybody survives and are candidate parents, scored by how far
    # they migrated from their birth location.
    case CHALLENGE_MIGRATE_DISTANCE:
        #requiredDistance = p.sizeX / 2.0
        distance = (indiv.loc - indiv.birthLoc).length()
        distance = distance / (float)(std.max(p.sizeX, p.sizeY))
        return { True, distance


    # Survivors are all those on the left or right eighths of the arena
    case CHALLENGE_EAST_WEST_EIGHTHS:
        return indiv.loc.x < p.sizeX / 8 or indiv.loc.x >= (p.sizeX - p.sizeX / 8)?
               std.pair<bool, float> { True, 1.0
               :
               std.pair<bool, float> { False, 0.0

    # Survivors are those within radius of any barrier center. Weighted by distance.
    case CHALLENGE_NEAR_BARRIER:
        float radius
        #radius = 20.0
        radius = p.sizeX / 2
        #radius = p.sizeX / 4

         std.vector<Coord> barrierCenters = grid.getBarrierCenters()
        minDistance = 1e8
        for (Coord center : barrierCenters)
            distance = (indiv.loc - center).length()
            if distance < minDistance:
                minDistance = distance


        if minDistance <= radius:
            return { True, 1.0 - (minDistance / radius)

        else:
            return { False, 0.0



    # Survivors are those not touching a border and with exactly one neighbor which has no other neighbor
    case CHALLENGE_PAIRS:
        onEdge = indiv.loc.x == 0 or indiv.loc.x == p.sizeX - 1
                      or indiv.loc.y == 0 or indiv.loc.y == p.sizeY - 1

        if onEdge:
            return { False, 0.0


        count = 0
        for (x = indiv.loc.x - 1; x < indiv.loc.x + 1; ++x)
            for (y = indiv.loc.y - 1; y < indiv.loc.y + 1; ++y)
                tloc = { x, y
                if tloc != indiv.loc and grid.isInBounds(tloc) and grid.isOccupiedAt(tloc):
                    ++count
                    if count == 1:
                        for (x1 = tloc.x - 1; x1 < tloc.x + 1; ++x1)
                            for (y1 = tloc.y - 1; y1 < tloc.y + 1; ++y1)
                                tloc1 = { x1, y1
                                if tloc1 != tloc and tloc1 != indiv.loc and grid.isInBounds(tloc1) and grid.isOccupiedAt(tloc1):
                                    return { False, 0.0




                    else:
                        return { False, 0.0




        if count == 1:
            return { True, 1.0

        else:
            return { False, 0.0



    # Survivors are those that contacted one or more specified locations in a sequence,
    # ranked by the number of locations contacted. There will be a bit set in their
    # challengeBits member for each location contacted.
    case CHALLENGE_LOCATION_SEQUENCE:
        count = 0
        bits = indiv.challengeBits
        maxNumberOfBits = sizeof(bits) * 8

        for (n = 0; n < maxNumberOfBits; ++n)
            if (bits & (1 << n)) != 0:
                ++count


        if count > 0:
            return { True, count / (float)maxNumberOfBits

        else:
            return { False, 0.0


    break

    # Survivors are all those within the specified radius of the NE corner
    case CHALLENGE_ALTRUISM_SACRIFICE:
        #radius = p.sizeX / 3.0; # in 128^2 world, 1429 agents
        radius = p.sizeX / 4.0; # in 128^2 world, 804 agents
        #radius = p.sizeX / 5.0; # in 128^2 world, 514 agents

        distance = (Coord(p.sizeX - p.sizeX / 4, p.sizeY - p.sizeY / 4) - indiv.loc).length()
        if distance <= radius:
            return { True, (radius - distance) / radius

        else:
            return { False, 0.0



    # Survivors are those inside the circular area defined by
    # safeCenter and radius
    case CHALLENGE_ALTRUISM:
        Coord safeCenter { (int16_t)(p.sizeX / 4.0), (int16_t)(p.sizeY / 4.0)
        radius = p.sizeX / 4.0; # in a 128^2 world, 3216

        offset = safeCenter - indiv.loc
        distance = offset.length()
        return distance <= radius ?
               std.pair<bool, float> { True, (radius - distance) / radius
               :
               std.pair<bool, float> { False, 0.0


    default:
        assert(False)



} # end namespace BS

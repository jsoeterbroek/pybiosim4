# genome-compare.cpp -- compute similarity of two genomes

#include <cassert>
#include "simulator.h"

namespace BS

# Approximate gene match: Has to match same source, sink, similar weight
#
def genesMatch(self, &g1, &g2):
    return g1.sinkNum == g2.sinkNum
           and g1.sourceNum == g2.sourceNum
           and g1.sinkType == g2.sinkType
           and g1.sourceType == g2.sourceType
           and g1.weight == g2.weight



# The jaro_winkler_distance() function is adapted from the C version at
# https:#github.com/miguelvps/c/blob/master/jarowinkler.c
# under a GNU license, ver. 3. This comparison function is useful if
# the simulator allows genomes to change length, if genes are allowed
# to relocate to different offsets in the genome. I.e., function is
# tolerant of gaps, relocations, genomes of unequal lengths.
#
def jaro_winkler_distance(self, &genome1, &genome2):
    float dw
    max = [](int a, b)
        return a > b ? a : b

    min = [](int a, b)
        return a < b ? a : b


     auto &s = genome1
     auto &a = genome2

    int i, j, l
    m = 0, t = 0
    sl = s.size(); # strlen(s)
    al = a.size(); # strlen(a)

    constexpr maxNumGenesToCompare = 20
    sl = min(maxNumGenesToCompare, sl); # optimization: approximate for long genomes
    al = min(maxNumGenesToCompare, al)

    std.vector<int> sflags(sl, 0)
    std.vector<int> aflags(al, 0)
    range = max(0, max(sl, al) / 2 - 1)

    if not sl or not al:
        return 0.0

    ''' calculate matching characters '''
    for (i = 0; i < al; i++)
        for (j = max(i - range, 0), l = min(i + range + 1, sl); j < l; j++)
            if genesMatch(a[i], s[j]) and not sflags[j]:
                sflags[j] = 1
                aflags[i] = 1
                m++
                break




    if not m:
        return 0.0

    ''' calculate character transpositions '''
    l = 0
    for (i = 0; i < al; i++)
        if aflags[i] == 1:
            for (j = l; j < sl; j++)
                if sflags[j] == 1:
                    l = j + 1
                    break


            if not genesMatch(a[i], s[j]):
                t++


    t /= 2

    ''' Jaro distance '''
    dw = (((float)m / sl) + ((float)m / al) + ((float)(m - t) / m)) / 3.0f
    return dw



# Works only for genomes of equal length
def hammingDistanceBits(self, &genome1, &genome2):
    assert(genome1.size() == genome2.size())

     unsigned int *p1 = ( unsigned int *)genome1.data()
     unsigned int *p2 = ( unsigned int *)genome2.data()
     numElements = genome1.size()
     bytesPerElement = sizeof(genome1[0])
     lengthBytes = numElements * bytesPerElement
     lengthBits = lengthBytes * 8
    bitCount = 0

    for (index = 0; index < genome1.size(); ++p1, ++p2, ++index)
        bitCount += __builtin_popcount(*p1 ^ *p2)


    # For two completely random bit patterns, half the bits will differ,
    # resulting in c. 50% match. We will scale that by 2X to make the range
    # from 0 to 1.0. We clip the value to 1.0 in case the two patterns are
    # negatively correlated for some reason.
    return 1.0 - std.min(1.0, (2.0 * bitCount) / (float)lengthBits)



# Works only for genomes of equal length
def hammingDistanceBytes(self, &genome1, &genome2):
    assert(genome1.size() == genome2.size())

     unsigned int *p1 = ( unsigned int *)genome1.data()
     unsigned int *p2 = ( unsigned int *)genome2.data()
     numElements = genome1.size()
     bytesPerElement = sizeof(genome1[0])
     lengthBytes = numElements * bytesPerElement
    byteCount = 0

    for (index = 0; index < genome1.size(); ++p1, ++p2, ++index)
        byteCount += (unsigned)(*p1 == *p2)


    return byteCount / (float)lengthBytes



# Returns 0.0..1.0
#
# ToDo: optimize by approximation for long genomes
def genomeSimilarity(self, &g1, &g2):
    switch (p.genomeComparisonMethod)
    case 0:
        return jaro_winkler_distance(g1, g2)
    case 1:
        return hammingDistanceBits(g1, g2)
    case 2:
        return hammingDistanceBytes(g1, g2)
    default:
        assert(False)




# returns 0.0..1.0
# Samples random pairs of individuals regardless if they are alive or not
def geneticDiversity(self):
    if p.population < 2:
        return 0.0


    # count limits the number of genomes sampled for performance reasons.
    count = std.min(1000U, p.population);    # todo: not !not  p.analysisSampleSize
    numSamples = 0
    similaritySum = 0.0f

    while (count > 0)
        index0 = randomUint(1, p.population - 1); # skip first and last elements
        index1 = index0 + 1
        similaritySum += genomeSimilarity(peeps[index0].genome, peeps[index1].genome)
        --count
        ++numSamples

    diversity = 1.0f - (similaritySum / numSamples)
    return diversity


} # end namespace BS

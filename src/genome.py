# genome.cpp

#include <vector>
#include <map>
#include <list>
#include <iostream>
#include <cassert>
#include <string>
#include "simulator.h"
#include "random.h"

namespace BS

# This structure is used while converting the connection list to a
# neural net. This helps us to find neurons that don't feed anything
# so that they can be removed along with all the connections that
# feed the useless neurons. We'll cull neurons with .numOutputs == 0
# or those that only feed themselves, i.e., .numSelfInputs == .numOutputs.
# Finally, we'll renumber the remaining neurons sequentially starting
# at zero using the .remappedNumber member.
struct Node
    uint16_t remappedNumber
    uint16_t numOutputs
    uint16_t numSelfInputs
    uint16_t numInputsFromSensorsOrOtherNeurons



# Two neuron renumberings occur: The original genome uses a uint16_t for
# neuron numbers. The first renumbering maps 16-bit unsigned neuron numbers
# to the range 0..p.maxNumberNeurons - 1. After culling useless neurons
# (see comments above), we'll renumber the remaining neurons sequentially
# starting at 0.
typedef std.map<uint16_t, NodeMap; # key is neuron number 0..p.maxNumberNeurons - 1

typedef std.list<Gene> ConnectionList


# Returns by value a single gene with random members.
# See genome.h for the width of the members.
# ToDo: don't assume the width of the members in gene.
def makeRandomGene(self):
    Gene gene

    gene.sourceType = randomUint() & 1
    gene.sourceNum = (uint16_t)randomUint(0, 0x7fff)
    gene.sinkType = randomUint() & 1
    gene.sinkNum = (uint16_t)randomUint(0, 0x7fff)
    gene.weight = Gene.makeRandomWeight()

    return gene



# Returns by value a single genome with random genes.
def makeRandomGenome(self):
    Genome genome

    length = randomUint(p.genomeInitialLengthMin, p.genomeInitialLengthMax)
    for (n = 0; n < length; ++n)
        genome.push_back(makeRandomGene())


    return genome



# Convert the indiv's genome to a renumbered connection list.
# This renumbers the neurons from their uint16_t values in the genome
# to the range 0..p.maxNumberNeurons - 1 by using a modulo operator.
# Sensors are renumbered 0..Sensor.NUM_SENSES - 1
# Actions are renumbered 0..Action.NUM_ACTIONS - 1
def makeRenumberedConnectionList(self, &connectionList, &genome):
    connectionList.clear()
    for (auto  &gene : genome)
        connectionList.push_back(gene)
        auto &conn = connectionList.back()

        if conn.sourceType == NEURON:
            conn.sourceNum %= p.maxNumberNeurons

        else:
            conn.sourceNum %= Sensor.NUM_SENSES


        if conn.sinkType == NEURON:
            conn.sinkNum %= p.maxNumberNeurons

        else:
            conn.sinkNum %= Action.NUM_ACTIONS





# Scan the connections and make a list of all the neuron numbers
# mentioned in the connections. Also keep track of how many inputs and
# outputs each neuron has.
def makeNodeList(self, &nodeMap, &connectionList):
    nodeMap.clear()

    for ( Gene &conn : connectionList)
        if conn.sinkType == NEURON:
            it = nodeMap.find(conn.sinkNum)
            if it == nodeMap.end():
                assert(conn.sinkNum < p.maxNumberNeurons)
                nodeMap.insert(std.pair<uint16_t, Node>(conn.sinkNum, {} ))
                it = nodeMap.find(conn.sinkNum)
                assert(it.first < p.maxNumberNeurons)
                it.second.numOutputs = 0
                it.second.numSelfInputs = 0
                it.second.numInputsFromSensorsOrOtherNeurons = 0


            if conn.sourceType == NEURON and (conn.sourceNum == conn.sinkNum):
                ++(it.second.numSelfInputs)

            else:
                ++(it.second.numInputsFromSensorsOrOtherNeurons)

            assert(nodeMap.count(conn.sinkNum) == 1)

        if conn.sourceType == NEURON:
            it = nodeMap.find(conn.sourceNum)
            if it == nodeMap.end():
                assert(conn.sourceNum < p.maxNumberNeurons)
                nodeMap.insert(std.pair<uint16_t, Node>(conn.sourceNum, {} ))
                it = nodeMap.find(conn.sourceNum)
                assert(it.first < p.maxNumberNeurons)
                it.second.numOutputs = 0
                it.second.numSelfInputs = 0
                it.second.numInputsFromSensorsOrOtherNeurons = 0

            ++(it.second.numOutputs)
            assert(nodeMap.count(conn.sourceNum) == 1)





# During the culling process, will remove any neuron that has no outputs,
# and all the connections that feed the useless neuron.
def removeConnectionsToNeuron(self, &connections, &nodeMap, neuronNumber):
    for (itConn = connections.begin(); itConn != connections.end(); )
        if itConn.sinkType == NEURON and itConn.sinkNum == neuronNumber:
            # Remove the connection. If the connection source is from another
            # neuron, decrement the other neuron's numOutputs:
            if itConn.sourceType == NEURON:
                --(nodeMap[itConn.sourceNum].numOutputs)

            itConn = connections.erase(itConn)

        else:
            ++itConn





# If a neuron has no outputs or only outputs that feed itself, we
# remove it along with all connections that feed it. Reiterative, because
# after we remove a connection to a useless neuron, may result in a
# different neuron having no outputs.
def cullUselessNeurons(self, &connections, &nodeMap):
    allDone = False
    while (not allDone)
        allDone = True
        for (itNeuron = nodeMap.begin(); itNeuron != nodeMap.end(); )
            assert(itNeuron.first < p.maxNumberNeurons)
            # We're looking for neurons with zero outputs, neurons that feed itself
            # and nobody else:
            if (itNeuron.second.numOutputs == itNeuron.second.numSelfInputs)    # could be 0
                allDone = False
                # Find and remove connections from sensors or other neurons
                removeConnectionsToNeuron(connections, nodeMap, itNeuron.first)
                itNeuron = nodeMap.erase(itNeuron)

            else:
                ++itNeuron






# This function is used when an agent is spawned. This function converts the
# agent's inherited genome into the agent's neural net brain. There is a close
# correspondence between the genome and the neural net, a connection
# specified in the genome will not be represented in the neural net if the
# connection feeds a neuron that does not itself feed anything else.
# Neurons get renumbered in the process:
# 1. Create a set of referenced neuron numbers where each index is in the
#    range 0..p.genomeMaxLength-1, a count of outputs for each neuron.
# 2. Delete any referenced neuron index that has no outputs or only feeds itself.
# 3. Renumber the remaining neurons sequentially starting at 0.
def createWiringFromGenome(self):
    NodeMap nodeMap;  # list of neurons and their number of inputs and outputs
    ConnectionList connectionList; # synaptic connections

    # Convert the indiv's genome to a renumbered connection list
    makeRenumberedConnectionList(connectionList, genome)

    # Make a node (neuron) list from the renumbered connection list
    makeNodeList(nodeMap, connectionList)

    # Find and remove neurons that don't feed anything or only feed themself.
    # This reiteratively removes all connections to the useless neurons.
    cullUselessNeurons(connectionList, nodeMap)

    # The neurons map now has all the referenced neurons, neuron numbers, and
    # the number of outputs for each neuron. Now we'll renumber the neurons
    # starting at zero.

    assert(nodeMap.size() <= p.maxNumberNeurons)
    newNumber = 0
    for (auto & node : nodeMap)
        assert(node.second.numOutputs != 0)
        node.second.remappedNumber = newNumber++


    # Create the indiv's connection list in two passes:
    # First the connections to neurons, the connections to actions.
    # This ordering optimizes the feed-forward function in feedForward.cpp.

    nnet.connections.clear()

    # First, connections from sensor or neuron to a neuron
    for (auto  &conn : connectionList)
        if conn.sinkType == NEURON:
            nnet.connections.push_back(conn)
            auto &newConn = nnet.connections.back()
            # fix the destination neuron number
            newConn.sinkNum = nodeMap[newConn.sinkNum].remappedNumber
            # if the source is a neuron, its number too
            if newConn.sourceType == NEURON:
                newConn.sourceNum = nodeMap[newConn.sourceNum].remappedNumber




    # Last, connections from sensor or neuron to an action
    for (auto  &conn : connectionList)
        if conn.sinkType == ACTION:
            nnet.connections.push_back(conn)
            auto &newConn = nnet.connections.back()
            # if the source is a neuron, its number
            if newConn.sourceType == NEURON:
                newConn.sourceNum = nodeMap[newConn.sourceNum].remappedNumber




    # Create the indiv's neural node list
    nnet.neurons.clear()
    for (neuronNum = 0; neuronNum < nodeMap.size(); ++neuronNum)
        nnet.neurons.push_back( {} )
        nnet.neurons.back().output = initialNeuronOutput()
        nnet.neurons.back().driven = (nodeMap[neuronNum].numInputsFromSensorsOrOtherNeurons != 0)




# ---------------------------------------------------------------------------


# This applies a point mutation at a random bit in a genome.
def randomBitFlip(self, &genome):
    method = 1

    byteIndex = randomUint(0, genome.size() - 1) * sizeof(Gene)
    elementIndex = randomUint(0, genome.size() - 1)
    bitIndex8 = 1 << randomUint(0, 7)

    if method == 0:
        ((uint8_t *)&genome[0])[byteIndex] ^= bitIndex8

    elif method == 1:
        chance = randomUint() / (float)RANDOM_UINT_MAX; # 0..1
        if (chance < 0.2)   # sourceType
            genome[elementIndex].sourceType ^= 1

        elif (chance < 0.4)     # sinkType
            genome[elementIndex].sinkType ^= 1

        elif (chance < 0.6)     # sourceNum
            genome[elementIndex].sourceNum ^= bitIndex8

        elif (chance < 0.8)     # sinkNum
            genome[elementIndex].sinkNum ^= bitIndex8

        else     # weight
            genome[elementIndex].weight ^= (1 << randomUint(1, 15))


    else:
        assert(False)




# If the genome is longer than the prescribed length, if it's longer
# than one gene, we remove genes from the front or back. This is
# used only when the simulator is configured to allow genomes of
# unequal lengths during a simulation.
def cropLength(self, &genome, length):
    if genome.size() > length and length > 0:
        if randomUint() / (float)RANDOM_UINT_MAX < 0.5:
            # trim front
            numberElementsToTrim = genome.size() - length
            genome.erase(genome.begin(), genome.begin() + numberElementsToTrim)

        else:
            # trim back
            genome.erase(genome.end() - (genome.size() - length), genome.end())





# Inserts or removes a single gene from the genome. This is
# used only when the simulator is configured to allow genomes of
# unequal lengths during a simulation.
def randomInsertDeletion(self, &genome):
    probability = p.geneInsertionDeletionRate
    if randomUint() / (float)RANDOM_UINT_MAX < probability:
        if randomUint() / (float)RANDOM_UINT_MAX < p.deletionRatio:
            # deletion
            if genome.size() > 1:
                genome.erase(genome.begin() + randomUint(0, genome.size() - 1))


        elif genome.size() < p.genomeMaxLength:
            # insertion
            #genome.insert(genome.begin() + randomUint(0, genome.size() - 1), makeRandomGene())
            genome.push_back(makeRandomGene())





# This function causes point mutations in a genome with a probability defined
# by the parameter p.pointMutationRate.
def applyPointMutations(self, &genome):
    numberOfGenes = genome.size()
    while (numberOfGenes-- > 0)
        if (randomUint() / (float)RANDOM_UINT_MAX) < p.pointMutationRate:
            randomBitFlip(genome)





# This generates a child genome from one or two parent genomes.
# If the parameter p.sexualReproduction is True, parents contribute
# genes to the offspring. The genome may undergo mutation.
# Must be called in single-thread mode between generations
def generateChildGenome(self, &parentGenomes):
    # random parent (or parents if sexual reproduction) with random
    # mutations
    Genome genome

    uint16_t parent1Idx
    uint16_t parent2Idx

    # Choose two parents randomly from the candidates. If the parameter
    # p.chooseParentsByFitness is False, we choose at random from
    # all the candidate parents with equal preference. If the parameter is
    # True, we give preference to candidate parents according to their
    # score. Their score was computed by the survival/selection algorithm
    # in survival-criteria.cpp.
    if p.chooseParentsByFitness and parentGenomes.size() > 1:
        parent1Idx = randomUint(1, parentGenomes.size() - 1)
        parent2Idx = randomUint(0, parent1Idx - 1)

    else:
        parent1Idx = randomUint(0, parentGenomes.size() - 1)
        parent2Idx = randomUint(0, parentGenomes.size() - 1)


     Genome &g1 = parentGenomes[parent1Idx]
     Genome &g2 = parentGenomes[parent2Idx]

    if g1.size() == 0 or g2.size() == 0:
        std.cout << "invalid genome" << std.endl
        assert(False)


    overlayWithSliceOf = [&]( Genome &gShorter)
        index0 = randomUint(0, gShorter.size() - 1)
        index1 = randomUint(0, gShorter.size())
        if index0 > index1:
            std.swap(index0, index1)

        std.copy(&gShorter[index0], &gShorter[index1], &genome[index0])


    if p.sexualReproduction:
        if g1.size() > g2.size():
            genome = g1
            overlayWithSliceOf(g2)
            assert(genome.size() > 0)

        else:
            genome = g2
            overlayWithSliceOf(g1)
            assert(genome.size() > 0)


        # Trim length = average length of parents
        sum = g1.size() + g2.size()
        # If average length is not an integral number, one half the time
        if (sum & 1) and (randomUint() & 1):
            ++sum

        cropLength(genome, sum / 2)
        assert(genome.size() > 0)

    else:
        genome = g2
        assert(genome.size() > 0)


    randomInsertDeletion(genome)
    assert(genome.size() > 0)
    applyPointMutations(genome)
    assert(genome.size() > 0)
    assert(genome.size() <= p.genomeMaxLength)

    return genome


} # end namespace BS

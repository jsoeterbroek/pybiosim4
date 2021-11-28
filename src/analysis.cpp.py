# analysis.cpp -- various reports

#include <iostream>
#include <iomanip>
#include <fstream>
#include <cassert>
#include <cstring>
#include <string>
#include "simulator.h"

namespace BS

# This converts sensor numbers to descriptive strings.
def sensorName(self, sensor):
    switch(sensor)
    case AGE:
        return "age"
        break
    case BOUNDARY_DIST:
        return "boundary dist"
        break
    case BOUNDARY_DIST_X:
        return "boundary dist X"
        break
    case BOUNDARY_DIST_Y:
        return "boundary dist Y"
        break
    case LAST_MOVE_DIR_X:
        return "last move dir X"
        break
    case LAST_MOVE_DIR_Y:
        return "last move dir Y"
        break
    case LOC_X:
        return "loc X"
        break
    case LOC_Y:
        return "loc Y"
        break
    case LONGPROBE_POP_FWD:
        return "long probe population fwd"
        break
    case LONGPROBE_BAR_FWD:
        return "long probe barrier fwd"
        break
    case BARRIER_FWD:
        return "short probe barrier fwd-rev"
        break
    case BARRIER_LR:
        return "short probe barrier left-right"
        break
    case OSC1:
        return "osc1"
        break
    case POPULATION:
        return "population"
        break
    case POPULATION_FWD:
        return "population fwd"
        break
    case POPULATION_LR:
        return "population LR"
        break
    case RANDOM:
        return "random"
        break
    case SIGNAL0:
        return "signal 0"
        break
    case SIGNAL0_FWD:
        return "signal 0 fwd"
        break
    case SIGNAL0_LR:
        return "signal 0 LR"
        break
    case GENETIC_SIM_FWD:
        return "genetic similarity fwd"
        break
    default:
        assert(False)
        break




# Converts action numbers to descriptive strings.
def actionName(self, action):
    switch(action)
    case MOVE_EAST:
        return "move east"
        break
    case MOVE_WEST:
        return "move west"
        break
    case MOVE_NORTH:
        return "move north"
        break
    case MOVE_SOUTH:
        return "move south"
        break
    case MOVE_FORWARD:
        return "move fwd"
        break
    case MOVE_X:
        return "move X"
        break
    case MOVE_Y:
        return "move Y"
        break
    case SET_RESPONSIVENESS:
        return "set inv-responsiveness"
        break
    case SET_OSCILLATOR_PERIOD:
        return "set osc1"
        break
    case EMIT_SIGNAL0:
        return "signal.emit 0"
        break
    case KILL_FORWARD:
        return "kill fwd"
        break
    case MOVE_REVERSE:
        return "move reverse"
        break
    case MOVE_LEFT:
        return "move left"
        break
    case MOVE_RIGHT:
        return "move right"
        break
    case MOVE_RL:
        return "move R-L"
        break
    case MOVE_RANDOM:
        return "move random"
        break
    case SET_LONGPROBE_DIST:
        return "set longprobe dist"
        break
    default:
        assert(False)
        break




# This converts sensor numbers to mnemonic strings.
# Useful for later processing by graph-nnet.py.
def sensorShortName(self, sensor):
    switch(sensor)
    case AGE:
        return "Age"
        break
    case BOUNDARY_DIST:
        return "ED"
        break
    case BOUNDARY_DIST_X:
        return "EDx"
        break
    case BOUNDARY_DIST_Y:
        return "EDy"
        break
    case LAST_MOVE_DIR_X:
        return "LMx"
        break
    case LAST_MOVE_DIR_Y:
        return "LMy"
        break
    case LOC_X:
        return "Lx"
        break
    case LOC_Y:
        return "Ly"
        break
    case LONGPROBE_POP_FWD:
        return "LPf"
        break
    case LONGPROBE_BAR_FWD:
        return "LPb"
        break
    case BARRIER_FWD:
        return "Bfd"
        break
    case BARRIER_LR:
        return "Blr"
        break
    case OSC1:
        return "Osc"
        break
    case POPULATION:
        return "Pop"
        break
    case POPULATION_FWD:
        return "Pfd"
        break
    case POPULATION_LR:
        return "Plr"
        break
    case RANDOM:
        return "Rnd"
        break
    case SIGNAL0:
        return "Sg"
        break
    case SIGNAL0_FWD:
        return "Sfd"
        break
    case SIGNAL0_LR:
        return "Slr"
        break
    case GENETIC_SIM_FWD:
        return "Gen"
        break
    default:
        assert(False)
        break




# Converts action numbers to mnemonic strings.
# Useful for later processing by graph-nnet.py.
def actionShortName(self, action):
    switch(action)
    case MOVE_EAST:
        return "MvE"
        break
    case MOVE_WEST:
        return "MvW"
        break
    case MOVE_NORTH:
        return "MvN"
        break
    case MOVE_SOUTH:
        return "MvS"
        break
    case MOVE_X:
        return "MvX"
        break
    case MOVE_Y:
        return "MvY"
        break
    case MOVE_FORWARD:
        return "Mfd"
        break
    case SET_RESPONSIVENESS:
        return "Res"
        break
    case SET_OSCILLATOR_PERIOD:
        return "OSC"
        break
    case EMIT_SIGNAL0:
        return "SG"
        break
    case KILL_FORWARD:
        return "Klf"
        break
    case MOVE_REVERSE:
        return "Mrv"
        break
    case MOVE_LEFT:
        return "MvL"
        break
    case MOVE_RIGHT:
        return "MvR"
        break
    case MOVE_RL:
        return "MRL"
        break
    case MOVE_RANDOM:
        return "Mrn"
        break
    case SET_LONGPROBE_DIST:
        return "LPD"
        break
    default:
        assert(False)
        break




# List the names of the active sensors and actions to stdout.
# "Active" means those sensors and actions that are compiled into
# the code. See sensors-actions.h for how to define the enums.
def printSensorsActions(self):
    unsigned i
    std.cout << "Sensors:" << std.endl
    for (i = 0; i < Sensor.NUM_SENSES; ++i)
        std.cout << "  " << sensorName((Sensor)i) << std.endl

    std.cout << "Actions:" << std.endl
    for (i = 0; i < Action.NUM_ACTIONS; ++i)
        std.cout << "  " << actionName((Action)i) << std.endl

    std.cout << std.endl



# Format: 32-bit hex strings, per gene
def printGenome(self):
    constexpr genesPerLine = 8
    count = 0
    for (Gene gene : genome)
        if count == genesPerLine:
            std.cout << std.endl
            count = 0

        elif count != 0:
            std.cout << " "


        assert(sizeof(Gene) == 4)
        uint32_t n
        std.memcpy(&n, &gene, sizeof(n))
        std.cout << std.hex << std.setfill('0') << std.setw(8) << n
        ++count

    std.cout << std.dec << std.endl



#'''
#Example format:
#
#    ACTION_NAMEa from:
#    ACTION_NAMEb from:
#        SENSOR i
#        SENSOR j
#        NEURON n
#        NEURON m
#    Neuron x from:
#        SENSOR i
#        SENSOR j
#        NEURON n
#        NEURON m
#    Neuron y ...
#'''
#void Indiv.printNeuralNet()
##    for (action = 0; action < Action.NUM_ACTIONS; ++action)#        actionDisplayed = False
#        for (auto & conn : nnet.connections)#
#            assert((conn.sourceType == NEURON and conn.sourceNum < p.maxNumberNeurons)
#                or (conn.sourceType == SENSOR and conn.sourceNum < Sensor.NUM_SENSES))
#            assert((conn.sinkType == ACTION and conn.sinkNum < Action.NUM_ACTIONS)
#                or (conn.sinkType == NEURON and conn.sinkNum < p.maxNumberNeurons))
#
#            if conn.sinkType == ACTION and (conn.sinkNum) == action:#                if not actionDisplayed:#                    std.cout << "Action " << actionName((Action)action) << " from:" << std.endl
#                    actionDisplayed = True
#
#                if conn.sourceType == SENSOR:#                    std.cout << "   " << sensorName((Sensor)(conn.sourceNum))
#                } else:
#                    std.cout << "   Neuron " << (conn.sourceNum % nnet.neurons.size())
#
#                std.cout << " " << conn.weightAsFloat() << std.endl
#
#
#
#
#    for (neuronNum = 0; neuronNum < nnet.neurons.size(); ++neuronNum)#        neuronDisplayed = False
#        for (auto & conn : nnet.connections)#            if conn.sinkType == NEURON and (conn.sinkNum) == neuronNum:#                if not neuronDisplayed:#                    std.cout << "Neuron " << neuronNum << " from:" << std.endl
#                    neuronDisplayed = True
#
#                if conn.sourceType == SENSOR:#                    std.cout << "   " << sensorName((Sensor)(conn.sourceNum))
#                } else:
#                    std.cout << "   Neuron " << (conn.sourceNum)
#
#                std.cout << " " << conn.weightAsFloat() << std.endl
#
#
#
#
#


# This prints a neural net in a form that can be processed with
# graph-nnet.py to produce a graphic illustration of the net.
def printIGraphEdgeList(self):
    for (auto & conn : nnet.connections)
        if conn.sourceType == SENSOR:
            std.cout << sensorShortName((Sensor)(conn.sourceNum))

        else:
            std.cout << "N" << std.to_string(conn.sourceNum)


        std.cout << " "

        if conn.sinkType == ACTION:
            std.cout << actionShortName((Action)(conn.sinkNum))

        else:
            std.cout << "N" << std.to_string(conn.sinkNum)


        std.cout << " " << std.to_string(conn.weight) << std.endl




def averageGenomeLength(self):
    count = 100
    numberSamples = 0
    unsigned sum = 0

    while (count-- > 0)
        sum += peeps[randomUint(1, p.population)].genome.size()
        ++numberSamples

    return sum / numberSamples



# The epoch log contains one line per generation in a format that can be
# fed to graphlog.gp to produce a chart of the simulation progress.
# ToDo: remove hardcoded filename.
def appendEpochLog(self, generation, numberSurvivors, murderCount):
    std.ofstream foutput

    if generation == 0:
        foutput.open(p.logDir + "/epoch-log.txt")
        foutput.close()


    foutput.open(p.logDir + "/epoch-log.txt", std.ios.app)

    if foutput.is_open():
        foutput << generation << " " << numberSurvivors << " " << geneticDiversity()
                << " " << averageGenomeLength() << " " << murderCount << std.endl

    else:
        assert(False)




# Print stats about pheromone usage.
def displaySignalUse(self):
    if Sensor.SIGNAL0 > Sensor.NUM_SENSES and Sensor.SIGNAL0_FWD > Sensor.NUM_SENSES and Sensor.SIGNAL0_LR > Sensor.NUM_SENSES:
        return


    unsigned long sum = 0
    count = 0

    for (x = 0; x < p.sizeX; ++x)
        for (y = 0; y < p.sizeY; ++y)
            magnitude = signals.getMagnitude(0, { x, y })
            if magnitude != 0:
                ++count
                sum += magnitude



    std.cout << "Signal spread " << ((double)count / (p.sizeX * p.sizeY)) << "%, average " << ((double)sum / (p.sizeX * p.sizeY)) << std.endl



# Print how many connections occur from each kind of sensor neuron and to
# each kind of action neuron over the entire population. This helps us to
# see which sensors and actions are most useful for survival.
def displaySensorActionReferenceCounts(self):
    std.vector<unsigned> sensorCounts(Sensor.NUM_SENSES, 0)
    std.vector<unsigned> actionCounts(Action.NUM_ACTIONS, 0)

    for (index = 1; index <= p.population; ++index)
        if peeps[index].alive:
             Indiv &indiv = peeps[index]
            for ( Gene &gene : indiv.nnet.connections)
                if gene.sourceType == SENSOR:
                    assert(gene.sourceNum < Sensor.NUM_SENSES)
                    ++sensorCounts[(Sensor)gene.sourceNum]

                if gene.sinkType == ACTION:
                    assert(gene.sinkNum < Action.NUM_ACTIONS)
                    ++actionCounts[(Action)gene.sinkNum]





    std.cout << "Sensors in use:" << std.endl
    for (i = 0; i < sensorCounts.size(); ++i)
        if sensorCounts[i] > 0:
            std.cout << "  " << sensorCounts[i] << " - " << sensorName((Sensor)i) << std.endl


    std.cout << "Actions in use:" << std.endl
    for (i = 0; i < actionCounts.size(); ++i)
        if actionCounts[i] > 0:
            std.cout << "  " << actionCounts[i] << " - " << actionName((Action)i) << std.endl





def displaySampleGenomes(self, count):
    index = 1; # indexes start at 1
    for (index = 1; count > 0 and index <= p.population; ++index)
        if peeps[index].alive:
            std.cout << "---------------------------\nIndividual ID " << index << std.endl
            peeps[index].printGenome()
            std.cout << std.endl

            #peeps[index].printNeuralNet()
            peeps[index].printIGraphEdgeList()


            std.cout << "---------------------------" << std.endl
            --count



    displaySensorActionReferenceCounts()


} # end namespace BS

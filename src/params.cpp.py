# params.cpp
# See params.h for notes.

#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <string>
#include <cctype>
#include <cstdint>
#include <map>
#include "params.h"

# To add a parameter:
#    1. Add a member to struct Params in params.h.
#    2. Add a member and its default value to privParams in ParamManager.setDefault()
#          in params.cpp.
#    3. Add an else clause to ParamManager.ingestParameter() in params.cpp.
#    4. Add a line to the user's parameter file (default name biosim4.ini)

namespace BS

def setDefaults(self):
    privParams.sizeX = 128
    privParams.sizeY = 128
    privParams.challenge = 0

    privParams.genomeInitialLengthMin = 16
    privParams.genomeInitialLengthMax = 16
    privParams.genomeMaxLength = 20
    privParams.logDir = "./logs/"
    privParams.imageDir = "./images/"
    privParams.population = 100
    privParams.stepsPerGeneration = 100
    privParams.maxGenerations = 100
    privParams.barrierType = 0
    privParams.replaceBarrierType = 0
    privParams.replaceBarrierTypeGenerationNumber = (uint32_t)-1
    privParams.numThreads = 1
    privParams.signalLayers = 1
    privParams.maxNumberNeurons = privParams.genomeMaxLength / 2
    privParams.pointMutationRate = 0.0001
    privParams.geneInsertionDeletionRate = 0.0001
    privParams.deletionRatio = 0.7
    privParams.killEnable = False
    privParams.sexualReproduction = True
    privParams.chooseParentsByFitness = True
    privParams.populationSensorRadius = 2.0
    privParams.signalSensorRadius = 1
    privParams.responsiveness = 0.5
    privParams.responsivenessCurveKFactor = 2
    privParams.longProbeDistance = 16
    privParams.shortProbeBarrierDistance = 3
    privParams.valenceSaturationMag = 0.5
    privParams.saveVideo = True
    privParams.videoStride = 1
    privParams.videoSaveFirstFrames = 0
    privParams.displayScale = 1
    privParams.agentSize = 2
    privParams.genomeAnalysisStride = 1
    privParams.displaySampleGenomes = 0
    privParams.genomeComparisonMethod = 1
    privParams.updateGraphLog = False
    privParams.updateGraphLogStride = 16
    privParams.graphLogUpdateCommand = "/usr/bin/gnuplot --persist ./tools/graphlog.gp"



def registerConfigFile(self, *filename):
    configFilename = std.string(filename)



def checkIfUint(self, &s):
    return s.find_first_not_of("0123456789") == std.string.npos



def checkIfInt(self, &s):
    #return s.find_first_not_of("-0123456789") == std.string.npos
    std.istringstream iss(s)
    int i
    iss >> std.noskipws >> i; # noskipws considers leading whitespace invalid
    # Check the entire string was consumed and if either failbit or badbit is set
    return iss.eof() and not iss.fail()



def checkIfFloat(self, &s):
    std.istringstream iss(s)
    double d
    iss >> std.noskipws >> d; # noskipws considers leading whitespace invalid
    # Check the entire string was consumed and if either failbit or badbit is set
    return iss.eof() and not iss.fail()



def checkIfBool(self, &s):
    return s == "0" or s == "1" or s == "True" or s == "False"



def getBoolVal(self, &s):
    if s == "True" or s == "1":
        return True
    elif s == "False" or s == "0":
        return False
    else:
        return False



def ingestParameter(self, name, val):
    std.transform(name.begin(), name.end(), name.begin(),
                   [](unsigned char c)
        return std.tolower(c)
    })
    #std.cout << name << " " << val << '\n' << std.endl

    isUint = checkIfUint(val)
    uVal = isUint ? (unsigned)std.stol(val.c_str()) : 0
    isInt = checkIfInt(val)
    iVal = isInt ? std.stoi(val.c_str()) : 0
    isFloat = checkIfFloat(val)
    dVal = isFloat ? std.stod(val.c_str()) : 0.0
    isBool = checkIfBool(val)
    bVal = getBoolVal(val)

    do
        if name == "sizex" and isUint and uVal >= 2 and uVal <= (uint16_t)-1:
            privParams.sizeX = uVal
            break

        elif name == "sizey" and isUint and uVal >= 2 and uVal <= (uint16_t)-1:
            privParams.sizeY = uVal
            break

        elif name == "challenge" and isUint and uVal < (uint16_t)-1:
            privParams.challenge = uVal
            break

        elif name == "genomeinitiallengthmin" and isUint and uVal > 0 and uVal < (uint16_t)-1:
            privParams.genomeInitialLengthMin = uVal
            break

        elif name == "genomeinitiallengthmax" and isUint and uVal > 0 and uVal < (uint16_t)-1:
            privParams.genomeInitialLengthMax = uVal
            break

        elif name == "logdir":
            privParams.logDir = val
            break

        elif name == "imagedir":
            privParams.imageDir = val
            break

        elif name == "population" and isUint and uVal > 0 and uVal < (uint32_t)-1:
            privParams.population = uVal
            break

        elif name == "stepspergeneration" and isUint and uVal > 0 and uVal < (uint16_t)-1:
            privParams.stepsPerGeneration = uVal
            break

        elif name == "maxgenerations" and isUint and uVal > 0 and uVal < 0x7fffffff:
            privParams.maxGenerations = uVal
            break

        elif name == "barriertype" and isUint and uVal < (uint32_t)-1:
            privParams.barrierType = uVal
            break

        elif name == "replacebarriertype" and isUint and uVal < (uint32_t)-1:
            privParams.replaceBarrierType = uVal
            break

        elif name == "replacebarriertypegenerationnumber" and isInt and iVal >= -1:
            privParams.replaceBarrierTypeGenerationNumber = (iVal == -1 ? (uint32_t)-1 : iVal)
            break

        elif name == "numthreads" and isUint and uVal > 0 and uVal < (uint16_t)-1:
            privParams.numThreads = uVal
            break

        elif name == "signallayers" and isUint and uVal < (uint16_t)-1:
            privParams.signalLayers = uVal
            break

        elif name == "genomemaxlength" and isUint and uVal > 0 and uVal < (uint16_t)-1:
            privParams.genomeMaxLength = uVal
            break

        elif name == "maxnumberneurons" and isUint and uVal > 0 and uVal < (uint16_t)-1:
            privParams.maxNumberNeurons = uVal
            break

        elif name == "pointmutationrate" and isFloat and dVal >= 0.0 and dVal <= 1.0:
            privParams.pointMutationRate = dVal
            break

        elif name == "geneinsertiondeletionrate" and isFloat and dVal >= 0.0 and dVal <= 1.0:
            privParams.geneInsertionDeletionRate = dVal
            break

        elif name == "deletionratio" and isFloat and dVal >= 0.0 and dVal <= 1.0:
            privParams.deletionRatio = dVal
            break

        elif name == "killenable" and isBool:
            privParams.killEnable = bVal
            break

        elif name == "sexualreproduction" and isBool:
            privParams.sexualReproduction = bVal
            break

        elif name == "chooseparentsbyfitness" and isBool:
            privParams.chooseParentsByFitness = bVal
            break

        elif name == "populationsensorradius" and isFloat and dVal > 0.0:
            privParams.populationSensorRadius = dVal
            break

        elif name == "signalsensorradius" and isFloat and dVal > 0.0:
            privParams.signalSensorRadius = dVal
            break

        elif name == "responsiveness" and isFloat and dVal >= 0.0:
            privParams.responsiveness = dVal
            break

        elif name == "responsivenesscurvekfactor" and isUint and uVal >= 1 and uVal <= 20:
            privParams.responsivenessCurveKFactor = uVal
            break

        elif name == "longprobedistance" and isUint and uVal > 0:
            privParams.longProbeDistance = uVal
            break

        elif name == "shortprobebarrierdistance" and isUint and uVal > 0:
            privParams.shortProbeBarrierDistance = uVal
            break

        elif name == "valencesaturationmag" and isFloat and dVal >= 0.0:
            privParams.valenceSaturationMag = dVal
            break

        elif name == "savevideo" and isBool:
            privParams.saveVideo = bVal
            break

        elif name == "videostride" and isUint and uVal > 0:
            privParams.videoStride = uVal
            break

        elif name == "videosavefirstframes" and isUint:
            privParams.videoSaveFirstFrames = uVal
            break

        elif name == "displayscale" and isUint and uVal > 0:
            privParams.displayScale = uVal
            break

        elif name == "agentsize" and isFloat and dVal > 0.0:
            privParams.agentSize = dVal
            break

        elif name == "genomeanalysisstride" and isUint and uVal > 0:
            privParams.genomeAnalysisStride = uVal
            break

        elif name == "genomeanalysisstride" and val == "videoStride":
            privParams.genomeAnalysisStride = privParams.videoStride
            break

        elif name == "displaysamplegenomes" and isUint:
            privParams.displaySampleGenomes = uVal
            break

        elif name == "genomecomparisonmethod" and isUint:
            privParams.genomeComparisonMethod = uVal
            break

        elif name == "updategraphlog" and isBool:
            privParams.updateGraphLog = bVal
            break

        elif name == "updategraphlogstride" and isUint and uVal > 0:
            privParams.updateGraphLogStride = uVal
            break

        elif name == "updategraphlogstride" and val == "videoStride":
            privParams.updateGraphLogStride = privParams.videoStride
            break

        else:
            std.cout << "Invalid param: " << name << " = " << val << std.endl


    while (0)



def updateFromConfigFile(self):
    # std.ifstream is RAII, i.e. no need to call close
    std.ifstream cFile(configFilename.c_str())
    if cFile.is_open():
        std.string line
        while(getline(cFile, line))
            line.erase(std.remove_if(line.begin(), line.end(), isspace),
                       line.end())
            if line[0] == '#' or line.empty():
                continue

            delimiterPos = line.find("=")
            name = line.substr(0, delimiterPos)
            std.transform(name.begin(), name.end(), name.begin(),
                           [](unsigned char c)
                return std.tolower(c)
            })
            value0 = line.substr(delimiterPos + 1)
            delimiterComment = value0.find("#")
            value = value0.substr(0, delimiterComment)
            rawValue = value
            value.erase(std.remove_if(value.begin(), value.end(), isspace),
                        value.end())
            #std.cout << name << " " << value << '\n' << std.endl
            ingestParameter(name, value)


    else:
        std.cerr << "Couldn't open config file " << configFilename << ".\n" << std.endl



} # end namespace BS

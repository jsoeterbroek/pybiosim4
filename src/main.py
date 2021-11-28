# This is the only call needed to start the simulator. No header file
# because it's just one declaration. Pass it argc and argv as if from main().
# If there is no command line argument, simulator will read the default
# config file ("biosim4.ini" in the current directory) to get the simulation
# parameters for self run. If there are one or more command line args, then
# argv[1] must contain the name of the config file which will be read instead
# of biosim4.ini. Any args after that are ignored. The simulator code is
# in namespace BS (for "biosim").
#namespace BS
#def simulator(self, argc, **argv):

import simulator

def main(self, argc, **argv):
    #BS.unitTestBasicTypes(); # called only for unit testing of basic types

    # Start the simulator with optional config filename (default "biosim4.ini").
    # See simulator.cpp and simulator.h.
    simulator(argc, argv)

    return 0


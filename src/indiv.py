class Indiv:

    # This is called when any individual is spawned.
    # The responsiveness parameter will be initialized here to maximum value
    # of 1.0, depending on which action activation function is used,
    # the default undriven value may be changed to 1.0 or action midrange.

    def initialize(self, index_, loc_, andgenome_):
        index = index_
        loc = loc_
        #birthLoc = loc_
        grid.set(loc_, index_)
        age = 0
        oscPeriod = 34; # ToDo not !not  define a constant
        alive = True
        lastMoveDir = Dir.random8()
        responsiveness = 0.5; # range 0.0..1.0
        #longProbeDist = p.longProbeDistance
        #challengeBits = (unsigned)False; # will be set True when some task gets accomplished
        #genome = std.move(genome_)
        #createWiringFromGenome()

# peeps.py
#
# Manages a container of individual agents of type Indiv and their
# locations in the grid container

#from dataclasses import dataclass, field

class SimpleQueue:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class deathQueue(SimpleQueue):
    pass

class moveQueue(SimpleQueue):
    pass

class Peeps():

    def __init__(self, population):

        self.dq = deathQueue()
        self.mq = deathQueue()
        self.population = population

        #Index 0 is reserved, so add one:
        self.individuals = self.population + 1

    def ret_population(self):
        return self.population

    def ret_individuals(self):
        return self.individuals

    # Indiv will remain alive and in-world until end of sim step when
    # drainDeathQueue() is called.
    def queueForDeath(self, indiv):
        self.dq.enqueue(indiv)

    # TODO
    # This executes all the
    # queued deaths, removing the dead agents from the grid.
    #def drainDeathQueue():

    # indiv won't move until end
    # of sim step when drainMoveQueue() is called.
    def queueForMove(self, indiv, newloc):
        indiv_newloc = {}
        indiv_newloc[indiv] = newloc
        self.mq.enqueue(indiv_newloc)

    # TODO
    # This executes all the queued movements. Each movement is 
    # typically one 8-neighbor cell distance but this
    # function can move an individual any arbitrary distance.
    #def drainMoveQueue():

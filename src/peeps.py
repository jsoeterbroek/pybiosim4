


class Peeps():


    def __init__(self, population):
        self.population = population
        #Index 0 is reserved, so add one:
        self.individuals = self.population + 1

    def ret_population(self):
        return self.population

    def ret_individuals(self):
        return self.individuals

from copy import copy
from random import shuffle, random
from Path import Path
from crossovers import crossover1
from mutations import mutation1


class GeneticAlgorithm:
    def __init__(self, cities, options):
        self.cities = cities
        self.options = options
        self.population = []
        self.fitness_hash = {}
        self.current_iter = 0
        self.limit = 0
        self.current_best = float('Inf')
        self.best_path = None
        self.init_population()

    def init_population(self):
        for i in range(self.options['PopulationSize']):
            cities = copy(self.cities)
            shuffle(cities)
            self.population.append(Path(cities))
        self.best_path = self.population[0]

    def calculate_fitness(self):
        self.fitness_hash.clear()

        for path in self.population:
            fitness = path.total_distance
            self.fitness_hash[path] = fitness

    def next_iter(self):
        self.init_population()
        if self.current_iter < self.options['NumOfGenerations'] and self.limit <= self.options['Limit']:
            self.selection()
            self.population.sort(key=lambda x: self.fitness_hash[x])
            self.population = self.population[0:self.options['PopulationSize']]
            self.current_iter += 1
            # ako nema napretka options['Limit'] puta, prekini petlju
            if self.current_best - self.population[0].total_distance < self.options['FunctionTolerance']:
                self.limit += 1
            else:
                self.limit = 0
            self.current_best = self.population[0].total_distance
            return True
        return False

    def selection(self):
        childrens = []

        self.calculate_fitness()
        for i in range(len(self.population) // 2):
            parent1, parent2 = self.select_parents()
            child1, child2 = crossover1(parent1, parent2)

            mutation1(child1, self.options['MutationRate'])
            childrens.append(child1)

            mutation1(child2, self.options['MutationRate'])
            childrens.append(child2)

        self.population += childrens
        # mozda editovati funkciju da kalkulise samo drugi deo a ne ponovo za roditelje
        self.calculate_fitness()

    def select_parents(self):
        roulette_table = []
        for path in self.population:
            fitness_with_random = self.fitness_hash[path] * random()
            roulette_table.append(fitness_with_random)

        min1 = [0, roulette_table[0]] if roulette_table[0] < roulette_table[1] else [1, roulette_table[1]]
        min2 = [0, roulette_table[0]] if roulette_table[0] > roulette_table[1] else [1, roulette_table[1]]

        for i in range(2, len(self.population)):
            fitness = roulette_table[i]

            if fitness < min1[1]:
                min2 = min1
                min1 = [i, fitness]
                continue

            if fitness < min2[1]:
                min2 = [i, fitness]

        return self.population[min1[0]], self.population[min1[0]]

import json
import random
import numpy as np
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

class Evaluator(object):
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity
    def __call__(self, candidate):
        total_weight = 0
        total_profit = 0

        for i in xrange(len(candidate)):
            if candidate[i]:
                total_weight += self.items[i]['weight']
                total_profit += self.items[i]['profit']

        if total_weight > self.capacity:
            overload = total_weight - self.capacity
        else:
            overload = 0

        return (overload, total_profit)

with open('items.json') as f:
    items = json.load(f)

with open('capacity.json') as f:
    capacity = json.load(f)

evaluator = Evaluator(items, capacity)

# Objectives are decreasing overload and increasing total profit, in that order
creator.create('FitnessMulti', base.Fitness, weights=(-1, 1))
creator.create('Individual', list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register('random_bit', lambda: random.choice([False, True]))
toolbox.register('individual',
                 tools.initRepeat,
                 creator.Individual,
                 toolbox.random_bit,
                 n = len(items))
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('evaluate', evaluator)
toolbox.register('mate', tools.cxTwoPoint)
toolbox.register('mutate', tools.mutFlipBit, indpb=0.05)
toolbox.register('select', tools.selNSGA2)

def main():
    # random.seed(42)

    NGEN = 500
    MU = 50
    LAMBDA = 100
    CXPB = 0.5
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()

    pop, log = algorithms.eaMuPlusLambda(pop, toolbox,
                                         MU,
                                         LAMBDA,
                                         CXPB,
                                         MUTPB,
                                         NGEN,
                                         halloffame=hof,
                                         verbose=True)

    total_profit = 0
    total_weight = 0
    best_solution = hof[0]

    print 'Items selected:'

    for i in xrange(len(best_solution)):
        if best_solution[i]:
            print i + 1
            total_profit += items[i]['profit']
            total_weight += items[i]['weight']

    print
    print 'Total weight: %d' % total_weight
    print 'Capacity: %d' % capacity
    print 'Total profit: %d' % total_profit

main()

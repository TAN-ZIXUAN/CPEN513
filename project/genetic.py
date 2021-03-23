# https://towardsdatascience.com/introducing-geneal-a-genetic-algorithm-python-library-db69abfc212c
import numpy as np
def initialize_population(pop_size, n_genes, input_limits):
    """
    Initializes the population of the problem according to the 
    populatoin size and number of genes
    :param pop_size: number of individuals in the population
    :param n_genes: number of genes (variables) in the problem
    :param input_limits: tuple containing the minimum and maximum allowed
    
    :return: a numpy array with randomly initialized population
    """
    population = np.random.uniform(input_limits[0], input_limits[1], size = (pop_size, n_genes))

    return population
    
def fitness_function(individual):
    """
    Implements the logic that calculates the fitness
    measure of an indivdual
    
    :param individual: chromosome of genes representing an individual
    :return: the fitness of the individual
    """

    raise NotImplementedError

def select_parents(self, selection_strategy, n_matings, prob_intervals):
    """
    Selects the parents according to a given selection strategy
    Options are:
    roulette_wheel: Selects individuals from mating pool giving higher probabilities to fit individuals.

    :param selection_strategy: the strategy to use for selecting parents
    :param n_mating: the number of matings to perform
    :param prob_intervals: the selection probability for each individual in the mating pool

    :return: 2 arrays with selected individuals corresponding to each parent
    """
    ma, pa = None, None
    
    if selection_strategy == "roulette_wheel":
        ma = np.apply_along_axis(lambda value: np.argmin(value > prob_intervals) - 1, 1, np.random.rand(n_matings, 1))
        pa = np.apply_along_axis(lambda value: np.argmin(value > prob_intervals) - 1, 1, np.random.rand(n_matings, 1))
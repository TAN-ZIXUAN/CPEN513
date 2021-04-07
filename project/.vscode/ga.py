import random
# https://github.com/kiecodes/genetic-algorithms/blob/master/algorithms/genetic.py
"""
genome is a list of 0 and 1. represent a possible solution.
0 and 1 stands for group 0 and group 1.
idx stands for the pin number.
so a genome stands for the distribution of pins in two groups

population is a list of genomes, aka many kinds of solution
we want evolve a solution that minimize the cutsize
"""


def generate_genome(length):
    """ using random.choices generate genome list(a list of genes(0 or 1))
    Args: 
        length: the length of the genome list. it should be the same as the pin numbers
    
    Returns:
        genome: a generated genome list consists of 0 and 1
    """

    return random.choices([0, 1], k = length)

def generate_population(size, genome_length):
    """Population: List[genome]
    Args: 
        size: size of the population (the length of population list)
        genome_length: the length of a genome list
    Returns:
        population: List[genome]
    """
    return [generate_genome(genome_length) for _ in range(size)]

def single_point_crossover(a, b):
    """ crossover of two genomes 
        a(a1, a2), b(b1, b2) => a(a1, b2), b(b1, a2)
    Args:
        a, b: two genomes of the same size
    Returns：
        genome a, b after single-point crossover
    """
    if len(a) != len(b):
        raise ValueError("Genomes a and b should be of the same length")

    length = len(a)
    if length < 2:
        return a, b

    # pick a random position to do crossover
    p = random.randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome, num = 1, prob = 0.5):
    """mutation of a genome with mutation probability to be prob.
        
    Args:
        genome: genmoe to be mutated
        num: number of genes on genome to be mutated
        prob: mutation probability
    Returns:
        return a genome after mutation
    """
    for _ in range(num):
        idx = random.randrange(len(genome))
        genome[idx] = genome[idx] if random() > prob else abs(genome[idx] - 1)

    return genome

def population_fitness(population, fitness_func):
    """ calc the fitness of population with the fitness_func
    Args:
        population: population List[genome]
        fitness_func: fitness function input: genome, output: fitness value
    Returns:
        the sum of genome fitness inside this population
    """

def sort_population(population, fitness_func):
    """ sort population with the fitness value
    return a sorted population (decreasing fitness value)
    """
    return sorted(population, key = fitness_func, reverse=True)

def genome_to_string(genome):
    return "".join(map(str, genome))

def print_stats(population, generation_id, fitness_func):
    print("GENERATION %02d" % generation_id)
    print("=============")
    print("Population: [%s]" % ", ".join([genome_to_string(gene) for gene in population]))
    print("Avg. Fitness: %f" % (population_fitness(population, fitness_func) / len(population)))
    sorted_population = sort_population(population, fitness_func)
    print(
        "Best: %s (%f)" % (genome_to_string(sorted_population[0]), fitness_func(sorted_population[0])))
    print("Worst: %s (%f)" % (genome_to_string(sorted_population[-1]),
                              fitness_func(sorted_population[-1])))
    print("")

    return sorted_population[0]

def run_evolution()



import random
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from consolemenu import SelectionMenu
import math
from collections import Counter

# todo stopping criteria: stop when 80% of the chromosome has same fitness.

def is_balanced(chromosome):
    """ check the if partition represented by chromosome is balanced

    balance: the difference between the amount of 1s and 0s should be at most 1.

    Args:
        chromosome
    Returns:
        true if the chromosome is balanced
        false if the chromosome is unbalanced
    """
    num_ones = np.count_nonzero(chromosome)
    num_zeros = len(chromosome) - num_ones
    
    return abs(num_ones - num_zeros) <= 1

def adjust(chromosome):
    """ adjust gene values of chromosome to make it balance

    mutate genes until it's balanced

    Args:
        chromosome
    """

    num_ones = np.count_nonzero(chromosome)
    num_zeros = len(chromosome) - num_ones
    zero_indices = [i for i in range(len(chromosome)) if chromosome[i] == 0]
    one_indices = [i for i in range(len(chromosome)) if chromosome[i] == 1]
    num_adjustment = len(chromosome) // 2 - min(num_ones, num_zeros) 
    if num_ones < num_zeros:
        # we need more one => flip zero to one
        index_list = np.random.choice(zero_indices, size=num_adjustment, replace=False)
        for idx in index_list:
            chromosome[idx] = 1
    elif num_ones > num_zeros:
        # we need more zero => flip one to zero
        index_list = np.random.choice(one_indices, size=num_adjustment, replace=False)
        for idx in index_list:
            chromosome[idx] = 0

def partition_visualizetion(filename, best_cutsize, best_assignment, population_size, generation_limit):
    """plot best assignment using matplot
    """
    fig, ax = plt.subplots()
    ax.set_title('''benchmark file: {}, net cutsize: {}'''.format(filename[:-4], best_cutsize))
    
    # hide ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_aspect('equal')
    ax.autoscale_view()



    left = best_assignment[0]
    right = best_assignment[1]
    max_nodes_per_side = num_nodes // 2 + 2
    num_rows = max_nodes_per_side if max_nodes_per_side <= 16 else math.ceil(math.sqrt(max_nodes_per_side))
    num_cols = 1 if max_nodes_per_side <= 16 else math.ceil(max_nodes_per_side / num_rows) + 1
    m = [[np.nan] * (2 * num_cols + 1) for _ in range(num_rows)]

    node_coord = [None]*num_nodes
    for idx, node in enumerate(left):
        i = idx // num_cols
        j = idx % num_cols
        m[i][j] = node
        node_coord[node] = [i,j]
        ax.text(j, i, str(m[i][j]), va='center', ha='center', fontsize="large")
    for idx, node in enumerate(right):
        i = idx // num_cols
        j = idx % num_cols + num_cols + 1
        m[i][j] = node
        node_coord[node] = [i,j]
        ax.text(j, i, str(m[i][j]), va='center', ha='center', fontsize = "large")
    ax.matshow(m)

    for net in netlist:
        src = net[0]
        sinks = net[1:]
        for sink in sinks:
            x = [node_coord[src][0], node_coord[sink][0]]
            y = [node_coord[src][1], node_coord[sink][1]]
            ax.plot(y, x)
    plt.show()

    # save figure
    fig.savefig("figs/{}_{}_{}".format(filename[:-4], population_size, generation_limit))

def line_chart(mincuts, fitnesses, filename, population_size, generation_limit):
    """plot line chart for mincut and fitness value per iteration
    reference: https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/subplots_demo.html
    """
    if len(mincuts) != len(fitnesses):
        raise ValueError("plot error. mincuts and fitnesses should be the same length")

    iterations = range(len(mincuts))
    fig, (ax1, ax2) = plt.subplots(1, 2) # two subplots mincut and fitness
    fig.suptitle("{} (population: {}, generation: {})".format(filename, population_size, generation_limit))
    # ax1: mincut plot
    ax1.set_title("mincut plot")
    ax1.plot(iterations, mincuts)
    ax1.set(xlabel="iterations", ylabel="mincut")

    # ax1: mincut plot
    ax2.set_title("fitness plot")
    ax2.plot(iterations, fitnesses)
    ax2.set(xlabel="iterations", ylabel="fitness")

    plt.show()
    fig.savefig("figs/" + "{}_line_chart_{}_{}".format(filename, population_size, generation_limit))

def parse_file(filepath):
    """ parse benchmarkfile
        store info of netlist, num_nodes(number of nodes), num_nets(number of nets)

    Args: 
        filepath: filepath of benchmark file
    """
    global netlist, num_nodes, num_nets
    # init netlist
    netlist = []
    with open(filepath, 'r') as f:
        for line_num, l in enumerate(f):
            line = l.strip().split()
            if not line: # be careful about empty lines
                break
            # print("{} {}".format(line_num, line))
            if line_num == 0: # first line: num_nodes, num_connections, num_rows, num_cols
                num_nodes = int(line[0])
                num_nets = int(line[1])
            
            else: # the rest of lines (contains netlist)
                nodes = []  # id of nodes in current net   
                for item in line[1:]:
                    node_id = int(item)
                    nodes.append(node_id)

                netlist.append(nodes)
    print(filepath)
    print("netlist",netlist)
    print("num_nodes", num_nodes)
    print("num_nets", len(netlist))

def list_files(directory="ass3_files/"):
    """ return a list of files under the directory
    Args:
        directory: the directory where files exist
    Returns:
        return a list of files under the directory. files are represented by their filename 
    """
    file_list =  [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    return file_list

def console_menu(select_list):
    """create a selection menu for selecting benchmark file in the console
    Args:
        select_list: a list of option for user to select from
    Returns: return the index of the selected item in the select_list
    """
    # menu = SelectionMenu(list_files(), "Select a benchmark file")
    return SelectionMenu.get_selection(select_list, title="Select a benchmark file")

def calc_net_cutsize(assignment):
    """ calculate the net cutsize of current assignment 
    Args: 
        assignment: an array represents the current assignment [[],[]]
        netlist: netlist parsed from benchmark file
    Return: net cutsize
    """
    cutsize = 0
    left = set(assignment[0])
    right = set(assignment[1])
    # fast way to check if a net is cut
    for net in netlist:
        if set(net).intersection(left) and set(net).intersection(right):
            cutsize += 1
    return cutsize

def generate_assignment(chromosome):
    """generated the assignment represented by chromosome
    Args:
        chromosome: a list of 0 and 1. represent a possible solution.
        0 and 1 stands for left and right part of the assignment.
        idx stands for the node number.
    Returns:
        assignment [[node1, node2, ..],[node3, node4, ..]]
    """
    left = []
    right = []

    for i, gene in enumerate(chromosome):
        if gene == 0:
            left.append(i)
        elif gene == 1:
            right.append(i)
    return [left, right]   

def generate_chromosome(length):
    """ generate and return a balanced chromosome list(a list of genes(0 or 1)) with given length

using np.randint to generate chromosome 1d array

    Args: 
        length: the length of the chromosome list. it should be the same as the pin numbers
    
    Returns:
        chromosome: a generated chromosome list consists of 0 and 1
    """
    chromosome = [0] * (length // 2) + [1] * (length - length//2)
    chromosome = np.asarray(chromosome)
    np.random.shuffle(chromosome)
    return chromosome

def generate_population(size, chromosome_length):
    """generate and return a population 1d array.

    Population is a array of chromosom

    Args: 
        size: size of the population (the length of population list)
        chromosome_length: the length of a chromosome list
    Returns:
        population: List[chromosome]
    """
    population = [generate_chromosome(chromosome_length) for _ in range(size)]
    return np.array(population)

def crossover_with_complement(a, b):
    """single point crossover with complement. return two offspring after crossover of chromosome a and b
    
    given chromosome a and b with crossover point to p devides each of them to two part a[a1:a2] b[b1:b2]
    offspring_a = [a1:b2]
    offspring_b = [a1: complement of b2]
    """
    p = random.randint(0, len(a) - 1) # a random crossover point
    a_new = np.append(a[:p], b[p:])
    b_new = np.append(a[:p], 1 - b[p:])
    return a_new, b_new

def single_point_crossover(a, b):
    """ single point crossover of two chromosomes 

    a(a1, a2), b(b1, b2) => a(a1, b2), b(b1, a2)
    Args:
        a, b: two chromosomes of the same size
    Returns：
        chromosome a, b after single-point crossover
    Raises:
        ValueError if the length of two chromosome are not the same
    """
    if len(a) != len(b):
        raise ValueError("chromosomes a and b should be of the same length")

    length = len(a)
    if length < 2:
        return a, b

    # pick a random position to do crossover
    p = random.randint(0, length - 1) # a random crossover point
    a_new = np.append(a[:p], b[p:])
    b_new = np.append(b[:p], a[p:])
    return a_new, b_new

def mutation(chromosome, num=1, prob=0.5):
    """mutation of a chromosome with mutation probability to be prob.
        
    Args:
        chromosome: genmoe to be mutated
        num: number of genes on chromosome to be mutated
        prob: mutation probability
    Returns:
        return a chromosome after mutation
    """
    for _ in range(num):
        idx = np.random.randint(0, len(chromosome)) # a random number from [0, n) n = len(chromosome)
        chromosome[idx] = chromosome[idx] if random.random() > prob else abs(chromosome[idx] - 1)

    return chromosome

def select_pairs(population, fitness_func):
    """
    randomly select the 2 chromosome population (weighted by fitness)
    Args:
        population: a list of chromosome
        fitness_func: function for calculating fitness of chromosome
    Returns:
        a pair of chromosome [chromosome1, chromosome2]
    """
    weights = [fitness_func(chromosome, population) for chromosome in population]
    return random.choices(population=population, weights=weights, k=2)

def calc_chromo_cutsize(chromosome):
    """calculate the cutsize of the chromosome. 
    it is actually the function to calculate net cutsize. 
    Args:
        chromosome: chromosome is a list of 0 and 1. represent a possible solution.
                0 and 1 stands for left and right part of the assignment.
                idx stands for the node number.
                so a chromosome stands for the distribution of pins in two groups
    Return: fitness(negated cutsize) of the chromosome.
    """
    assignment = generate_assignment(chromosome)
    return calc_net_cutsize(assignment)

def calc_fitness(chromosome, population):
    """calculate fitness of a chromosome inside a population
    
    fitness = fitness = (worst_cutsize - calc_chromo_cutsize(chromosome)) + (worst_cutsize - best_cutsize) / 3

    Args:
        chromosome: the chromosome array that we need to calculate fitness for
        population: the population the chromosome currently in
    Returns:
        return the fitness the given chromosome
    """
    population_sort_by_cutsize = sorted(population, key=calc_chromo_cutsize)
    worst = population_sort_by_cutsize[-1]
    best = population_sort_by_cutsize[0]
    worst_cutsize = calc_chromo_cutsize(worst)
    best_cutsize = calc_chromo_cutsize(best)
    fitness = (worst_cutsize - calc_chromo_cutsize(chromosome)) + (worst_cutsize - best_cutsize) / 3
    return fitness

def population_fitness(population, fitness_func):
    """ calc the unfitness of population with the unfitness_func
    Args:
        population: population List[chromosome]
        unfitness_func: fitness function input: chromosome, output: unfitness value(net cutsize)
    Returns:
        the sum of chromosome fitness inside this population
    """
    return sum([fitness_func(chromosome) for chromosome in population])

def exit_criterion(population, cutsize_limit=0):
    """ return True if at least 80% of chromosome has same fitness or min cutsize <= cutsize_upper_limit
    1. fitness criteria
    create a list of fitness and using collections.Counter count fitness occurrence.
    return True if the most common makes up >= 80% of the population size
    2. cutsize criteria
    return True if min cutsize <= cutsize_limit
    Args:
        population population List[chromosome]
    Returns:
        True: the population meet the exit criterion
        False: the population does not meet the exit criterion
    """
    fitnesses = [calc_fitness(chromosome, population) for chromosome in population]
    size = len(population)
    counter = Counter(fitnesses)
    top = counter.most_common(1)[0][1] # ex. [(5.333333333333334, 6)]

    population_sort_by_cutsize = sorted(population, key=calc_chromo_cutsize) # cutsize from low to high
    chromosome_mincut = population_sort_by_cutsize[0]
    min_cutsize = calc_chromo_cutsize(chromosome_mincut)
    
    if top >= 0.8 * size or min_cutsize <= cutsize_limit:
        return True
    else:
        return False


def ga(
    population_size,
    populate_func,
    fitness_func,
    selection_func,
    crossover_func,
    mutation_func,
    exit_criterion_func,
    cutsize_limit,
    generation_limit=100):
    """ genetic algorithm
    
    run evolution and return the final population after evolution
    
    Args:
        population_size: size of population
        pupulated_func: function for generating population
        unfitness_func: function for calculating unfitness(cutsize)
        cutsize_limit: the limit of cutsize. we exit evolution if we reach the limit(best cutsize <= unfitness_limit)
        crossover_func: function for crossover between two chromosome
        selection_func: function for selecting a pair of mates from population
        mutation_func: function for mutation
        exit_criterion_func: function for exit criterion
        cutsize_limit: cutsize limit used in exit criterion function
        generation_limit: the number of generation we want to go through
    Returns:
        final population after evolution
    """
    population = populate_func(size=population_size, chromosome_length=num_nodes)
    global mincuts, fitnesses # for plotting
    # empty lists first
    mincuts = []
    fitnesses = []

    for i in range(generation_limit):
        
        # sort population. fitness from high to low
        # population.sort(key= lambda chromosome : calc_fitness(chromosome, population), reverse=True)
        population = sorted(population, key= lambda chromosome : calc_fitness(chromosome, population), reverse=True)
        best_fitness = calc_fitness(population[0], population)
        population_mincut = sorted(population, key=calc_chromo_cutsize)
        best_cutsize = calc_chromo_cutsize(population_mincut[0])
        fitnesses.append(best_fitness)
        mincuts.append(best_cutsize)

        print("generation:{}, fit:{}, cutsize:{}".format(i, best_fitness, best_cutsize))

        # stop looping if  we meet the exit criterion
        if exit_criterion_func(population, cutsize_limit):
            break
        
        # pick the best two from population as the part of the next generation
        next_generation = population[0:2]
        # next_generation = [population[0]]

        for _ in range(len(population) // 2 - 1):
            # pick two to do crossover and mutation to generate next generation
            parents = selection_func(population, fitness_func)
            # crossover
            offspring_a, offspring_b = crossover_func(*parents)
            # mutation
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            if not is_balanced(offspring_a): adjust(offspring_a)
            if not is_balanced(offspring_b): adjust(offspring_b)
            next_generation.extend([offspring_a, offspring_b])
        
        # update population
        population = next_generation
    
    # return the final population after evolving
    # final sort
    population = sorted(population, key= lambda chromosome : calc_fitness(chromosome, population), reverse=True)
    best_fitness = calc_fitness(population[0], population)
    population_mincut = sorted(population, key=calc_chromo_cutsize)
    best_cutsize = calc_chromo_cutsize(population_mincut[0])
    fitnesses.append(best_fitness)
    mincuts.append(best_cutsize)
    return population

if __name__ == "__main__":
    # some global variables storing info from benchmark files
    netlist = []
    num_nets = 0
    num_nodes = 0

    mincuts = []
    fitnesses = []
    
    # for terminal menu
    directory = "ass3_files/"
    file_list = list_files(directory)
    filename = file_list[console_menu(file_list)]
    filepath = directory + filename
    
    parse_file(filepath)

    # hyper parameters
    population_size = 10
    generation_limit = 50

    final_population = ga(
        population_size=population_size,
        populate_func=generate_population,
        fitness_func=calc_fitness,
        selection_func=select_pairs,
        crossover_func=crossover_with_complement,
        mutation_func=mutation,
        exit_criterion_func=exit_criterion,
        cutsize_limit=0,
        generation_limit=generation_limit)
    final_population.sort(key= calc_chromo_cutsize)
    best_chromosome = final_population[0]
    best_assignment = generate_assignment(best_chromosome)
    best_cutsize = calc_net_cutsize(best_assignment)
    print('''
    FINAL best assignment: {}
    best_cutsize: {}
    '''.format(best_assignment, best_cutsize))
    # print("netlist", netlist)
    partition_visualizetion(filename, best_cutsize, best_assignment, population_size, generation_limit)
    line_chart(mincuts, fitnesses, filename[:-4], population_size, generation_limit)


import random
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from consolemenu import SelectionMenu

def plot(filename, best_cutsize, best_assignment):
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
    max_nodes_per_side = num_nodes
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
    fig.savefig("figs/" + filename[:-4])

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
    """ generate and return a chromosome list(a list of genes(0 or 1)) with given length

using np.randint to generate chromosome 1d array

    Args: 
        length: the length of the chromosome list. it should be the same as the pin numbers
    
    Returns:
        chromosome: a generated chromosome list consists of 0 and 1
    """

    return np.random.randint(2, size=length)

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
    p = random.randint(1, length - 1) # a random crossover point
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

def ga(
    populate_func,
    fitness_func,
    cutsize_limit,
    selection_func,
    crossover_func,
    mutation_func,
    generation_limit=100):
    """ genetic algorithm
    
    run evolution and return the final population after evolution
    
    Args:
        pupulated_func: function for generating population
        unfitness_func: function for calculating unfitness(cutsize)
        cutsize_limit: the limit of cutsize. we exit evolution if we reach the limit(best cutsize <= unfitness_limit)
        crossover_func: function for crossover between two chromosome
        selection_func: function for selecting a pair of mates from population
        mutation_func: function for mutation
        generation_limit: the number of generation we want to go through
    Returns:
        final population after evolution
    """
    population = populate_func(size=50, chromosome_length=num_nodes)

    for i in range(generation_limit):
        
        # sort population. fitness from high to low
        population = sorted(population, key= lambda chromosome : calc_fitness(chromosome, population))
        print("generation", i)
        # print("population", population)

        # stop looping if cutsize <= cutsize_limit (default is 0)
        if calc_chromo_cutsize(population[0]) <= cutsize_limit:
            break
        
        # pick the best two from population as the part of the next generation
        next_generation = population[0:2]

        for _ in range(len(population) // 2 - 1):
            # pick two to do crossover and mutation to generate next generation
            parents = selection_func(population, fitness_func)
            # crossover
            offspring_a, offspring_b = crossover_func(*parents)
            # mutation
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation.extend([offspring_a, offspring_b])
        
        # update population
        population = next_generation
    
    # return the final population after evolving
    return population

if __name__ == "__main__":
    # some global variables storing info from benchmark files
    netlist = []
    num_nets = 0
    num_nodes = 0
    
    # for terminal menu
    directory = "ass3_files/"
    file_list = list_files(directory)
    filename = file_list[console_menu(file_list)]
    filepath = directory + filename
    
    parse_file(filepath)

    final_population = ga(
        populate_func=generate_population,
        fitness_func=calc_fitness,
        cutsize_limit=0,
        selection_func=select_pairs,
        crossover_func=single_point_crossover,
        mutation_func=mutation,
        generation_limit=100)
    final_population.sort(key= calc_chromo_cutsize)
    best_chromesome = final_population[0]
    best_assignment = generate_assignment(best_chromesome)
    best_cutsize = calc_net_cutsize(best_assignment)
    print('''
    FINAL best assignment: {}
    best_cutsize: {}
    '''.format(best_assignment, best_cutsize))
    # print("netlist", netlist)
    plot(filename, best_cutsize, best_assignment)
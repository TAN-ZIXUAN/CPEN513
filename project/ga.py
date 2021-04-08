import random
import math
import os
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from consolemenu import SelectionMenu
import numpy as np
from collections import defaultdict
# https://github.com/kiecodes/genetic-algorithms/blob/master/algorithms/genetic.py
"""
chromesome is a list of 0 and 1. represent a possible solution.
0 and 1 stands for left and right part of the assignment.
idx stands for the node number.
so a chromesome stands for the distribution of pins in two groups

population is a list of chromesomes, aka many kinds of solution
we want evolve a solution that minimize the cutsize
"""
"""
todo optimize the data structure used in algorithm
todo 1. using numpy instead of normal list in python. numpy is faster. 
todo 2. using priority q to represent population to save time complexity waste on sorting in every iteration
todo 3. tunning hyper parameters. size of the population and generation times and exit criteria (exit when cutsize <= 0)
"""
 

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

def generate_assignment(chromesome):
    """generated the assignment represented by chromesome
    Args:
        chromesome: a list of 0 and 1. represent a possible solution.
        0 and 1 stands for left and right part of the assignment.
        idx stands for the node number.
    Returns:
        assignment [[node1, node2, ..],[node3, node4, ..]]
    """
    left = []
    right = []
    for i, gene in enumerate(chromesome):
        if gene == 0:
            left.append(i)
        elif gene == 1:
            right.append(i)
    return [left, right]

def list_files(directory="ass3_files/"):
    """ return a list of files under the directory
    Args:
        directory: the directory where files exist
    Returns:
        return a list of files under the directory. files are represented by their filename 
    """
    file_list =  [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    return file_list
def consol_menu(select_list):
    """create a selection menu for selecting benchmark file in the console
    Args:
        select_list: a list of option for user to select from
    Returns: return the index of the selected item in the select_list
    """
    # menu = SelectionMenu(list_files(), "Select a benchmark file")
    return SelectionMenu.get_selection(select_list, title="Select a benchmark file")


def cal_fitness(chromesome, population):
    population_sort_by_cutsize = sorted(population, key=cal_unfitness)
    worst = population_sort_by_cutsize[-1]
    best = population_sort_by_cutsize[0]
    worst_cutsize = cal_unfitness(worst)
    best_cutsize = cal_unfitness(best)
    fitness = (worst_cutsize - cal_unfitness(chromesome)) + (worst_cutsize - best_cutsize) / 3
    return fitness
def cal_net_cutsize(assignment):
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
def generate_chromesome(length):
    """ using random.choices generate chromesome list(a list of genes(0 or 1))
    Args: 
        length: the length of the chromesome list. it should be the same as the pin numbers
    
    Returns:
        chromesome: a generated chromesome list consists of 0 and 1
    """

    return random.choices([0, 1], k = length)

def generate_population(size, chromesome_length):
    """Population: List[chromesome]
    Args: 
        size: size of the population (the length of population list)
        chromesome_length: the length of a chromesome list
    Returns:
        population: List[chromesome]
    """
    return [generate_chromesome(chromesome_length) for _ in range(size)]

def single_point_crossover(a, b):
    """ crossover of two chromesomes 
        a(a1, a2), b(b1, b2) => a(a1, b2), b(b1, a2)
    Args:
        a, b: two chromesomes of the same size
    Returns：
        chromesome a, b after single-point crossover
    """
    if len(a) != len(b):
        raise ValueError("chromesomes a and b should be of the same length")

    length = len(a)
    if length < 2:
        return a, b

    # pick a random position to do crossover
    p = random.randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(chromesome, num = 1, prob = 0.5):
    """mutation of a chromesome with mutation probability to be prob.
        
    Args:
        chromesome: genmoe to be mutated
        num: number of genes on chromesome to be mutated
        prob: mutation probability
    Returns:
        return a chromesome after mutation
    """
    for _ in range(num):
        idx = random.randrange(len(chromesome))
        chromesome[idx] = chromesome[idx] if random.random() > prob else abs(chromesome[idx] - 1)

    return chromesome

def select_pairs(population, fitness_func):
    """
    randomly select the 2 chromesome population (weighted by fitness)
    Args:
        population: a list of chromesome
        fitness_func: function for calculating fitness of chromesome
    Returns:
        a pair of chromesome [chromesome1, chromesome2]
    """
    weights = [fitness_func(chromesome, population) for chromesome in population]
    return random.choices(population=population, weights=weights, k=2)

def cal_unfitness(chromesome):
    """calculate the unfitness of the chromesome. 
    it is actually the function to calculate net cutsize. 
    Args:
        chromesome: chromesome is a list of 0 and 1. represent a possible solution.
                0 and 1 stands for left and right part of the assignment.
                idx stands for the node number.
                so a chromesome stands for the distribution of pins in two groups
    Return: fitness(negated cutsize) of the chromesome.
    """
    assignment = generate_assignment(chromesome)
    return cal_net_cutsize(assignment)


def population_unfitness(population, unfitness_func):
    """ calc the unfitness of population with the unfitness_func
    Args:
        population: population List[chromesome]
        unfitness_func: fitness function input: chromesome, output: unfitness value(net cutsize)
    Returns:
        the sum of chromesome fitness inside this population
    """
    return sum([unfitness_func(chromesome) for chromesome in population])

def sort_population(population, unfitness_func):
    """ sort population with the fitness value
    return a sorted population (increase unfitness(cutsize))
    """
    return sorted(population, key=unfitness_func)

def chromesome_to_string(chromesome):
    return "".join(map(str, chromesome))


def run_evolution(
    populate_func,
    fitness_func,
    # unfitness_limit,
    selection_func,
    crossoer_func,
    mutation_func,
    generation_limit=100,):
    """ run evolution and return the final population after evolution
    Args:
        pupulated_func: function for generating population
        unfitness_func: function for calculating unfitness(cutsize)
        # unfitness_limit: the limit of unfitness(cutsize). we exit evolution if we reach the fitness limit(best unfitness(best cutsize) <= unfitness_limit)
        selection_func: function for selecting a pair of mates from population
        mutation_func: function for mutation
        generation_limit: the number of generation we want to go through
    Returns:
        final population after evolution
    """

    #generate population
    population = populate_func(size=100, chromesome_length=num_nodes)

    for i in range(generation_limit):
        
        # sort population. fitness from high to low
        population = sorted(population, key= lambda chromesome : cal_fitness(chromesome, population))
        print("generation", i)
        print("population", population)
        # check if it reaches the fitness limit
        # if fitness_func(population[0]) <= unfitness_limit:
        #     break
        
        # pick the best two from population as the part of the next generation
        next_generation = population[0:2]

        for _ in range(len(population) // 2 - 1):
            # pick two to do crossover and mutation to generate next generation
            parents = selection_func(population, fitness_func)
            # crossover
            offspring_a, offspring_b = crossoer_func(*parents)
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
    filename = file_list[consol_menu(file_list)]
    filepath = directory + filename
    
    parse_file(filepath)

    final_population = run_evolution(generate_population, cal_fitness, select_pairs, single_point_crossover, mutation, 100)
    final_population.sort(key= cal_unfitness)
    best_chromesome = final_population[0]
    best_assignment = generate_assignment(best_chromesome)
    best_cutsize = cal_net_cutsize(best_assignment)
    print('''
    FINAL best assignment: {}
    best_cutsize: {}
    '''.format(best_assignment, best_cutsize))
    # print("netlist", netlist)
    plot(filename, best_cutsize, best_assignment)
    



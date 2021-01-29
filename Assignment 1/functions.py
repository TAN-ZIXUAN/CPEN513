import config as c
import pygame
from node import Node


def parse_file(file): #example file  # [['40', '20'], ['101'], ['25', '1'], ['26', '1'], ['27', '1']
    # convert string to integer
    for i in range(len(file)):
        for j in range(len(file[i])):
            file[i][j] = int(file[i][j])
    print(file)
    
    c.NUM_X, c.NUM_Y = file[0][0], file[0][1]
    c.SIZE_X = c.WIDTH / c.NUM_X
    c.SIZE_Y = c.WIDTH / c.NUM_Y
    c.NUM_OBS = file[1][0]

    for i in range(c.NUM_OBS):
        c.OBS.append((file[2 + i][0], file[2 + i][1]))
    
    c.NUM_WIRE = file[2 + c.NUM_OBS][0]

    for i in range(c.NUM_WIRE):
        source = (file[2 + c.NUM_OBS + 1 + i][1], file[2 + c.NUM_OBS + 1 + i][2])
        c.WIRE2SOURCE[i] = source
        c.WIRE2NUM_PINS[i] = file[2 + c.NUM_OBS + 1 + i][0]
        c.SOURCES.append(c.WIRE2SOURCE[i])
        # print("sources", c.SOURCES)

        tmp = 0
        for j in range(c.WIRE2NUM_PINS[i] - 1):
            sink = (file[2 + c.NUM_OBS + 1 + i][3 + j + tmp], file[2 + c.NUM_OBS + 1 + i][4 + j + tmp])
            c.SOURCE2SINKS[source].append(sink)
            c.WIRE2SINK[i].append(sink)
            c.SINKS.append(sink)
            tmp += 1
    # print("sources", c.SOURCES) #{(4, 2), (29, 10), (24, 4), (3, 5)}
    # print("wire2sink", c.WIRE2SINK) # {0: [(24, 2), (24, 11)], 1: [(24, 9), (5, 5)], 2: [(29, 3)], 3: [(34, 8)]})

# creating grid (made of node,size: num_x*num_y )
def create_grid(num_x, num_y):
    grid = []

    for i in range(num_x):
        grid.append([])
        for j in range(num_y):
            node = Node(i, j)
            grid[i].append(node)

    return grid

# draw grid boarders in the surface
def draw_grid(surface, num_x, size_x): 
    width = num_x * size_x
    for i in range(num_x):
        pygame.draw.line(surface, c.GREY, (0, i * size_x), (width, i * size_x))
        for j in range(num_x):
            pygame.draw.line(surface, c.GREY, (j * size_x, 0), (j * size_x, width))


# paint node with its colour property
def paint_nodes(surface, grid):
    for row in grid:
        for node in row:
            rect = (node.coor_x, node.coor_y, c.SIZE_X, c.SIZE_Y)
            pygame.draw.rect(surface, node.colour, rect)

def draw(surface, grid, num_x, size_x): # combination of draw_grid and paint_nodes
    paint_nodes(surface, grid)
    draw_grid(surface, num_x, size_x)



def update_grid_colour(grid): # update grid color: source sink and obstacles
    for x, y in c.OBS:
        c.GRID[x][y].colour = c.BLACK
    for wire in c.WIRE2SOURCE:
        src_x, src_y = c.WIRE2SOURCE[wire]
        color_tmp = 50+wire*30
        while color_tmp > 255:
            color_tmp -= 40
        c.GRID[src_x][src_y].colour = (color_tmp, 100, 60)

        for sink_x, sink_y in c.WIRE2SINK[wire]:
            c.GRID[sink_x][sink_y].colour = (color_tmp, 100, 60)


#heuristic return manhattan distance between two nodes p1 and p2
def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def backtracing(pre, curr, draw):
	while curr in pre:
		curr = pre[curr]
		curr.mark_path()

		draw()
# algorithm


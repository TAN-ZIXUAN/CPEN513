import config as c
import sys
import numpy as np



def generate_grid(rows, cols):
    grid = np.full((rows, cols), c.T_UNVIS)

    for row, col in c.OBS:
        grid[row][col] = c.T_OBS
    
    for row, col in c.SOURCES:
        grid[row][col] = c.T_SOURCE #(wire_number, type of pins)

    for row, col in c.SINKS:
        grid[row][col] = c.T_SINK #(wire_number, type of pins)
    
    return grid
def color_grid(grid): # return a grid consit of colors (also call this to update color of each cell)
    (rows, cols) = grid.shape
    
    colorGrid = np.full((rows, cols, 3), c.COLOR_UNVIS)
    # print("orig", colorGrid)
    for row, col in c.OBS:
        colorGrid[row][col] = c.COLOR_OBS


    for i in range(rows):
        for j in range(cols): 
            # visited cell
            if grid[i][j] > c.T_SOURCE:
                colorGrid[i][j] = c.COLOR_VIS

            # path cell
            elif grid[i][j] == c.T_PATH:
                colorGrid[i][j] = c.COLOR_PATH



    # for each group of source ans sinks
    for wire in c.WIRE2SOURCE:
        src_x, src_y = c.WIRE2SOURCE[wire]
        color_tmp = 50+wire*30
        while color_tmp > 255:
            color_tmp -= 40
            colorGrid[src_x][src_y] = (color_tmp, 100, 60)

        for sink_x, sink_y in c.WIRE2SINK[wire]:
            colorGrid[sink_x][sink_y] = (color_tmp, 100, 60)

    return colorGrid


def parse_file(file_path): #example file  # [['40', '20'], ['101'], ['25', '1'], ['26', '1'], ['27', '1']
    loaded_file = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            loaded_file.append((line.strip().split()))

    
    # convert string to integer
    file = loaded_file
    for i in range(len(file)):
        for j in range(len(file[i])):
            file[i][j] = int(file[i][j])
    
    print("loaded_file", file)
    c.NUM_X, c.NUM_Y = file[0][0], file[0][1]
    c.SIZE_X = c.WIDTH / c.NUM_X
    c.SIZE_Y = c.WIDTH / c.NUM_Y
    c.NUM_OBS = file[1][0]

    for i in range(c.NUM_OBS):
        c.OBS.add((file[2 + i][0], file[2 + i][1]))

    c.NUM_WIRE = file[2 + c.NUM_OBS][0]

    for i in range(c.NUM_WIRE):
        source = (file[2 + c.NUM_OBS + 1 + i][1], file[2 + c.NUM_OBS + 1 + i][2])
        c.WIRE2SOURCE[i] = source
        c.WIRE2NUM_PINS[i] = file[2 + c.NUM_OBS + 1 + i][0]
        c.SOURCES.add(c.WIRE2SOURCE[i])
        # print("sources", c.SOURCES)
        c.PIN2WIRE[(source)] = i

        tmp = 0
        for j in range(c.WIRE2NUM_PINS[i] - 1):
            sink = (file[2 + c.NUM_OBS + 1 + i][3 + j + tmp], file[2 + c.NUM_OBS + 1 + i][4 + j + tmp])
            c.SOURCE2SINKS[source].append(sink)
            c.WIRE2SINK[i].append(sink)
            c.SINKS.add(sink)
            c.PIN2WIRE[(sink)] = i
            tmp += 1

    
    # print("wire2souce", c.WIRE2SOURCE)
    # print("wire2sink", c.WIRE2SINK)
    # print("source", c.SOURCES)
    # print("pin2wire", c.PIN2WIRE)
    grid = generate_grid(c.NUM_X, c.NUM_Y)
    # print("grid", grid)
    colorGrid = color_grid(grid)
    # print("color grid", colorGrid)
    c.GRID = grid
    c.COLOR_GRID = colorGrid
    return grid  # return grid file

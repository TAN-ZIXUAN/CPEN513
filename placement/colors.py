import matplotlib
import matplotlib.colors as mcolors
# color_list = list(matplotlib.colors.cnames.values())

# css_color = list(mcolors.CSS4_COLORS)
# print(len(color_list))
# print(color_list)
# print(len(css_color))
hex_colors = []

color_file = "hex_color.txt"
with open(color_file, 'r') as f:
    for line in f:
        l = line.strip().split()
        # print(line[-1])
        hex_color.append(l[-1])


# print(len(hex_colors))
# print(hex_colors)

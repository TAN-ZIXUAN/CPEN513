
from block import Block
# parent class is Block
class Pin(Block):
    def __init__(self, row, col, size_x, size_y):
        Block.__init__(self, row, col, size_x, size_y)
        
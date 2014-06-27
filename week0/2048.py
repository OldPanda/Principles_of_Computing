"""
Clone of 2048 game.
"""

import poc_2048_gui  
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    length = len(line)
    new_line = [0 for dummy_i in range(length)]
    index = 0
    
    nonzero1 = -1
    nonzero2 = -2
    for item in range(length):
        if line[item] == 0:
            continue
        else:
            if nonzero1 < 0:
                nonzero1 = line[item]
            else:
                nonzero2 = line[item]
        if nonzero1 >= 0 and nonzero2 >= 0:
            if nonzero1 == nonzero2:
                new_line[index] = nonzero1 + nonzero2
                nonzero1 = -1
                nonzero2 = -2
                index += 1
            else:
                new_line[index] = nonzero1
                nonzero1 = nonzero2
                nonzero2 = -2
                index += 1
    if nonzero1 >= 0:
        new_line[index] = nonzero1
    return new_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.value = self.reset()
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        return [[0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ""
        for row in self.value:
            string += str(row)
            string += "\n"
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width
                            
    def new_list_gen(self, value_list, offset, dimension):
        """
        This function is mainly used for reducting branches in 
        'move' function. 
        Merge value_list to a new line via 'merge' function. 
        """
        if offset[dimension] < 0:
            value_list.reverse()
            new_list = merge(value_list)
            new_list.reverse()
        else:
            new_list = merge(value_list)
        return new_list

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        offset = OFFSETS[direction]
        if offset[0] != 0:
            for col_index in range(self.grid_width):
                value_list = [self.value[row_index][col_index] for row_index in range(self.grid_height)]
                new_list = self.new_list_gen(value_list, offset, 0)
                for row_index in range(self.grid_height):
                    if self.value[row_index][col_index] != new_list[row_index]:
                        self.value[row_index][col_index] = new_list[row_index]
                        moved = True
        else:
            for row_index in range(self.grid_height):
                value_list = [self.value[row_index][col_index] for col_index in range(self.grid_width)]
                new_list = self.new_list_gen(value_list, offset, 1)
                for col_index in range(self.grid_width):
                    if self.value[row_index][col_index] != new_list[col_index]:
                        self.value[row_index][col_index] = new_list[col_index]
                        moved = True
        if moved:
            self.new_tile()
        
    
    def find_empty_tile(self):
        """
        Find a empty tile randomly
        """
        row = random.randrange(0, self.grid_height)
        col = random.randrange(0, self.grid_width)
        while self.value[row][col] != 0:
            row=random.randrange(0, self.grid_height)
            col=random.randrange(0, self.grid_width)
        return row, col
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        seed = random.random()
        if seed < 0.9:
            tile = 2
        else:
            tile = 4
        row, col = self.find_empty_tile()
        self.set_tile(row, col, tile)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.value[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self.value[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
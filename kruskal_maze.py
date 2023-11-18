'''
class KruskalMaze
The maze is represented as a 2D array of cells. Each cell is either a wall or a
passage. The maze is generated by removing walls between cells. The algorithm
starts with a grid of passages and walls. The (odd, odd) cells are passages and
the remaining cells are walls. It then removes walls between cells until all
cells are connected. Each passage is represented as a set of connected cells in
the disjoint set data structure. The algorithm removes walls by selecting a
random wall and checking if the cells on either side of the wall are connected.
If the cells are not connected, the wall is removed and the cells are connected.
If the cells are already connected, the wall is left in place. The algorithm
continues until all cells are connected.
'''
import random
import time
import tkinter as tk

from cell import Cell
from disjoint_set import DisjointSet

CELL_WALL = 1
CELL_PASSAGE = 0
WINDOW_SIZE = 750
CELL_DISPLAY_FILL = 'black'
ANIMATION_DELAY = 1000  # divided by the (number of cells) ^ 2 in the maze


class KruskalMaze:
    def __init__(self, width, height):
        # Initialize the maze. The (odd, odd) cells are passages and the remaining cells are walls.
        self.maze_width = width * 2 + 1
        self.maze_height = height * 2 + 1
        self.maze = []
        for y in range(self.maze_height):
            row = []
            for x in range(self.maze_width):
                if x % 2 == 1 and y % 2 == 1:
                    row.append(CELL_PASSAGE)
                else:
                    row.append(CELL_WALL)
            self.maze.append(row)

        # Initialize the disjoint set data structure. Exclude the walls between cells.
        self.disjoint_set = DisjointSet(width, height)

        # Create the tkinter window.
        self.root = tk.Tk()
        self.root.title('Maze Generation with Kruskal\'s Algorithm')
        if width > height:
            self.root.geometry(str(WINDOW_SIZE) + 'x' +
                               str(WINDOW_SIZE * height // width))
            self.canvas = tk.Canvas(self.root, width=WINDOW_SIZE,
                                    height=WINDOW_SIZE * height // width)
        else:
            self.root.geometry(str(WINDOW_SIZE * width // height) + 'x' +
                               str(WINDOW_SIZE))
            self.canvas = tk.Canvas(self.root, width=WINDOW_SIZE * width // height,
                                    height=WINDOW_SIZE)
        self.canvas.pack()

        # Generate the maze.
        self.generate_maze_kruskal()
        self.root.mainloop()

    def generate_maze_kruskal(self):
        '''
        Description: This function generates the maze.
        '''
        removable_walls = []
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                cell = Cell(x, y)
                if self.is_wall_removable(cell):
                    removable_walls.append(cell)

        # Mark starting and ending cells
        

        # Remove walls until all cells are connected.
        while self.disjoint_set.set_count > 1 and removable_walls:
            # Select a random wall.
            wall_index = random.randint(0, len(removable_walls) - 1)
            wall = removable_walls[wall_index]
    
            # Check if the cells on either side of the wall are connected.
            if wall.x % 2 == 1:
                cell1 = Cell(wall.x, wall.y - 1)
                cell2 = Cell(wall.x, wall.y + 1)
            else:
                cell1 = Cell(wall.x - 1, wall.y)
                cell2 = Cell(wall.x + 1, wall.y)
    
            if self.disjoint_set.find(cell1) != self.disjoint_set.find(cell2):
                # Remove the wall.
                self.maze[wall.y][wall.x] = CELL_PASSAGE
                self.disjoint_set.union(cell1, cell2)
    
                # Remove the wall from the list of removable walls.
                removable_walls.pop(wall_index)
    
                # Pause the execution to simulate animation delay.
                self.draw_maze()  # Update the canvas
                self.root.update()
                delay = ANIMATION_DELAY / \
                    (self.maze_width * self.maze_height) ** 2
                time.sleep(delay)
        self.mark_start_end_cells()

    def is_wall_removable(self, cell):
        '''
        Description: This function returns whether the wall at the given coordinates can be removed.
        Parameters: cell - The cell.
        Return: Whether the wall at the given coordinates can be removed.
        '''
        # Check if the cell is a wall.
        if self.maze[cell.y][cell.x] == CELL_WALL:
            # Check if the cell is on the edge of the maze.
            if cell.x == 0 or cell.x == self.maze_width - 1 or cell.y == 0 or cell.y == self.maze_height - 1:
                return False

            # Check if the cell is adjacent to a passage.
            if self.maze[cell.y - 1][cell.x] == CELL_PASSAGE or self.maze[cell.y + 1][cell.x] == CELL_PASSAGE or self.maze[cell.y][cell.x - 1] == CELL_PASSAGE or self.maze[cell.y][cell.x + 1] == CELL_PASSAGE:
                return True

            return False

        return False

    def draw_maze(self):
        '''
        Description: This function draws the maze in tkinter.
        '''
        self.canvas.delete('all')  # Clear the canvas

        # Draw the maze.
        cell_size = WINDOW_SIZE // max(self.maze_width, self.maze_height)
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                if self.maze[y][x] == CELL_WALL:
                    self.canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1)
                                                 * cell_size, (y + 1) * cell_size, fill=CELL_DISPLAY_FILL)
                elif self.maze[y][x] == 'START':  # Draw starting cell in red
                    self.canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1)
                                                 * cell_size, (y + 1) * cell_size, fill='red')
                elif self.maze[y][x] == 'END':  # Draw ending cell in green
                    self.canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1)
                                                 * cell_size, (y + 1) * cell_size, fill='green')
                else:
                    # Set passable cells to a constant white color.
                    self.canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1)
                                                 * cell_size, (y + 1) * cell_size, fill='white')

        # Update the canvas.
        self.root.update()
    def mark_start_end_cells(self):
        '''
        Description: Marks a random cell as the starting cell (red) and another random cell as the ending cell (green).
        '''
        # Get random coordinates for the starting cell.
        start_x = random.randint(1, self.maze_width - 2)
        start_y = random.randint(1, self.maze_height - 2)
        while self.maze[start_y][start_x] != CELL_PASSAGE:
            start_x = random.randint(1, self.maze_width - 2)
            start_y = random.randint(1, self.maze_height - 2)

        # Get random coordinates for the ending cell (ensuring it's different from the starting cell).
        end_x = random.randint(1, self.maze_width - 2)
        end_y = random.randint(1, self.maze_height - 2)
        while self.maze[end_y][end_x] != CELL_PASSAGE or (start_x == end_x and start_y == end_y):
            end_x = random.randint(1, self.maze_width - 2)
            end_y = random.randint(1, self.maze_height - 2)

        # Mark the starting and ending cells with red and green colors respectively.
        cell_size = WINDOW_SIZE // max(self.maze_width, self.maze_height)
        self.canvas.create_rectangle(
            start_x * cell_size, start_y * cell_size,
            (start_x + 1) * cell_size, (start_y + 1) * cell_size,
            fill='red'
        )
        self.canvas.create_rectangle(
            end_x * cell_size, end_y * cell_size,
            (end_x + 1) * cell_size, (end_y + 1) * cell_size,
            fill='green'
        )

        

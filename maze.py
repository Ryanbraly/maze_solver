from graphics import Cell
import time
import random

class Maze:

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        
        if seed:
            random.seed(seed)

        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        self.reset_cells_visited()

    def create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self.cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cell(i, j)

    def draw_cell(self, i, j):
        if self.win is None:
            return
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.025)

    def break_entrance_and_exit(self):
        top_left = self.cells[0][0]
        bottom_right = self.cells[self.num_cols - 1][self.num_rows - 1]

        top_left.has_top_wall = False
        self.draw_cell(0, 0)
        bottom_right.has_bottom_wall = False
        self.draw_cell(self.num_cols - 1, self.num_rows - 1)

    def break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        while True:
            to_visit = []
                        
            # left
            if i > 0 and not self.cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            # right
            if i < self.num_cols - 1 and not self.cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            # up
            if j > 0 and not self.cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            # down
            if j < self.num_rows - 1 and not self.cells[i][j + 1].visited:
                to_visit.append((i, j + 1))

            # check to see if there's anything in to_visit after trying to populate it - bail if not
            if len(to_visit) == 0:
                self.draw_cell(i, j)
                return
            
            # choose a new direction at random
            direction_index = random.randrange(len(to_visit))
            next_index = to_visit[direction_index]

            # remove wall between current cell and cell we've selected to visit next
            # right
            if next_index[0] == i + 1:
                self.cells[i][j].has_right_wall = False
                self.cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self.cells[i][j].has_left_wall = False
                self.cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self.cells[i][j].has_bottom_wall = False
                self.cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self.cells[i][j].has_top_wall = False
                self.cells[i][j - 1].has_bottom_wall = False

            # visit next cell, making method recursive
            self.break_walls_r(next_index[0], next_index[1])


    def reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False


    def solve(self):
        return self.solve_r(0, 0)

    def solve_r(self, i, j):
        self.animate()
        self.cells[i][j].visited = True

        # check if we're at the bottom right (exit) cell
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        
        # check adjacent cells
        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self.cells[i][j].has_left_wall
            and not self.cells[i - 1][j].visited
        ):
            self.cells[i][j].draw_move(self.cells[i - 1][j])
            if self.solve_r(i - 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.num_cols - 1
            and not self.cells[i][j].has_right_wall
            and not self.cells[i + 1][j].visited
        ):
            self.cells[i][j].draw_move(self.cells[i + 1][j])
            if self.solve_r(i + 1, j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self.cells[i][j].has_top_wall
            and not self.cells[i][j - 1].visited
        ):
            self.cells[i][j].draw_move(self.cells[i][j - 1])
            if self.solve_r(i, j - 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.num_rows - 1
            and not self.cells[i][j].has_bottom_wall
            and not self.cells[i][j + 1].visited
        ):
            self.cells[i][j].draw_move(self.cells[i][j + 1])
            if self.solve_r(i, j + 1):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[i][j + 1], True)

        # by this point, if we're not finding any adjacent cells we can move to, we've taken a wrong turn
        return False

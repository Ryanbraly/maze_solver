from tkinter import Tk, BOTH, Canvas

class Window:

    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(self.root, bg="white", width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.is_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)


    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
        

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)



class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:

    def __init__(self, point_1, point_2):
        self.p1 = point_1
        self.p2 = point_2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

class Cell:

    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.win.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.win.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.win.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        line_color = "red"
        if undo:
            line_color = "gray"
        self_center = Point(((self.x1 + self.x2) // 2), ((self.y1 + self.y2) // 2))
        other_center = Point(((to_cell.x1 + to_cell.x2) // 2), ((to_cell.y1 + to_cell.y2) // 2))
        line = Line(self_center, other_center)
        self.win.draw_line(line, line_color)

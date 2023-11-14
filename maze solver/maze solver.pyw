'''
Source: https://github.com/mat4x/GUI-ized

This is one of my work in the collection of
converting normal programs into GUI applications
using Python's tkinter module.

This program solves the maze using:
    - DFS algorithm
    - BFS algorithm
    - A*  algorithm

The 'visualization' option can be used
to see the working of the algorithms.

The program opens with a 'SAMPLE' puzzle.
Click the 'RESET' button to enter fresh values.

NOTE1: the maze tiles are stored as linear lists
but operation are performed in a matrix manner
the conversion from matrix cordinate to linear indices
can be identifed as 'idx = x*self.maze_size + y' | idx-list index; (x,y)-matrix coords
*NOTE1: The above "issue" has been resolved. The self.maze_grid is a matrix and not a linear list

NOTE2: Shortcuts available
 R - Reset
 T - Sample
 V - Viualise
 Enter/Space - Solve Maze
 E, W, S, G  - Empty, Wall, Start, Goal

- Completed on 12/05/2022
'''

from tkinter import Tk, Frame, Button, Label, Scale, HORIZONTAL, SOLID, DISABLED, NORMAL
import itertools
import heapq
import random
import os
import re


# used for A* algorithm
class PriorityQueue:
    def __init__(self):
        self.elements = []
    def __str__(self):
        return str(self.elements)
    def is_empty(self):
        return not self.elements
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    def get(self):
        return heapq.heappop(self.elements)[1]


class MazeSolver:
    def __init__(self, win):
        
        # window setup
        self.win = win
        self.win.title("Maze Solver - Mayur Sharma")
        DIMS = (600, 600)
        BACKGROUND   = '#ffffeb'
        BUTTON_COLOR = "#e5d273"
        BUTTON_FONT  = "#1a1100"
        self.win.geometry(f'{DIMS[0]}x{DIMS[1]}+400+50')
        self.win.minsize(DIMS[0], DIMS[1])
        self.win.config(bg=BACKGROUND)

        # flags and shared variables
        self.maze_grid      = []
        self.visited_cells  = []     # used to visualise path
        self.is_maze_solved = False  # used to stop visualizing path if reset interrupt
        self.all_buttons    = dict()
        self.offsets = { 'up'   : (-1, 0),
                         'left' : (0, -1),
                         'down' : (+1, 0),
                         'right': (0, +1) }
        
        # Yellow and Blue Theme
        self.state_colour = {
                         'empty' : "#fffff7",
                         'wall'  : "#004466",
                         'start' : "#428db3",
                         'goal'  : "#5c8599" }


        # exit button and title
        Label(self.win, text="Maze Solver", fg='#99752e', font=("8514oem", 35, 'bold'),
           bg=BACKGROUND ).place(relx=0.5, y=10, anchor='n', relwidth=1)
        Button(self.win, text='X', bg='#e5e573', fg=BUTTON_FONT, font=(None, 10, 'bold'),
           width=3, command=self.win.quit).place(relx=0.99, rely=0.01, anchor='ne')
      
        # maze grid controls
        self.maze_scale = Scale(self.win, from_=2, to=15, bg=BACKGROUND, orient=HORIZONTAL)
        Label(self.win, text="Maze Size", fg=BUTTON_FONT, bg=BACKGROUND).place(relx=0.2,rely=0.13, anchor='center')
        self.maze_scale.place(relx=0.2, rely=0.18, anchor='center')
        self.maze_scale.set(5)

        self.all_buttons["Reset"]     = Button(self.win, text="(Re)Set Grid", width=12, relief=SOLID, bd=0.5, fg=BUTTON_FONT, bg=BUTTON_COLOR, command=self.update_maze_tiles)
        self.all_buttons["Solve"]     = Button(self.win, text="Solve",        width=12, relief=SOLID, bd=0.5, fg=BUTTON_FONT, bg=BUTTON_COLOR, command=self.solve_maze)
        self.all_buttons["Visualize"] = Button(self.win, text="Visualize Algorithm", width=22, relief=SOLID,  fg=BUTTON_FONT, bd=0.5, bg=BUTTON_COLOR, command=self.visualize_maze_solution)
        self.all_buttons["Reset"].place(relx=0.45, rely=0.15, anchor='center')
        self.all_buttons["Solve"].place(relx=0.45, rely=0.2, anchor='center')
        self.all_buttons["Visualize"].place(relx=0.75, rely=0.2, anchor='center')

        # maze tile buttons
        Label(self.win, text="Tile Setup", fg=BUTTON_FONT, bg=BACKGROUND, font=(None, 10), bd=0).place(relx=0.9, rely=0.28, anchor='center')
        config_btn_pos = [0.36 + 0.125*m for m in range(4)]    # start + spacing
        
        self.config_btns = []
        self.config_btns.append( Button(self.win, text="E", fg="#333", bg=self.state_colour["empty"], command=lambda: self.set_state("empty"), relief=SOLID, bd=0.5) )
        self.config_btns.append( Button(self.win, text="W", fg="#fff", bg=self.state_colour["wall"],  command=lambda: self.set_state("wall"),  relief=SOLID, bd=0.5) )
        self.config_btns.append( Button(self.win, text="S", fg="#fff", bg=self.state_colour["start"], command=lambda: self.set_state("start"), relief=SOLID, bd=0.5) )
        self.config_btns.append( Button(self.win, text="G", fg="#fff", bg=self.state_colour["goal"],  command=lambda: self.set_state("goal"),  relief=SOLID, bd=0.5) )
        [btn.place(relx=0.9, rely=y, height=40, width=40, anchor='center') for btn,y in zip(self.config_btns, config_btn_pos)]
        
        config_lbls = []
        config_lbls.append( Label(self.win, text="Empty", fg=BUTTON_FONT, bg=BACKGROUND, bd=0) )
        config_lbls.append( Label(self.win, text="Wall",  fg=BUTTON_FONT, bg=BACKGROUND, bd=0) )
        config_lbls.append( Label(self.win, text="Start", fg=BUTTON_FONT, bg=BACKGROUND, bd=0) )
        config_lbls.append( Label(self.win, text="Goal",  fg=BUTTON_FONT, bg=BACKGROUND, bd=0) )
        [lbl.place(relx=0.9, rely=y, anchor='center') for lbl,y in zip(config_lbls, [y+0.05 for y in config_btn_pos])]

        self.all_buttons["sample_mazes"] = Button(self.win, text="Sample Mazes", relief=SOLID, fg=BUTTON_FONT, bg=BUTTON_COLOR, bd=0.5, command=self.sample_maze)
        self.all_buttons["sample_mazes"].place(relx=0.9, rely=0.87, anchor='center')

        # maze solving algorithm selection
        def set_solver(type_="A*"):
            mapping = {"DFS":[self.DFS,0], "BFS":[self.BFS,1], "A*":[self.A_star,2]}
            self.solver = mapping[type_][0]
            for btn in solver_types:
                btn.config(bg = "orange" if btn["text"] == type_ else "yellow")

        solver_types = []
        solver_types.append( Button(self.win, text="DFS", relief=SOLID, bd=0.5, fg=BUTTON_FONT, command=lambda: set_solver("DFS")) )
        solver_types.append( Button(self.win, text="BFS", relief=SOLID, bd=0.5, fg=BUTTON_FONT, command=lambda: set_solver("BFS")) )
        solver_types.append( Button(self.win, text="A*" , relief=SOLID, bd=0.5, fg=BUTTON_FONT, command=lambda: set_solver("A*" )) )
        [btn.place(relx=x, rely=0.15, width=40, anchor="center") for btn,x in zip(solver_types,[0.65,0.75,0.85])]
        set_solver()

        # maze area
        length = (min(DIMS)-100)*0.8
        self.maze_area = Frame(self.win, bg='black', bd=2, relief=SOLID)
        self.maze_area.place(relx=0.45, rely=0.575, anchor='center', height=length, width=length)

        # initial setup
        self.set_bindings()
        self.update_maze_tiles()
        self.set_state()
        self.sample_maze()      # optional but okay


    def set_state(self, state = "empty"):
        self.state_set_to = state
        mapping = {"empty": 'E', "wall": 'W', "start": 'S', "goal": 'G'}
        text = mapping[state]
        for btn in self.config_btns:
            if btn["text"] == text: btn.config(bd = 3)
            else: btn.config(bd = 0.5)


    def set_bindings(self):
        self.win.bind('<Return>', lambda e: self.solve_maze() )
        self.win.bind('<space>',  lambda e: self.solve_maze() )
        self.win.bind('<Double-Escape>', lambda e: self.win.quit() )
        self.win.bind('<r>', lambda e: self.update_maze_tiles() )
        self.win.bind('<t>', lambda e: self.sample_maze() )
        self.win.bind('<v>', lambda e: self.visualize_maze_solution() )

        self.win.bind('<e>', lambda e: self.set_state("empty") )
        self.win.bind('<w>', lambda e: self.set_state("wall") )
        self.win.bind('<s>', lambda e: self.set_state("start") )
        self.win.bind('<g>', lambda e: self.set_state("goal") )


    def update_maze_tiles(self):
        self.maze_grid.clear()
        self.is_maze_solved = False
        self.start_cell = None
        self.goal_cell  = None
        self.maze_size  = self.maze_scale.get()
        [child.destroy() for child in self.maze_area.winfo_children()]

        n = self.maze_size * 2
        for y in range(1, n, 2):
            self.maze_grid.append(list())
            for x in range(1, n, 2):
                self.maze_grid[-1].append( Button(self.maze_area, relief=SOLID, bd=0.5) )
                self.maze_grid[-1][-1].place(relx=x/n, rely=y/n, relwidth=2/n, relheight=2/n, anchor='center')
                self.maze_grid[-1][-1].cell_state = None               # initialising state attributes
                self.set_cell_state(self.maze_grid[-1][-1], "empty")
                self.maze_grid[-1][-1].config(command = lambda cell=self.maze_grid[-1][-1] : self.set_cell_state(cell, self.state_set_to))


    def set_cell_state(self, cell, state="empty"):        
        if  cell.cell_state == "start": self.start_cell = None
        elif cell.cell_state == "goal": self.goal_cell  = None
        cell.cell_state = state
        cell.config(text = '')
        cell["bg"] = self.state_colour[state]
        
        # while assigning 'start' and 'goal' cells
        # set the previously defined cell (if any) to empty
        if state == "start":
            if self.start_cell: self.set_cell_state(self.start_cell, "empty")
            self.start_cell = cell
            self.start_cell.config(text="S")

        elif state == "goal":
            if self.goal_cell: self.set_cell_state(self.goal_cell, "empty")
            self.goal_cell = cell
            self.goal_cell.config(text="G")


    def get_maze_grid(self):
        print("Getting cells")
        maze = ""
        for x in range(self.maze_size):
            for y in range(self.maze_size):
                if self.maze_grid[x][y].cell_state == "wall": maze += "*"
                else: maze += " "
                if self.maze_grid[x][y].cell_state == "start": start = (x, y)
                elif self.maze_grid[x][y].cell_state == "goal":  goal  = (x, y)
            maze += "\n"
        result = [[char for char in line] for line in maze.split('\n')]
        return result, start, goal


    def warning(self, type_=0):
        if type_ == 0: text = "PLEASE SET\nA START AND\nAN END POINT"
        if type_ == 1: text = "NO PATH WAS FOUND"
        warning_lbl = Label(self.win, text=text, width=20, fg='red', font=(None, 30), relief=SOLID)
        warning_lbl.place(relx=0.45, rely=0.55, anchor='center')
        self.win.after(2800, warning_lbl.destroy)


    def solve_maze(self):
        # invalid maze setting
        if not (self.start_cell and self.goal_cell):
            self.warning()
            return

        # solving maze
        print("Solving Maze")
        self.visited_cells.clear()
        maze, start, end = self.get_maze_grid()
        solution_path    = self.solver(maze, start, end)
        #[print(''.join(line)) for line in maze]
        if solution_path:
            for x,y in itertools.product(range(self.maze_size), range(self.maze_size)):
                if self.maze_grid[x][y].cell_state == "empty":
                    if (x,y) in solution_path: self.maze_grid[x][y].config(bg = "#e5d273")
                    else:                      self.maze_grid[x][y].config(bg = "white")
        else: self.warning(1)


    def visualize_maze_solution(self):
        print("Displaying Working of Algorithm")
        self.visited_cells.clear()
        if not (self.start_cell and self.goal_cell):
            self.warning()
            return

        for name, btn in self.all_buttons.items():
            if name != "Visualize": btn.config(state = DISABLED)
            else: btn.config(text = "Stop")
        [btn.config(state = DISABLED) for btn in self.maze_area.winfo_children()]
        [self.win.unbind(cmd) for cmd in ['<Return>', '<space>', '<r>', '<t>'] ]

        maze,start,end = self.get_maze_grid()
        solution_path  = self.solver(maze, start, end)
        self.is_maze_solved = not self.is_maze_solved

        # visualising starts
        for x,y in itertools.product(range(self.maze_size), range(self.maze_size)):
            if self.maze_grid[x][y].cell_state == "empty":
                self.maze_grid[x][y].config(bg = "white")

        def call_back(cells=self.visited_cells[1:-1] if solution_path else self.visited_cells[1:]): # don't visit start and goal
            if cells == [] or not self.is_maze_solved:
                self.is_maze_solved = False
                # print("Visualization Done")
                for name, btn in self.all_buttons.items():
                    if name == "Visualize": btn.config(text = "Visualize")
                    else: btn.config(state = NORMAL)
                [btn.config(state = NORMAL) for btn in self.maze_area.winfo_children()]
                self.set_bindings()
                return
            x,y = cells.pop(0)
            self.maze_grid[x][y].config(bg = "#f2ecce")
            self.win.after(250, lambda: call_back(cells))
        call_back()


    def read_maze_from_file(self):
        files = [ file for file in os.listdir('./levels') if re.match("maze[A-Za-z0-9]*.txt", file.lower()) ]
        file_ = random.choice(files)
        with open(f"./levels/{file_}", 'r') as file:
            return [''.join(line) for line in file.read().lower().split('\n')]


    def sample_maze(self):
        char_mapping = {'s':"start", '*':"wall", ' ':"empty", 'g':"goal"}
        maze_text = self.read_maze_from_file()
        self.maze_scale.set( len(maze_text) )
        self.update_maze_tiles()
        # print(len(maze_text), len(maze_text[0]))
        for x,y in itertools.product(range(self.maze_size), range(self.maze_size)):
            self.set_cell_state(self.maze_grid[x][y], char_mapping[maze_text[x][y]])


    def valid_cell(self, puzzle, pos):
        rows = columns = self.maze_size
        return (0 <= pos[0] < rows) and (0 <= pos[1] < columns) and (puzzle[pos[0]][pos[1]] != '*')


    def get_path(self, predecessors, start, goal):
        current = goal
        path    = []
        while current != start:
            path.append(current)
            current = predecessors[current]
        path.append(start)
        path.reverse()
        return path


    def DFS(self, puzzle, start, goal):
        print("DFS")
        stack = [start]
        predecessors = {start: None}
        while stack:
            current = stack.pop()
            self.visited_cells.append(current)
            if current == goal:
                return self.get_path(predecessors, start, goal)
            for direction in random.sample(["up", "left", "down", "right"], 4):
                r_offset, c_offset = self.offsets[direction]
                neighbour = (current[0] + r_offset, current[1] + c_offset)
                if self.valid_cell(puzzle, neighbour) and neighbour not in predecessors:
                    stack.append(neighbour)
                    predecessors[neighbour] = current
        return None


    def BFS(self, puzzle, start, goal):
        print("BFS")
        queue = [start]
        predecessors = {start: None}
        while queue:
            current = queue.pop(0)
            self.visited_cells.append(current)
            if current == goal:
                return self.get_path(predecessors, start, goal)
            for direction in random.sample(["up", "left", "down", "right"], 4):
                r_offset, c_offset = self.offsets[direction]
                neighbour = (current[0] + r_offset, current[1] + c_offset)
                if self.valid_cell(puzzle, neighbour) and neighbour not in predecessors:
                    queue.append(neighbour)
                    predecessors[neighbour] = current
        return None


    def A_star(self, puzzle, start, goal):
        print("A*")
        def heuristic(a, b):
            x1, y1 = a
            x2, y2 = b
            return abs(x1-x2) + abs(y1-y2)
        pq = PriorityQueue()
        pq.put(start, 0)
        predecessors = {start: None}
        g_values = {start: 0}

        while not pq.is_empty():
            current = pq.get()
            self.visited_cells.append(current)
            if current == goal:
                return self.get_path(predecessors, start, goal)
            for direction in ["up", "left", "down", "right"]:
                r_offset, c_offset = self.offsets[direction]
                neighbour = (current[0] + r_offset, current[1] + c_offset)
                if self.valid_cell(puzzle, neighbour) and neighbour not in g_values:
                    new_cost = g_values[current] + 1
                    g_values[neighbour] = new_cost
                    f_value = new_cost + heuristic(goal, neighbour)
                    pq.put(neighbour, f_value)
                    predecessors[neighbour] = current
        return None


if __name__ == "__main__":
    win = Tk()
    app = MazeSolver(win)
    win.mainloop()
    exit()

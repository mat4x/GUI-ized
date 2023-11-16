'''
This is another work in my collection of
converting normal programs into GUI applications
using Python's tkinter module.

The solver algorithm uses brute force approach
to find all possible valid entries in a cell.
If the input puzzle given is solvable
the solution will be displayed at the bottom,
else a warning will be flashed on screen.

The program opens with a 'SAMPLE' puzzle.
Click the 'RESET' button to enter fresh values.

- Completed on 08/05/2022
'''


from tkinter import Tk, Button, Label, Entry, Frame, SOLID, FLAT, END, CENTER
import numpy
import random
import os, re


class SudokuSolver():
	def __init__(self, win):
		
		# window setup
		self.win = win
		self.win.title("Sudoku Solver - Mayur Sharma")
		self.DIMS = (400, 600)
		BACKGROUND = '#fff2ff'
		self.win.geometry(f'{self.DIMS[0]}x{self.DIMS[1]}+400+50')
		self.win.minsize(self.DIMS[0], self.DIMS[1])
		self.win.config(bg=BACKGROUND)
		
		# key bindings
		self.win.bind('<Return>', lambda e: self.solve_puzzle() )
		self.win.bind('<space>',  lambda e: self.solve_puzzle() )
		self.win.bind('<Double-Escape>', lambda e: self.win.quit() )
		self.win.bind('<r>', lambda e: self.reset_puzzle() )
		self.win.bind('<s>', lambda e: self.set_sample_puzzle() )

		# exit button and title
		Button(self.win, text='X', bg='#ff8095', fg='white', font=(None, 10, 'bold'),
			width=3, command=self.win.quit).place(relx=0.99, rely=0.01, anchor='ne')
		Label(self.win, text="Sudoku Solver", fg='#790038', font=("8514oem", 35, 'bold'),
			bg=BACKGROUND ).place(relx=0.5, y=10, anchor='n')

		# input validation
		callback = lambda inp: True if (inp.isdigit() and 0<int(inp)<10) or inp == "" else False
		reg = self.win.register(callback)

		# input boxes
		brdr_clr = '#330011'
		self.input_frame = Frame(self.win, background='#ba1337')
		length = 0.8*self.DIMS[0]
		self.input_frame.place(relx=0.5, rely=0.1, anchor='n', width=length, height=length)

		self.inps = []
		for y in range(1, 18, 2):
			for x in range(1, 18, 2):
				self.inps.append( Entry(self.input_frame, fg='#330011', bg='#fff0f5', justify=CENTER, font=(None, 20), relief=FLAT, insertofftime=3000,) )
				self.inps[-1].place(relx=x/18, rely=y/18, relwidth=0.09, relheight=0.09, anchor='center')
				self.inps[-1].config(validate="key", validatecommand=(reg, '%P'))
		
		# boders
		Frame(self.input_frame, background=brdr_clr).place(relx=0.333, rely=0.5, relheight=1, width=4, anchor='center')
		Frame(self.input_frame, background=brdr_clr).place(relx=0.667, rely=0.5, relheight=1, width=4, anchor='center')
		Frame(self.input_frame, background=brdr_clr).place(relx=0.5, rely=0.333, relwidth=1, height=4, anchor='center')
		Frame(self.input_frame, background=brdr_clr).place(relx=0.5, rely=0.667, relwidth=1, height=4, anchor='center')

		# buttons RESET, SOLVE, SAMPLE
		Button(self.win, text='SOLVE (\u21B5)', width=8, relief=SOLID, command=self.solve_puzzle).place(relx=0.2, rely=0.72, anchor='center')
		Button(self.win, text='RESET', width=8, relief=SOLID, command=self.reset_puzzle).place(relx=0.2, rely=0.80, anchor='center')
		Button(self.win, text='SAMPLE',width=8, relief=SOLID,command=self.set_sample_puzzle).place(relx=0.2, rely=0.88, anchor='center')

		# solution area
		self.solution_frame = Frame(self.win, background='#ffb453')
		length = 0.5*self.DIMS[0]
		self.solution_frame.place(relx=0.65, rely=0.65, anchor='n', width=length, height=length)

		self.sol_tiles = []
		for y in range(1, 18, 2):
			for x in range(1, 18, 2):
				self.sol_tiles.append( Label(self.solution_frame, fg='#553300', background='#fff265', justify=CENTER, font=(None, 10, 'bold')) )
				self.sol_tiles[-1].place(relx=x/18, rely=y/18, relwidth=0.09, relheight=0.09, anchor='center')
		brdr_clr = '#996600'
		Frame(self.solution_frame, background=brdr_clr).place(relx=0.333, rely=0.5, relheight=1, width=4, anchor='center')
		Frame(self.solution_frame, background=brdr_clr).place(relx=0.667, rely=0.5, relheight=1, width=4, anchor='center')
		Frame(self.solution_frame, background=brdr_clr).place(relx=0.5, rely=0.333, relwidth=1, height=4, anchor='center')
		Frame(self.solution_frame, background=brdr_clr).place(relx=0.5, rely=0.667, relwidth=1, height=4, anchor='center')
		
		self.load_samples()
		self.set_sample_puzzle()
		#self.solve_puzzle() # testing

	
	# brute force
	def solve_sudoku(self, puzzle):
		for row in range(9):
			for column in range(9):
				if puzzle[row][column] == 0:
					# determining block
					x = (row//3)*3
					y = (column//3)*3    
					for value in range(1,10):
						if ( value not in puzzle[row] and
							 value not in [ puzzle[r][column] for r in range(9) ] and
							 value not in [ puzzle[i][j] for i in range(x,x+3) for j in range(y,y+3) ]):

							puzzle[row][column] = value

							if self.solve_sudoku(puzzle): return puzzle
							else: puzzle[row][column] = 0
					else: return False
		return puzzle


	def load_samples(self):
		self.puzzles = []
		files = [ file for file in os.listdir('./levels') if re.match("puzzle [0-9]+.txt", file.lower()) ]
		for file_name in files:
			with open(f"./levels/{file_name}", 'r') as file:
				self.puzzles.append( [list(map(int, line.split())) for line in file.read().strip().split('\n')] )


	def set_sample_puzzle(self):
		self.reset_puzzle()
	
		puzzle = random.choice(self.puzzles)
		idx = 0
		for row in puzzle:
			for value in row:
				if value !=0:
					self.inps[idx].insert(END, value)
				idx += 1


	def solve_puzzle(self, e=None):
		# print("Solving Puzzle!")
		puzzle = numpy.zeros([9,9], dtype = numpy.int8)
		idx = 0
		for row in range(9):
			for column in range(9):
				entry = self.inps[idx].get()
				puzzle[row][column] = int(entry) if entry.isdigit() else 0
				idx+=1

		solution = self.solve_sudoku(puzzle.tolist())

		if solution:
			self.display_solution(solution)
		else:
			# print("Solution not found")
			warning = Label(self.win, text="NO SOLUTION\nWAS FOUND",width=15, fg='red', font=(None, 30), relief=SOLID)
			warning.place(relx=0.5, rely=0.5, anchor='center')
			self.win.after(3500, warning.destroy)


	def reset_puzzle(self):
		# print("Resetting Puzzle!")
		idx = 0
		for row in range(9):
			for value in range(9):
				self.inps[idx].delete(0, END)
				self.sol_tiles[idx].config(text = '')
				idx += 1


	def display_solution(self, solution):
		idx = 0
		for row in range(9):
			for column in range(9):
				value = solution[row][column]
				self.sol_tiles[idx].config(text = value if value else '')
				idx += 1


if __name__ == "__main__":
	win = Tk()
	app = SudokuSolver(win)
	win.mainloop()
	exit()

'''
Source: https://github.com/mat4x/GUI-ized

This program is one of my work in the collection of
converting normal programs into GUI applications
using Python's tkinter module.

The program requirements were:
1. take a number input 'n' from the user.
2. return the 'nth' number in the fibonacci series

Additions:
	- multiple algorithm for calculation and their respective flaws
	- shortcut keys mapping for quick use
	- invalid input error handling

Note: this program required an external library 'pyperclip'

- Completed on 26/01/2022
'''


from tkinter import Tk, Label, Button, Entry, CENTER, X, LEFT, E, SOLID
from pyperclip import copy


# RecursionError: max depth exceeded & takes up memory
'''def fibonacci(n, memo={0:0,1:1}):
	if n<0: return int(((-1)**(n+1))*fibonacci(abs(n)))
	if n in memo: return memo[n]
	memo[n] = fibonacci(n-2) + fibonacci(n-1)
	return memo[n]'''


# takes up too much memory to store list
'''def fibonacci(n):
	if n==0: return 0
	if n<0: return int(((-1)**(n+1))*fibonacci(abs(n)))
	lst=[0,1]
	for i in range(n-1):
		lst.append(lst[-1]+lst[-2])
	return lst[-1]'''


# no memoization, slow if function called again
def fibonacci(n:int) -> int:
	if n == 0: return 0
	if n < 0 : return int(((-1)**(n+1))*fibonacci(abs(n))) # generalizing for negative indices

	v1, v2 = 0, 1
	for i in range(n):
		v1     = v2 + v1
		v1, v2 = v2, v1
	return v1


class EmptyInputError(Exception): pass


class App:
	def __init__(self, win):
		info = 'In mathematics, the Fibonacci numbers, commonly denoted Fₙ, \
form a sequence, called the Fibonacci sequence, such that each \
number is the sum of the two preceding ones, starting from 0 and 1, for n≥1.'

		# window setup
		self.win = win
		self.win.geometry("300x500+500+100")
		self.win.title("Fibonacci Calculator - Mayur Sharma")

		# calculator elements
		Button(self.win,text="  X  ", bg="#aaa", command=self.win.destroy, relief=SOLID, borderwidth=0).pack(anchor=E)
		Label(self.win, text="Nth Fibonacci Number Calculator", font=(None,15)).pack(fill=X, pady=15)
		self.entry = Entry(self.win, font=(None,15), justify=CENTER); self.entry.pack(fill=X)
		self.entry.focus_set()

		Button(win, text="Calculate", font=(None,15), command=self.get_ans).pack(fill=X,pady=10)
		self.lbl_ans = Label(self.win, font=(None,15), bg="#ccc", wraplength=280)
		self.lbl_ans.pack(fill=X, pady=10)
		Button(win,text="Copy Value", font=(None,10), command=lambda: copy(self.ans["text"])).pack(anchor=E, padx=20)
		Label(win, text=info, font=(None,10), wraplength=280, justify=LEFT).pack(fill=X, pady=10)

		# accessibilty/shortcuts
		win.bind('<Return>', self.get_ans)
		win.bind('<Double-Escape>', lambda e: win.destroy())


	def get_ans(self, event=None):
		inp_val = self.entry.get().strip()
		try:
			if inp_val.strip() == '':
				raise EmptyInputError
			ans = fibonacci(int(inp_val))
			
		# error handling
		except RecursionError:  ans = "Going way over board here\n*can still be calculated by switch the function"
		except EmptyInputError: ans = ""; print("You want to get no fib value?")
		except:                 ans = "Invalid input:\nLearn Mathematics\nnumbers are 1, 2, 3, 4..."    # humor

		# display result
		finally:
			self.lbl_ans.config(text = str(ans))
			l = len(str(ans))
			self.lbl_ans.configure(font=(None, 15 if l<230 else
											   8 if l<554  else
											   6 if l<3135 else 4))     # font size depends on answer length


if __name__ == '__main__':
	win = Tk()
	app = App(win)
	win.mainloop()
	exit()

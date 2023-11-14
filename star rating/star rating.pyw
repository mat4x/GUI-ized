'''
Source: https://github.com/mat4x/GUI-ized

This program is one of my work in the collection of
converting normal programs into GUI applications
using Python's tkinter module.

The program requirements are:
1. a 5 star rating class to be palced in a container widget taken as an input parameter

- Completed on 14/05/2022
'''

from tkinter import Tk, Frame, Label, Button, SOLID, X, Y, BOTH


class StarRating:
	def __init__(self, frame, BG_color="white", bind_keys=False):
		self.rating = 0
		self.star_buttons = []

		# set star buttons
		for i in range(1, 6):
			self.star_buttons.append( Button(frame, text='☆', bg=BG_color, fg="#bf8c00",
											 font=(None,20), relief=SOLID, bd=0,
											 activebackground=BG_color,
											 activeforeground="yellow",
											 command = lambda x=i: self.set_rating(x)) )
			self.star_buttons[-1].place(relx=i/6, rely=0.5, anchor='center')

			if bind_keys: win.bind( str(i), lambda e, x=i: self.set_rating(x) )

		self.rating_text = Label(text = '<>', bg=BG_color, fg="#633500")
		self.rating_text.place(relx=0.5, rely=0.8, anchor='center')


	def set_rating(self, n):
		self.rating = n
		mapping = {1:"Terrible", 2:"Unsatisfactory", 3:"Average", 4:"Good", 5:"Excellent"}
		for btn in self.star_buttons[:n]:
			btn.config(text = "★", fg="orange")
		for btn in self.star_buttons[n:]:
			btn.config(text = "☆", fg="#bf8c00")
		self.rating_text.config(text=mapping[n])


if __name__ == "__main__":
	win = Tk()
	win.title("Star Rating - Mayur Sharma")
	win.geometry("500x300")
	frame = Frame(win, bg='lightyellow', width=100, height=10)
	frame.pack(expand=True, fill=BOTH)
	StarRating(frame, "lightyellow", bind_keys=True)
	win.mainloop()

'''
Source: https://github.com/mat4x/GUI-ized

This program is one of my work in the collection of
converting normal programs into GUI applications
using Python's tkinter module.

It was a project related to a Python GUI course
on LinkedIn Learning that I tried to recreate
on my own, with additional features.

The program requirements were:
1. It will display a logo and instructions to user.
2. It will have user input fields for:
	Name
	Email address
	Multiline comments
3. It will have two buttons: Submit and Clear.
3. Pressing Submit will:
	Print contents of input fields to the console
	Empty content of input field
	Notify the user that comments were submitted
4. Pressing Clear will:
	Empty the input fields

Additions:
	- animated element in the UI
	- entry validation and message popup on invalid entries
	- storing entries in a csv file

Note: this program has 3 external data elements:
	- tour_logo.gif
	- ocean_waves.gif
	- California feedback.csv (auto generated)

- Completed on 13/05/2022
'''

from tkinter import (Tk, Frame, Button, Label, Entry, Text,
					SOLID, END, PhotoImage, messagebox,
					X, Y, LEFT, BOTTOM, BOTH, TOP)
from PIL import Image
import re


class FeedbackForm:
	def __init__(self, win):
		
		# window setup
		DIMS = (350, 520)
		BG_COLOR = "#e3dcbc"
		self.win = win
		self.win.configure(bg=BG_COLOR)
		self.win.title("California Feedback - Mayur Sharma")
		self.win.geometry(f"{DIMS[0]}x{DIMS[1]}+500+100")
		self.win.resizable(False, False)
		self.win.bind('<Double-Escape>', lambda e: self.win.quit())
		# self.win.bind('<Return>', lambda e: self.submit_form())		# can not use this as <Enter> is required for multiline comments
		
		# form header
		frame_header = Frame(self.win, bg=BG_COLOR)
		frame_header.pack(fill=X, pady=(20,0), padx=5)

		self.logo = PhotoImage(file = "tour_logo.gif")
		Label(frame_header, image=self.logo, bg=BG_COLOR).grid(row=0,column=0, rowspan=2)
		Label(frame_header, bg=BG_COLOR, text="Thank you for exploring!", font=(None,15,'bold')).grid(row=0, column=1, sticky='nsew')
		Label(frame_header, bg=BG_COLOR, text="We're glad you chose Explore California for your recent adventure. \
Please tell us what you thought about the 'Desert to Sea' tour.", wraplength=250, justify="left").grid(row=1, column=1, padx=[10,0])

		# form elements
		frame_form = Frame(self.win, bg=BG_COLOR)
		frame_form.pack(fill=BOTH, expand=False, pady=(20,20), padx=15)
		frame_form.columnconfigure([0,1], weight=1)

		Label(frame_form, text="Name :" , bg=BG_COLOR).grid(row=0, column=0, sticky='sw', pady=5)
		Label(frame_form, text="Email :", bg=BG_COLOR).grid(row=0, column=1, sticky='sw', pady=5)

		self.name_entry  = Entry(frame_form, width=23)
		self.name_entry.grid(row=1, column=0, pady=[0,15])
		self.email_entry = Entry(frame_form, width=23)
		self.email_entry.grid(row=1, column=1, pady=[0,15])

		Label(frame_form, text="Comments :", bg=BG_COLOR).grid(row=2, column=0, sticky='sw')
		self.comment_text = Text(frame_form, width=45, height=10, font=('Arial', 10))
		self.comment_text.grid(row=3, column=0, columnspan=2, pady=5)

		Button(frame_form, text="Submit", width=15, bd=0.5, command=self.submit_form).grid(row=4, column=0, pady=[5,0])
		Button(frame_form, text="Clear" , width=15, bd=0.5, command=self.clear_form ).grid(row=4, column=1, pady=[5,0])
	
		# wave ui animation
		waves_label = Label(self.win, bg=BG_COLOR)
		waves_label.pack(fill=Y, anchor='n')
		self.ocean_animation(waves_label)

		# output file creation
		try:
			with open("feedbacks.csv", 'r'):
				print("File exists")
		except FileNotFoundError:
			with open("feedbacks.csv", 'w') as file:
				file.write("sep=|\n")


	def ocean_animation(self, label):
		frames = tuple(PhotoImage(file="ocean_waves.gif",
					format = 'gif -index %i' %(i)).zoom(2).subsample(5)
					for i in range(8))	# 8 frames of animation

		def update(idx=0):
			frame = frames[idx]
			idx = (idx+1)%8
			label.configure(image = frame)
			self.win.after(1800, update, idx)
		update()


	def clear_form(self):
		self.name_entry  .delete('0', END)
		self.email_entry .delete('0', END)
		self.comment_text.delete('1.0', END)


	def validate_inputs(self, name, email, comment):
		return ( comment and
				 re.fullmatch("[A-Z ]+", name.upper()) and
				 re.fullmatch(r"[\w._%+-]+@[\w]+\.[A-Za-z]{2,}", email) )


	def submit_form(self):
		name  	= self.name_entry.get()
		email 	= self.email_entry.get()
		comment = self.comment_text.get("1.0", END).strip().replace('\n', ' ')

		# store data
		if self.validate_inputs(name, email, comment):
			with open("feedbacks.csv", 'a') as file:
				file.write( '| '.join( (name, email, comment) ) + '\n' )
			messagebox.showinfo(title="California Feedback", message="Your response\nhas been submitted!")
			self.clear_form()
			self.win.focus_force()
		
		# show warning
		else:
			warning = Label(self.win, font=(None, 20), fg="maroon", bd=1, relief=SOLID,
							text="Please fill all entries\nwith valid details." )
			warning.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8)
			win.after(3500, warning.destroy)


if __name__ == "__main__":
	win = Tk()
	FeedbackForm(win)
	win.mainloop()

import customtkinter as ctk
import tkinter

from dbm import *
from logic import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.geometry("1200x1200")

class Frame() :
	def __init__(self, window, color) :
		self.frame = ctk.CTkFrame(master=window)
		self.frame.grid_propagate(False)
		self.frame.configure(fg_color=str(color))


	def grid_frame(self, r, c) :
		for i in range(r) :
			self.frame.rowconfigure(i, weight=1)
		for i in range(c) :
			self.frame.columnconfigure(i, weight=1)



class Child_Frame(Frame) :
	def __init__(self, window, color, frame_width, frame_border_width, frame_border_color) :
		super().__init__(window, color)
		self.frame.configure(width=frame_width, border_width=frame_border_width, border_color=str(frame_border_color))

	def grid_frame(self, r, c) :
		super().grid_frame(r, c)




def home_page(current_frame=None) :
	if (current_frame != None) :
		current_frame.pack_forget()

	home_page = Frame(window, "#33658A")
	home_page.frame.place(x=0, y=0, relwidth=1, relheight=1)
	home_page.grid_frame(8, 4)


	home_page_card = Child_Frame(home_page.frame, "#DDDDDD", 500, 3, "black")
	home_page_card.frame.grid(row=1, column=1, rowspan=6, columnspan=2, sticky="ns")
	home_page_card.grid_frame(6,3)


	home_page_card_label = ctk.CTkLabel(home_page_card.frame, text="Choose between the \ntwo options")
	home_page_card_label.configure(font=("Helvetica", 30, "bold"), text_color="black")
	home_page_card_label.grid(row=1, column=1)

	login_button = ctk.CTkButton(home_page_card.frame, text="Login", command=lambda: login_page(home_page.frame))
	login_button.configure(width=250, height=80, font=("Helvetica", 20, "bold"), text_color="black", fg_color="#33658A", hover_color="#2E5D80")
	login_button.grid(row=2, column=1, rowspan=2, columnspan=1)

	register_button = ctk.CTkButton(home_page_card.frame, text="Sign Up", command=lambda: register_page(home_page.frame))
	register_button.configure(width=250, height=80, font=("Helvetica", 20, "bold"), text_color="black", fg_color="#33658A", hover_color="#2E5D80")
	register_button.grid(row=4, column=1, rowspan=2, columnspan=1, sticky="n")


def login_page(current_frame=None) :
	if (current_frame != None) :
		current_frame.pack_forget()

	login_page = Frame(window, "#33658A")
	login_page.frame.place(x=0, y=0, relwidth=1, relheight=1)
	login_page.grid_frame(8,4)

	login_page_card = Child_Frame(login_page.frame, "#DDDDDD", 500, 3, "black")
	login_page_card.frame.grid(row=1, column=1, rowspan=6, columnspan=2, sticky="ns")
	login_page_card.grid_frame(8,4)

	back_button = ctk.CTkButton(login_page_card.frame, text="Back", command=lambda: home_page(login_page.frame))
	back_button.configure(width=125, height=80, font=("Helvetica", 20, "bold"), text_color="black", fg_color="#33658A", hover_color="#2E5D80")
	back_button.grid(row=6, column=1, rowspan=2, columnspan=1, sticky="n")

	login_page_label = ctk.CTkLabel(login_page_card.frame, text="Enter your email \nand password")
	login_page_label.configure(font=("Helvetica", 30, "bold"), text_color="black")
	login_page_label.grid(row=1, column=1, columnspan=2)

	email_entry = ctk.CTkEntry(login_page_card.frame, placeholder_text="Email")
	email_entry.configure(width=250, height=80, font=("Helvetica", 20), fg_color="#DDDDDD", text_color="black", border_width=3, border_color="black")
	email_entry.grid(row=2, column=1, rowspan=2, columnspan=2)

	password_entry = ctk.CTkEntry(login_page_card.frame, placeholder_text="Password", show="*")
	password_entry.configure(width=250, height=80, font=("Helvetica", 20), text_color="black", fg_color="#DDDDDD", border_width=3, border_color="black")
	password_entry.grid(row=4, column=1, rowspan=2, columnspan=2, sticky="n")

	login_button = ctk.CTkButton(login_page_card.frame, text="Login", command=lambda: main_menu(login_page.frame))
	login_button.configure(width=125, height=80, font=("Helvetica", 20, "bold"), text_color="black", fg_color="#33658A", hover_color="#2E5D80")
	login_button.grid(row=6, column=2, rowspan=2, columnspan=1, sticky="n")


def register_page(current_frame=None) :
	if (current_frame != None) :
		current_frame.pack_forget()

	register_page = Frame(window, "#33658A")
	register_page.frame.place(x=0, y=0, relwidth=1, relheight=1)
	register_page.grid_frame(8,4)

	register_page_card = Child_Frame(register_page.frame, "#DDDDDD", 500, 3, "black")
	register_page_card.frame.grid(row=1, column=1, rowspan=6, columnspan=2, sticky="ns")
	register_page_card.grid_frame(10,4)

	back_button = ctk.CTkButton(register_page_card.frame, text="Back", command=lambda: home_page(register_page.frame))
	back_button.configure(width=125, height=80, font=("Helvetica", 20, "bold"), text_color="black", fg_color="#33658A", hover_color="#2E5D80")
	back_button.grid(row=8, column=1, rowspan=2, columnspan=1, sticky="n")

	register_page_label = ctk.CTkLabel(register_page_card.frame, text="Sign Up")
	register_page_label.configure(font=("Helvetica", 30, "bold"), text_color="black")
	register_page_label.grid(row=1, column=1, columnspan=2, sticky="s")

	username_entry = ctk.CTkEntry(register_page_card.frame, placeholder_text="Username")
	username_entry.configure(width=250, height=80, font=("Helvetica", 20), fg_color="#DDDDDD", text_color="black", border_width=3, border_color="black")
	username_entry.grid(row=2, column=1, rowspan=2, columnspan=2, sticky="s")

	email_entry = ctk.CTkEntry(register_page_card.frame, placeholder_text="Email")
	email_entry.configure(width=250, height=80, font=("Helvetica", 20), fg_color="#DDDDDD", text_color="black", border_width=3, border_color="black")
	email_entry.grid(row=4, column=1, rowspan=2, columnspan=2)

	password_entry = ctk.CTkEntry(register_page_card.frame, placeholder_text="Password", show="*")
	password_entry.configure(width=250, height=80, font=("Helvetica", 20), text_color="black", fg_color="#DDDDDD", border_width=3, border_color="black")
	password_entry.grid(row=6, column=1, rowspan=2, columnspan=2, sticky="n")

	register_button = ctk.CTkButton(register_page_card.frame, text="Register", command=lambda: main_menu(register_page.frame))
	register_button.configure(width=125, height=80, font=("Helvetica", 20, "bold"), text_color="black", fg_color="#33658A", hover_color="#2E5D80")
	register_button.grid(row=8, column=2, rowspan=2, columnspan=1, sticky="n")


def main_menu(current_frame=None, index=0):
    if current_frame is not None:
        current_frame.pack_forget()

    main_menu_page = Frame(window, "#33658A")
    main_menu_page.frame.place(x=0, y=0, relwidth=1, relheight=1)
    main_menu_page.grid_frame(8, 4)

    main_menu_card = Child_Frame(main_menu_page.frame, "#DDDDDD", 800, 3, "black")
    main_menu_card.frame.grid(row=1, column=1, rowspan=6, columnspan=2, sticky="ns")
    main_menu_card.grid_frame(16, 9)

    mm_card_container = Child_Frame(main_menu_card.frame, "#DDDDDD", 700, 0, "black")
    mm_card_container.frame.configure(height=400)
    mm_card_container.frame.grid(row=1, column=1, rowspan=14, columnspan=7, sticky="nsew")
    mm_card_container.grid_frame(6, 6)

    res = return_books().fetchall()
    query_length = len(return_books().fetchall())

    if index == 0 or index < 0:
        start_index = 0
    elif index >= query_length:
        start_index = index - 5
    else:
        start_index = index

    button_counter = 0


    for row in res[start_index:]:
        if button_counter < 5:
            book_button = ctk.CTkButton(mm_card_container.frame, text=(row[1] + " by " + row[2]), command=None)
            book_button.configure(font=("Helvetica", 20, "bold"), text_color="black", fg_color="#BFB7B6", hover_color="#B0A8A7", height=70, width=700)

            book_button.grid(row=button_counter, column=0, rowspan=1, columnspan=6)

            button_counter += 1



    previous_button = ctk.CTkButton(mm_card_container.frame, text="Previous", command=lambda: main_menu(main_menu_page.frame, start_index - 5))
    previous_button.configure(font=("Helvetica", 20, "bold"), text_color="black", fg_color="#33658A", hover_color="#2E5D80", height=70, width=300)
    previous_button.grid(row=button_counter, column=0, columnspan=3)

    next_button = ctk.CTkButton(mm_card_container.frame, text="Next", command=lambda: main_menu(main_menu_page.frame, start_index + 5))
    next_button.configure(font=("Helvetica", 20, "bold"), text_color="black", fg_color="#33658A", hover_color="#2E5D80", height=70, width=300)
    next_button.grid(row=button_counter, column=3, columnspan=3)



def reading_window(current_frame=None) :
	if (current_frame != None) :
		current_frame.pack_forget()

	reading_window = Frame(window, "#33658A")
	reading_window.frame.place(x=0, y=0, relwidth=1, relheight=1)
	reading_window.grid_frame(12,12)

	text_box_left = ctk.CTkTextbox(reading_window.frame, corner_radius=3, fg_color="#DDDDDD", text_color="black", border_width=3, border_color="black")
	text_box_left.grid(row=1, column=1, columnspan=5, rowspan=8, sticky="nsew")
	text_box_left.insert("0.0", read_book("./books/moby_dick.pdf").left_page)

	text_box_right = ctk.CTkTextbox(reading_window.frame, corner_radius=3, fg_color="#DDDDDD", text_color="black", border_width=3, border_color="black")
	text_box_right.grid(row=1, column=6, columnspan=5, rowspan=8, sticky="nsew")
	text_box_right.insert("0.0", read_book("./books/moby_dick.pdf").right_page)

	previous_button = ctk.CTkButton(reading_window.frame, text="Previous", command=None)
	previous_button.configure(font=("Helvetica", 20, "bold"), text_color="black", fg_color="#DDDDDD", hover_color="#BAB8B8", height=70, width=300, border_color="black", border_width=3)
	previous_button.grid(row=10, column=3, columnspan=3)

	next_button = ctk.CTkButton(reading_window.frame, text="Next", command=None)
	next_button.configure(font=("Helvetica", 20, "bold"), text_color="black", fg_color="#DDDDDD", hover_color="#BAB8B8", height=70, width=300, border_color="black", border_width=3)
	next_button.grid(row=10, column=6, columnspan=3)


#Test
reading_window()
window.mainloop()
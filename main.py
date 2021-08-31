import json
import tkinter as tk
from tkcalendar import Calendar

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    # def create_widgets(self):
    #     self.hi_there = tk.Button(self)
    #     self.hi_there["text"] = "Hello World\n(click me)"
    #     self.hi_there["command"] = self.say_hi
    #     self.hi_there.pack(side="top")
    #
    #     self.quit = tk.Button(self, text="QUIT", fg="red",
    #                           command=self.master.destroy)
    #     self.quit.pack(side="bottom")
    #
    # def say_hi(self):
    #     print("hi there, everyone!")

    def create_widgets(self):
        # unstored widget label setup
        tk.Label(self, text="File Name: ").grid(row=0, pady=10, padx=5)
        tk.Label(self, text="Title: ").grid(row=1, padx=5)
        tk.Label(self, text="Completed: ").grid(row=2, padx=5)
        tk.Label(self, text="Description: ").grid(row=3, padx=5)
        tk.Label(self, text="Tags: ").grid(row=4, padx=5)
        tk.Label(self, text="Weight: ").grid(row=5, padx=5)
        tk.Label(self, text="Prerequisites: ").grid(row=6, padx=5)
        tk.Label(self, text="Time Estimate: ").grid(row=7, padx=5)
        tk.Label(self, text="DueDate: ").grid(row=8, padx=5)

        # stored (via variable) widget
        file_name = tk.Entry(self)
        title = tk.Entry(self)
        completed = tk.Entry(self)
        description = tk.Text(self, height=10, width=20)
        tags = tk.Entry(self)
        weight = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL)
        prerequisites = tk.Entry(self)
        time_estimate = tk.Entry(self)
        due_date = Calendar(self, selectmode='day', year=2021, month=8, day=30)

        # layout
        file_name.grid(row=0, column=1, pady=10, padx=5)
        title.grid(row=1, column=1, padx=5)
        completed.grid(row=2, column=1, padx=5)
        description.grid(row=3, column=1, padx=5)
        tags.grid(row=4, column=1, padx=5)
        weight.grid(row=5, column=1, padx=5)
        prerequisites.grid(row=6, column=1, padx=5)
        time_estimate.grid(row=7, column=1, padx=5)
        due_date.grid(row=8, column=1, padx=5)

        # action buttons
        add_button = tk.Button(self, text="Add")
        submit_button = tk.Button(self, text="Submit")
        preview_button = tk.Button(self, text="Preview")
        clear_button = tk.Button(self, text="Clear")

        # add to layout
        add_button.grid(row=9, column=0, padx=5, pady=5)
        preview_button.grid(row=9, column=1, padx=5, pady=5)
        submit_button.grid(row=10, column=0, padx=5, pady=5)
        clear_button.grid(row=10, column=1, padx=5, pady=5)


root = tk.Tk()
root.title("NoteJsonifier")
app = Application(master=root)
app.mainloop()

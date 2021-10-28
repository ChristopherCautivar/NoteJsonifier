import json
import tkinter as tk
from tkcalendar import Calendar
from trie import Trie


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        # stored (via variable) widget
        self.file_name = tk.Entry(self)
        self.title = tk.Entry(self)
        self.completed = tk.Entry(self)
        # setup description functionality
        self.description = tk.Text(self, height=10, width=20)
        # bind event handler to widget
        self.description.bind("<Tab>", self.tab_next_widget)
        # change font
        self.description.configure(font=tk.font.Font(family="Helvetica", size=8))
        self.tags = tk.Entry(self)
        self.weight = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, takefocus=1)
        self.prerequisites = tk.Entry(self)
        self.time_estimate = tk.Entry(self)
        self.due_date = tk.Button(self, text="Add Due Date", command=lambda: self.replace_calendar())
        self.due_date.bind("<Return>", lambda x: self.replace_calendar())
        self.calendar = Calendar(self, selectmode="day", date_patter="m/d/y")
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

    def tab_next_widget(self, event):
        # intercepts the tab key press to always go to the next widget
        event.widget.tk_focusNext().focus()
        return "break"

    def replace_calendar(self):
        # a very specific function that replaces the button to add a due date with a calendar widget
        gi = self.due_date.grid_info()
        self.due_date.grid_remove()
        self.calendar.grid(row=gi["row"], column=gi["column"], padx=gi["padx"])

    def submit(self):
        # writes to the file name provided
        # if it doesn't exist, create then do append functionality
        # if it exists, append.
        file = open("data/" + self.file_name.get() + ".txt", "a")
        s = "{title:"
        s += ",completed:"
        s += ",description:"
        s += ",tags:"
        s += ",weight:"
        s += ",prerequisites:"
        s += ",time_estimate:"
        s += ",due_date:}"
        file.write(s)

    def clear(self):
        # clears all fields and resets calendar widget
        self.title.delete(0, tk.END)
        self.completed.delete(0, tk.END)
        self.description.delete(1.0, tk.END)
        self.tags.delete(0, tk.END)
        self.weight.set(0)
        self.prerequisites.delete(0, tk.END)
        self.time_estimate.delete(0, tk.END)
        self.calendar.grid_remove()
        self.due_date.grid(row=8, column=1, padx=5)
        pass

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

        # layout
        self.file_name.grid(row=0, column=1, pady=10, padx=5)
        self.title.grid(row=1, column=1, padx=5)
        self.completed.grid(row=2, column=1, padx=5)
        self.description.grid(row=3, column=1, padx=5)
        self.tags.grid(row=4, column=1, padx=5)
        self.weight.grid(row=5, column=1, padx=5)
        self.prerequisites.grid(row=6, column=1, padx=5)
        self.time_estimate.grid(row=7, column=1, padx=5)
        self.due_date.grid(row=8, column=1, padx=5)

        # button layouts
        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.bind("<Return>", lambda: self.submit())
        clear_button = tk.Button(self, text="Clear", command=self.clear)
        clear_button.bind("<Return>", lambda x: self.clear())
        submit_button.grid(row=9, column=0, padx=5, pady=5)
        clear_button.grid(row=9, column=1, padx=5, pady=5)


t = Trie(["test", "asdf"])
res = []
t.traverse()
print(res)
root = tk.Tk()
root.title("NoteJsonifier")
app = Application(master=root)
app.mainloop()

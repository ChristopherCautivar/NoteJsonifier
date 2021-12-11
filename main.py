import json
import tkinter as tk
from tkcalendar import Calendar
from trie import Trie
from datetime import datetime


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        # load internal suggestion trie
        open("data/tags.json", "a+").close()
        with open("data/tags.json", "r+") as json_file:
            if json_file.read(1):
                json_file.seek(0)
                self.trie = Trie(json.load(json_file)["tags"])
            else:
                json_file.seek(0)
                json.dump({"tags": []}, json_file)
                self.trie = Trie([])
        # self.trie = Trie(["a", "ab", "abb", "abc", "ac", "ba", "bag", "cat", "batter", "bat"])
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
        self.tags = tk.ttk.Combobox(self, values=self.trie.find_words())
        self.current_tags = set()
        self.tags.bind("<KeyRelease>", lambda x: self.auto_suggest(x))
        self.tags.bind("<KeyPress>", lambda x: self.validate_tag(x))
        self.weight = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, takefocus=1)
        self.prerequisites = tk.Entry(self)
        self.time_estimate = tk.Entry(self)
        self.due_date = tk.Button(self, text="Add Due Date", command=lambda: self.replace_calendar())
        self.due_date.bind("<Return>", lambda x: self.replace_calendar())
        self.calendar = Calendar(self, selectmode="day", date_patter="m/d/y")
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.cleanup)

    def auto_suggest(self, x):
        print(x)
        # get all characters in combobox
        input = self.tags.get()
        input = input.lower().strip()
        if x.char == "\r":
            # finalize tag, clearing the field, storing the input, and updating the trie
            self.tags.selection_clear()
            self.tags.delete(0, tk.END)
            self.current_tags.add(input)
            self.trie.add_word(input)
            return
        # only run for character keys
        if not x.char or not x.char.isalpha():
            return
        # get current cursor position
        pos = self.tags.index(tk.INSERT)
        # search trie based on current characters
        matches = self.trie.find_suggestions(input)
        if matches:
            # clear all of input
            self.tags.delete(0, tk.END)
            # autofill the first one
            self.tags.set(matches[0])
            # skip ahead to typed characters and highlight the suggested ones to be overwritten
            self.tags.selection_range(pos, tk.END)
            self.tags.icursor(pos)
        # populate the combobox with all of the results
        self.tags["values"] = matches

    def validate_tag(self, x):
        # intercept any non alpha input that is not backspace
        if not x.keysym == "BackSpace" and (not x.char or not x.char.isalpha()):
            return "break"

    # from tutorial on using tkinter
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
        # a+ mode forces append regardless of any seek() operations. b modes allow negative indexing, but
        # do not allow json dumps easily, complicating in-place insertion of new json objects within.
        # r+ throws errors when the file does not exist.
        # therefore, the most robust solution while avoiding try exception handling would be to "touch"
        # the proposed file with a+ mode, then proceed with r+ to read/prepare the data before overwriting it

        # "touch" json file
        open("data/" + self.file_name.get() + ".json", "a+").close()
        # open json file and check if empty
        with open("data/" + self.file_name.get() + ".json", "r+") as json_file:
            if json_file.read(1):
                # successfully read truthy character
                json_file.seek(0)
                data = json.load(json_file)
            else:
                # read falsey character, such as an empty file
                data = {"todos": []}
            data["todos"].append({
                "title": self.title.get(),
                "completed": self.completed.get(),
                "description": self.description.get(1.0, "end-1c"),
                "tags": list(self.current_tags),
                "weight": self.weight.get(),
                "prerequisites": self.prerequisites.get(),
                "time_estimate": self.time_estimate.get(),
                # TODO: handle for calendar not being visible and converting from datetime to readable and back
                "due_date": "unknown"
            })
            # seek to start, overwrite data
            json_file.seek(0)
            json.dump(data, json_file)
            # TODO: toast success
            # clear fields
            self.clear()

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
        self.current_tags.clear()

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
        submit_button.bind("<Return>", lambda x: self.submit())
        clear_button = tk.Button(self, text="Clear", command=self.clear)
        clear_button.bind("<Return>", lambda x: self.clear())
        submit_button.grid(row=9, column=0, padx=5, pady=5)
        clear_button.grid(row=9, column=1, padx=5, pady=5)

    def cleanup(self):
        if self.title.get():
            self.submit()
        with open("data/tags.json", "w") as json_file:
            json.dump({"tags": self.trie.find_words()}, json_file)
        self.master.destroy()


root = tk.Tk()
root.title("NoteJsonifier")
app = Application(master=root)
app.mainloop()

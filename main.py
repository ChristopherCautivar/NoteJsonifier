import json
import tkinter as tk
from tkcalendar import Calendar
from trie import Trie
from datetime import datetime


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
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
        self.t_completed = tk.IntVar()
        self.completed = tk.Checkbutton(self, variable=self.t_completed)
        self.completed.bind("<Return>", lambda x: self.completed.toggle())
        # setup description functionality
        self.description = tk.Text(self, height=10, width=20)
        # bind event handler to widget
        self.description.bind("<Tab>", self.tab_next_widget)
        # change font
        self.description.configure(font=tk.font.Font(family="Helvetica", size=8))
        self.tags = tk.ttk.Combobox(self, values=self.trie.find_words())
        self.current_tags = set()
        self.previous_tags = tk.Label(self, wraplength=125)
        self.tags.bind("<KeyRelease>", lambda x: self.auto_suggest(x))
        self.tags.bind("<KeyPress>", lambda x: self.validate_tag(x))
        self.weight = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, takefocus=1)
        self.t_prereq = tk.IntVar()
        self.prerequisites = tk.Checkbutton(self, variable=self.t_prereq)
        self.prerequisites.bind("<Return>", lambda x: self.prerequisites.toggle())
        self.t_frame = tk.Frame(self)
        self.hours = tk.Entry(self.t_frame, width=2, validate="all",
                              validatecommand=(self.register(self.validate_num), "%P"))
        self.minutes = tk.Entry(self.t_frame, width=2, validate="all",
                                validatecommand=(self.register(self.validate_num), "%P"))
        self.due_date = tk.Button(self, text="Add Due Date", command=self.replace_calendar)
        self.due_date.bind("<Return>", lambda x: self.replace_calendar())
        self.calendar = Calendar(self, date_pattern="mm/dd/y")
        self.cal_bool = False

        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.cleanup)

    def create_widgets(self):
        # unstored widget label setup
        tk.Label(self, text="File Name: ").grid(row=0, pady=10, padx=5)
        tk.Label(self, text="Title: ").grid(row=1, padx=5)
        tk.Label(self, text="Completed: ").grid(row=2, padx=5)
        tk.Label(self, text="Description: ").grid(row=3, padx=5)
        tk.Label(self, text="Tags: ").grid(row=4, padx=5, rowspan=2)
        tk.Label(self, text="Weight: ").grid(row=6, padx=5)
        tk.Label(self, text="Prerequisites: ").grid(row=7, padx=5)
        tk.Label(self, text="Time Estimate: ").grid(row=8, padx=5)
        tk.Label(self.t_frame, text="Hours: ").grid(row=1, column=0)
        tk.Label(self.t_frame, text="Minutes: ").grid(row=1, column=2)
        tk.Label(self, text="DueDate: ").grid(row=9, padx=5)

        # layout
        self.file_name.grid(row=0, column=1, pady=10, padx=5)
        self.title.grid(row=1, column=1, padx=5)
        self.completed.grid(row=2, column=1, padx=5)
        self.description.grid(row=3, column=1, padx=5)
        self.tags.grid(row=4, column=1, padx=5)
        self.previous_tags.grid(row=5, column=1, padx=5)
        self.weight.grid(row=6, column=1, padx=5)
        self.prerequisites.grid(row=7, column=1, padx=5)
        self.t_frame.grid(row=8, column=1)
        self.hours.grid(row=1, column=1)
        self.minutes.grid(row=1, column=3)
        self.due_date.grid(row=9, column=1, padx=5)
        self.calendar.grid(row=9, column=1, padx=5)
        self.calendar.grid_remove()

        # button layouts
        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.bind("<Return>", lambda x: self.submit())
        clear_button = tk.Button(self, text="Clear", command=self.clear)
        clear_button.bind("<Return>", lambda x: self.clear())
        submit_button.grid(row=10, column=0, padx=5, pady=5)
        clear_button.grid(row=10, column=1, padx=5, pady=5)

    def auto_suggest(self, x):
        # get all characters in combobox
        input = self.tags.get()
        input = input.lower().strip()
        if x.char == "\r":
            # finalize tag, clearing the field, storing the input, and updating the trie
            self.tags.selection_clear()
            self.tags.delete(0, tk.END)
            self.current_tags.add(input)
            self.trie.add_word(input)
            self.previous_tags["text"] = self.current_tags
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
        # intercept any non alpha input that is not backspace or tab
        if not x.keysym == "Tab" and not x.keysym == "BackSpace" and (not x.char or not x.char.isalpha()):
            return "break"

    def tab_next_widget(self, event):
        # intercepts the tab key press to always go to the next widget
        event.widget.tk_focusNext().focus()
        return "break"

    def replace_calendar(self):
        # a very specific function that replaces the button to add a due date with a calendar widget
        self.due_date.grid_remove()
        self.calendar.grid()
        self.cal_bool = True

    def validate_num(self, pval):
        if (str.isdigit(pval) or pval == "") and len(pval) <= 2:
            return True
        else:
            return False

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
                "date_created": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                "date_updated": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                "completed": True if self.t_completed.get() else False,
                "description": self.description.get(1.0, "end-1c"),
                "tags": list(self.current_tags),
                "weight": self.weight.get(),
                "prerequisites": True if self.t_prereq.get() else False,
                "time_estimate": {"hours": int(self.hours.get() if self.hours.get() else 0),
                                  "minutes": int(self.minutes.get() if self.hours.get() else 0)},
                # TODO: handle for calendar not being visible and converting from datetime to readable and back
                "due_date": self.calendar.selection_get().strftime("%m/%d/%Y") if self.cal_bool else ""
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
        self.completed.deselect()
        self.description.delete(1.0, tk.END)
        self.tags.delete(0, tk.END)
        self.weight.set(0)
        self.prerequisites.deselect()
        self.hours.delete(0, tk.END)
        self.minutes.delete(0, tk.END)
        self.calendar.grid_remove()
        self.due_date.grid()
        self.current_tags.clear()
        self.previous_tags["text"] = ""
        self.cal_bool = False

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

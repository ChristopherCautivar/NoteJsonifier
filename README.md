# NoteJsonifier
a simple python project that prompts input from a gui before creating a resulting text file containing the information 
as a json file.

## Features
* Prompts for notes with the same fields as the Todo object from SimpleTodoWebapp.

### Stretch Features
- [x] ~~Implementing IntVar() **StringVar()** for tags for cleaner data binding and use of the trace method to track user input updates.~~
  * I tried this approach in a branch that never made it past the first commit.
  * While it is possible to use StringVar() variables and trace to more reliably track changes to the value, special care would have to be taken when accounting for backspaces, and for any other code that writes to that StringVar(). I think the workarounds and code necessary for that approach would make the program more complicated and less clear, so I have opted to avoid this approach. 
- [x] Handle backspaces to control display values in trie for the remaining characters

## Timeline
Project should take in total 1 week maximum to reach MVP status using given python knowledge and experience.
### Stages:
* Planning
* Coding
* Debugging
* Fine Tuning
# --------------------------------------
# Imports & Global Variables
# --------------------------------------

import ttkbootstrap as ttk  
# This imports the `ttkbootstrap` package, which extends tkinter with modern themes and styles for GUI components.
# We are importing it as `ttk` to use it easily throughout the code.

from tkinter import messagebox, font, Text  
# We import `messagebox` to show pop-up alerts, `font` to customize text appearance, 
# and `Text` to create multi-line text areas from the tkinter library.

completed_tasks = set()  
# This creates an empty set to store completed tasks. 
# A set is like a list, but it only holds unique items, so no task is marked complete more than once.

highlighted_task = None  
# This variable will keep track of the currently highlighted task in the task list. 
# It starts with `None` because no task is highlighted at first.

# --------------------------------------
# Task Management Functions
# --------------------------------------

def add_task(event=None):  
    # This defines a function `add_task`, which is responsible for adding a task to the list.
    # The parameter `event=None` is optional and is used because this function is sometimes triggered by events like pressing Enter.

    task = task_entry.get().strip()  
    # Get the text entered in the `task_entry` widget (a text input field), and `strip()` removes extra spaces around the text.

    if task:  
        # If the task is not an empty string (the user entered something):

        task_display.configure(state='normal')  
        # Enable the `task_display` text area for editing (it was disabled to prevent direct edits).

        task_display.insert('end', f"{task}\n")  
        # Insert the new task at the end of the `task_display` widget, followed by a newline (`\n`).

        task_entry.delete(0, 'end')  
        # Clear the input field after adding the task.

        apply_task_style(task, completed=False)  
        # Call the `apply_task_style` function to style the newly added task (not completed, so it's styled as incomplete).

        task_display.configure(state='disabled')  
        # Disable the task display again to prevent manual editing of the tasks.

    else:
        messagebox.showwarning("Input Error", "Please enter a task.")  
        # If the task is empty, show a warning popup with the message "Please enter a task."

def complete_task():  
    # This defines the function to mark a task as completed.

    task_index = get_current_task_index()  
    # Get the index (line number) of the currently selected task using the `get_current_task_index` function.

    if task_index is not None:  
        # If a valid task is selected (i.e., `task_index` is not `None`):

        task = task_display.get(f"{task_index}.0", f"{task_index}.end").strip()  
        # Get the text of the selected task by using its index (from start to end of the line).
        # `strip()` removes any leading or trailing spaces.

        if task not in completed_tasks:  
            # If the task is not already marked as completed:

            completed_tasks.add(task)  
            # Add the task to the `completed_tasks` set.

            apply_task_style(task, completed=True)  
            # Apply completed styling to the task (e.g., strikethrough and green text).

    else:
        messagebox.showwarning("Selection Error", "Please select a task to complete.")  
        # If no valid task is selected, show a warning popup.

def remove_task():  
    # This function is responsible for removing a selected task from the list.

    task_index = get_current_task_index()  
    # Get the index (line number) of the currently selected task.

    if task_index is not None:  
        # If a valid task is selected:

        task_display.configure(state='normal')  
        # Enable the task display so that we can edit (delete) tasks.

        task_display.delete(f"{task_index}.0", f"{task_index}.end+1c")  
        # Delete the selected task. This removes the line at `task_index` and the newline character.

        task_display.configure(state='disabled')  
        # Disable the task display again after deleting.

    else:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")  
        # If no valid task is selected, show a warning popup.

def get_current_task_index():  
    # This function gets the index (line number) of the current task (where the cursor is placed).

    try:
        index = task_display.index('insert').split('.')[0]  
        # Get the position of the cursor (`insert`) in the `task_display` widget.
        # `split('.')[0]` takes the line number (before the dot) from the position (format is "line.column").

        return int(index)  
        # Convert the index from a string to an integer and return it.

    except:
        return None  
        # If there is an error (e.g., no task selected), return `None`.

def apply_task_style(task, completed):  
    # This function applies styling to a task. It takes two parameters: `task` (the task text) and `completed` (whether the task is done or not).

    task_display.tag_add(task, 'end-2l', 'end-1l')  
    # Add a tag to the task. The range `'end-2l'` to `'end-1l'` refers to the last line in the task display.
    # This is how we locate the new task for styling.

    task_display.tag_config(  
        task,  
        foreground='green' if completed else 'red',  
        # If the task is completed, style it with green text; otherwise, use red text.

        font=font.Font(size=18, weight='bold', overstrike=completed)  
        # Set the font size to 18, make it bold, and apply strikethrough (`overstrike`) if the task is completed.
    )

# --------------------------------------
# Task Highlighting Function
# --------------------------------------

def highlight_task(event):  
    # This function highlights a task when the user clicks on it. It is triggered by a mouse click event.

    global highlighted_task  
    # Use the global variable `highlighted_task` to track which task is currently highlighted.

    task_index = task_display.index(f"@{event.x},{event.y}").split('.')[0]  
    # Get the index of the task at the clicked position using the x and y coordinates of the mouse click (`event.x`, `event.y`).

    if highlighted_task is not None:  
        # If a task was previously highlighted:

        task_display.tag_remove('highlight', f"{highlighted_task}.0", f"{highlighted_task}.end")  
        # Remove the highlight from the previous task.

    highlighted_task = task_index  
    # Update the `highlighted_task` variable with the index of the newly clicked task.

    task_display.tag_add('highlight', f"{task_index}.0", f"{task_index}.end")  
    # Highlight the new task.

    task_display.tag_config('highlight', background='gray')  
    # Set the highlight style by changing the background to gray.

    task_display.configure(state='normal')  
    # Enable the task display so it can respond to the focus event.

    app.focus()  
    # Set the focus back to the main application window.

    task_display.configure(state='disabled')  
    # Disable the task display after highlighting to prevent manual edits.

# --------------------------------------
# GUI Setup
# --------------------------------------

app = ttk.Window(themename="darkly")  
# Create the main application window using the `ttkbootstrap` library. 
# `themename="darkly"` applies a dark theme to the app.

app.title("To-Do List Manager")  
# Set the title of the window to "To-Do List Manager".

app.geometry("600x500")  
# Set the size of the window to 600 pixels wide and 500 pixels tall.

app.configure(bg='#2E2E2E')  
# Set the background color of the window to a dark gray (hex code: #2E2E2E).

task_entry = ttk.Entry(app, font=('Helvetica', 15))  
# Create an entry widget (a text input field) where users can type new tasks.
# The font used is Helvetica with a size of 15.

task_entry.pack(pady=20)  
# Pack the entry widget into the window and add vertical padding of 20 pixels.

task_entry.bind('<Return>', add_task)  
# Bind the Enter (Return) key to trigger the `add_task` function. When the user presses Enter, the task is added.

ttk.Button(app, text="Add Task", command=add_task).pack(pady=10)  
# Create a button that says "Add Task". When clicked, it runs the `add_task` function to add the task to the list.

task_display = Text(  
    app, font=('Helvetica', 14), height=11, bg='#3C3C3C', fg='white', wrap='none', state='disabled'
)  
# Create a text widget to display tasks. It has a height of 11 lines, uses a Helvetica font size 14, has a dark gray background, 
# white text, and doesn't wrap long lines. It starts in a disabled state so the user can't edit tasks directly.

task_display.pack(pady=5)  
# Pack the task display into the window with 5 pixels of vertical padding.

task_display.bind('<Button-1>', highlight_task)  
# Bind the left mouse button (`<Button-1>`) to trigger the `highlight_task` function when a user clicks on a task.

action_frame = ttk.Frame(app)  
# Create a frame (a container) to hold action buttons like "Complete Task" and "Remove Task".

action_frame.pack(pady=5)  
# Pack the frame into the window with 5 pixels of vertical padding.

ttk.Button(  
    action_frame, text="Complete Task", command=complete_task, bootstyle="success", padding=(10, 5)
).pack(side='left', padx=5)  
# Create a button that says "Complete Task". When clicked, it runs the `complete_task` function. 
# It uses the "success" style and has padding. The button is packed to the left side with 5 pixels of horizontal padding.

ttk.Button(  
    action_frame, text="Remove Task", command=remove_task, bootstyle="danger", padding=(10, 5)
).pack(side='left', padx=5)  
# Create a button that says "Remove Task". When clicked, it runs the `remove_task` function.
# It uses the "danger" style (red button) and has padding. It's packed next to the "Complete Task" button.

ttk.Button(  
    app, text="Quit", command=app.quit, bootstyle="danger-outline", padding=(10, 5)
).pack(pady=10)  
# Create a button that says "Quit". When clicked, it closes the application (`app.quit`). 
# It uses an outlined danger style and has padding. It's packed below the other buttons.

app.mainloop()  
# This starts the main event loop of the application, which waits for user interaction (e.g., button clicks, key presses).

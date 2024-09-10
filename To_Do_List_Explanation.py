# --------------------------------------
# Imports & Global Variables
# --------------------------------------

import ttkbootstrap as ttk  # Import ttkbootstrap for modern themed widgets and styling
from tkinter import messagebox, font, Text  # Import necessary modules from tkinter for GUI

completed_tasks = set()  # Set to store completed tasks
highlighted_task = None  # Variable to track the currently highlighted task

# --------------------------------------
# Task Management Functions
# --------------------------------------

def add_task(event=None):  # Function to add a new task to the task display
    task = task_entry.get().strip()  # Get the text from the task entry field and remove leading/trailing whitespace
    if task:  # If task is not an empty string
        task_display.configure(state='normal')  # Enable the task display widget to allow text insertion
        task_display.insert('end', f"{task}\n")  # Insert the task at the end of the task display
        task_entry.delete(0, 'end')  # Clear the task entry field
        apply_task_style(task, completed=False)  # Apply styling to the newly added task (as not completed)
        task_display.configure(state='disabled')  # Disable the task display widget to prevent direct editing
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")  # Show a warning message if task is empty

def complete_task():  # Function to mark a task as complete
    task_index = get_current_task_index()  # Get the index of the currently selected task
    if task_index is not None:  # If a valid task is selected
        task = task_display.get(f"{task_index}.0", f"{task_index}.end").strip()  # Get the task text
        if task not in completed_tasks:  # If the task is not already marked as completed
            completed_tasks.add(task)  # Add the task to the set of completed tasks
            apply_task_style(task, completed=True)  # Apply completed styling to the task
    else:
        messagebox.showwarning("Selection Error", "Please select a task to complete.")  # Show warning if no task is selected

def remove_task():  # Function to remove a task from the task display
    task_index = get_current_task_index()  # Get the index of the currently selected task
    if task_index is not None:  # If a valid task is selected
        task_display.configure(state='normal')  # Enable the task display widget to allow text deletion
        task_display.delete(f"{task_index}.0", f"{task_index}.end+1c")  # Delete the selected task
        task_display.configure(state='disabled')  # Disable the task display widget again
    else:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")  # Show warning if no task is selected

def get_current_task_index():  # Function to get the index of the current task based on cursor position
    try:
        index = task_display.index('insert').split('.')[0]  # Get the line index where the cursor is placed
        return int(index)  # Return the index as an integer
    except:
        return None  # Return None if there's an error (e.g., no task is selected)

def apply_task_style(task, completed):  # Function to apply styling to tasks
    task_display.tag_add(task, 'end-2l', 'end-1l')  # Add a tag to the task text (last line of the task display)
    task_display.tag_config(  # Configure the styling of the task based on whether it is completed or not
        task, 
        foreground='green' if completed else 'red',  # Use green text for completed tasks, red for incomplete
        font=font.Font(size=18, weight='bold', overstrike=completed)  # Use bold font and strikethrough for completed tasks
    )

# --------------------------------------
# Task Highlighting Function
# --------------------------------------

def highlight_task(event):  # Function to highlight a task when clicked
    global highlighted_task  # Access the global variable to track the highlighted task
    task_index = task_display.index(f"@{event.x},{event.y}").split('.')[0]  # Get the index of the task at the click position
    if highlighted_task is not None:  # If a task is already highlighted
        task_display.tag_remove('highlight', f"{highlighted_task}.0", f"{highlighted_task}.end")  # Remove highlight from the previous task
    highlighted_task = task_index  # Update the global variable to the newly highlighted task
    task_display.tag_add('highlight', f"{task_index}.0", f"{task_index}.end")  # Add highlight to the clicked task
    task_display.tag_config('highlight', background='gray')  # Configure the highlight style (gray background)
    task_display.configure(state='normal')  # Enable the task display to allow focus
    app.focus()  # Set the focus back to the main app window
    task_display.configure(state='disabled')  # Disable the task display after highlighting

# --------------------------------------
# GUI Setup
# --------------------------------------

app = ttk.Window(themename="darkly")  # Create the main application window with the "darkly" theme
app.title("To-Do List Manager")  # Set the window title
app.geometry("600x500")  # Set the window size
app.configure(bg='#2E2E2E')  # Set the background color for the window

task_entry = ttk.Entry(app, font=('Helvetica', 15))  # Create an entry widget for inputting tasks, with a specified font
task_entry.pack(pady=20)  # Pack the entry widget into the window with padding
task_entry.bind('<Return>', add_task)  # Bind the Return (Enter) key to trigger the add_task function

ttk.Button(app, text="Add Task", command=add_task).pack(pady=10)  # Create a button to manually add a task

task_display = Text(  # Create a text widget to display the list of tasks
    app, font=('Helvetica', 14), height=11, bg='#3C3C3C', fg='white', wrap='none', state='disabled'
)
task_display.pack(pady=5)  # Pack the task display with padding
task_display.bind('<Button-1>', highlight_task)  # Bind the left mouse button to the highlight_task function

action_frame = ttk.Frame(app)  # Create a frame to hold action buttons (Complete, Remove)
action_frame.pack(pady=5)  # Pack the frame with padding
ttk.Button(  # Create a button to mark tasks as completed
    action_frame, text="Complete Task", command=complete_task, bootstyle="success", padding=(10, 5)
).pack(side='left', padx=5)  # Pack the button inside the frame with left alignment and padding
ttk.Button(  # Create a button to remove tasks
    action_frame, text="Remove Task", command=remove_task, bootstyle="danger", padding=(10, 5)
).pack(side='left', padx=5)  # Pack the button inside the frame with left alignment and padding
ttk.Button(  # Create a button to quit the application
    app, text="Quit", command=app.quit, bootstyle="danger-outline", padding=(10, 5)
).pack(pady=10)  # Pack the quit button with padding

app.mainloop()  # Start the Tkinter event loop, waiting for user interaction

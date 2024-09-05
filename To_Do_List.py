import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font

# Dictionary to keep track of completed tasks
completed_tasks = set()

# Function to add a new task
def add_task(event=None):
    task = task_entry.get()
    if task:
        # Insert the task into the listbox
        task_listbox.insert(END, task)
        task_entry.delete(0, END)

        # Get the index of the newly added task
        index = task_listbox.size() - 1

        # Directly apply styles to the newly added task
        task_listbox.itemconfig(index, {
            'bg': '#3C3C3C',  # Dark gray background
            'fg': 'red',       # Red text for new tasks
        })
        
        # Explicitly apply changes to ensure the font color is applied immediately
        task_listbox.selection_clear(0, END)  # Clear any selection to enforce UI refresh
        task_listbox.selection_set(index)     # Temporarily select the newly added item
        task_listbox.selection_clear(index)   # Then clear it, to show correct colors

    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Function to mark a task as completed
def complete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        # Remove the task from the listbox
        task_listbox.delete(selected_task_index)
        # Add the task to the end of the listbox with green strikethrough effect
        task_listbox.insert(END, task_text)
        task_listbox.itemconfig(END, {
            'bg': '#2E2E2E',  # Darker gray background
            'fg': 'green',  # Green text for completed tasks
            'font': Font(task_listbox, size=14, weight='bold').configure(overstrike=True)  # Larger font with strikethrough
        })
        completed_tasks.add(task_text)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to complete.")

# Function to remove a task
def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        # Remove from completed_tasks if it was completed
        completed_tasks.discard(task_text)
        task_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")

# Function to update task display on selection
def on_select(event):
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        if task_text in completed_tasks:
            # Ensure completed tasks retain green color and strikethrough effect
            task_listbox.itemconfig(selected_task_index, {
                'bg': '#2E2E2E',
                'fg': 'green',
                'font': Font(task_listbox, size=14, weight='bold').configure(overstrike=True)
            })
        else:
            # Default selection style for incomplete tasks
            task_listbox.itemconfig(selected_task_index, {
                'bg': '#3C3C3C',  # Dark gray background
                'fg': 'red'
            })
    else:
        # Reset to default styles if nothing is selected
        for i in range(task_listbox.size()):
            task_text = task_listbox.get(i)
            if task_text in completed_tasks:
                task_listbox.itemconfig(i, {
                    'bg': '#2E2E2E',
                    'fg': 'green',
                    'font': Font(task_listbox, size=14, weight='bold').configure(overstrike=True)
                })
            else:
                task_listbox.itemconfig(i, {
                    'bg': '#3C3C3C',
                    'fg': 'red',
                    'font': Font(task_listbox, size=14, weight='bold')  # Ensuring font size and weight are consistent
                })

# Initialize the main application window with ttkbootstrap
app = ttk.Window(themename="darkly")
app.title("To-Do List Manager")
app.geometry("600x500")  # Adjusted window size to be smaller

# Set the background color of the main window
app.configure(bg='#2E2E2E')  # Dark gray background

# Frame to organize widgets
frame = ttk.Frame(app, padding=10, bootstyle="dark", style='dark.TFrame')
frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)

# Entry widget for task input
task_entry = ttk.Entry(frame, width=40, font=('Helvetica', 14, 'bold'))
task_entry.pack(pady=10)

# Bind Enter key to add_task function
task_entry.bind('<Return>', add_task)

# Button to add a new task
add_button = ttk.Button(frame, text="Add Task", bootstyle="primary-outline", command=add_task, padding=(10, 5))
add_button.pack(pady=5)

# Listbox to display tasks with dark gray background and red text
task_listbox = tk.Listbox(frame, width=70, height=7, selectmode=SINGLE, bg='#3C3C3C', fg='red', selectbackground='#3C3C3C', selectforeground='red', font=('Helvetica', 14, 'bold'))
task_listbox.pack(pady=10)

# Bind selection event to the on_select function
task_listbox.bind('<<ListboxSelect>>', on_select)

# Buttons to complete or remove tasks
button_frame = ttk.Frame(frame)
button_frame.pack(pady=10)

complete_button = ttk.Button(button_frame, text="Complete Task", bootstyle="success", command=complete_task, padding=(10, 5))
complete_button.pack(side=LEFT, padx=10)

remove_button = ttk.Button(button_frame, text="Remove Task", bootstyle="danger", command=remove_task, padding=(10, 5))
remove_button.pack(side=LEFT, padx=10)

# Quit button
quit_button = ttk.Button(frame, text="Quit", bootstyle="danger-outline", command=app.quit, padding=(10, 5))
quit_button.pack(pady=(10, 20))  # Adjusted padding

# Start the application
app.mainloop()

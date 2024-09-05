import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font

completed_tasks = set()

def add_task(event=None):
    task = task_entry.get()
    if task:
        task_listbox.insert(END, task)
        task_entry.delete(0, END)
        index = task_listbox.size() - 1

        task_listbox.itemconfig(index, {
            'bg': '#3C3C3C',  
            'fg': 'red',       
        })
        
        task_listbox.selection_clear(0, END)  
        task_listbox.selection_set(index)     
        task_listbox.selection_clear(index)  

    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def complete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        task_listbox.delete(selected_task_index)
        task_listbox.insert(END, task_text)
        task_listbox.itemconfig(END, {
            'bg': '#2E2E2E',  
            'fg': 'green', 
            'font': Font(task_listbox, size=14, weight='bold').configure(overstrike=True)  
        })
        completed_tasks.add(task_text)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to complete.")

def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        completed_tasks.discard(task_text)
        task_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")

def on_select(event):
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        if task_text in completed_tasks:
            task_listbox.itemconfig(selected_task_index, {
                'bg': '#2E2E2E',
                'fg': 'green',
                'font': Font(task_listbox, size=14, weight='bold').configure(overstrike=True)
            })
        else:
            task_listbox.itemconfig(selected_task_index, {
                'bg': '#3C3C3C',  
                'fg': 'red'
            })
    else:
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
                    'font': Font(task_listbox, size=14, weight='bold')  
                })

app = ttk.Window(themename="darkly")
app.title("To-Do List Manager")
app.geometry("600x500")  

app.configure(bg='#2E2E2E')  

frame = ttk.Frame(app, padding=10, bootstyle="dark", style='dark.TFrame')
frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)

task_entry = ttk.Entry(frame, width=40, font=('Helvetica', 14, 'bold'))
task_entry.pack(pady=10)

task_entry.bind('<Return>', add_task)

add_button = ttk.Button(frame, text="Add Task", bootstyle="primary-outline", command=add_task, padding=(10, 5))
add_button.pack(pady=5)

task_listbox = tk.Listbox(frame, width=70, height=7, selectmode=SINGLE, bg='#3C3C3C', fg='red', selectbackground='#3C3C3C', selectforeground='red', font=('Helvetica', 14, 'bold'))
task_listbox.pack(pady=10)

task_listbox.bind('<<ListboxSelect>>', on_select)

button_frame = ttk.Frame(frame)
button_frame.pack(pady=10)

complete_button = ttk.Button(button_frame, text="Complete Task", bootstyle="success", command=complete_task, padding=(10, 5))
complete_button.pack(side=LEFT, padx=10)

remove_button = ttk.Button(button_frame, text="Remove Task", bootstyle="danger", command=remove_task, padding=(10, 5))
remove_button.pack(side=LEFT, padx=10)

quit_button = ttk.Button(frame, text="Quit", bootstyle="danger-outline", command=app.quit, padding=(10, 5))
quit_button.pack(pady=(10, 20))  # Adjusted padding

app.mainloop()

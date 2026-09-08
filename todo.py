import tkinter as tk
from tkinter import messagebox
import json
import os
FILE_NAME = "tasks.json"
LIGHT_BG = "#f4f6f8"
LIGHT_CARD = "#ffffff"
LIGHT_TEXT = "#1f2937"
LIGHT_ENTRY = "#ffffff"
LIGHT_BORDER = "#d1d5db"
DARK_BG = "#121212"
DARK_CARD = "#1e1e1e"
DARK_TEXT = "#f5f5f5"
DARK_ENTRY = "#2b2b2b"
DARK_BORDER = "#444444"
dark_mode = False
all_tasks = []
def load_tasks():
    global all_tasks
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
            all_tasks = []
            for item in data:
                if isinstance(item, str):
                    all_tasks.append({
                        "task": item,
                        "due_date": "Not Set",
                        "priority": "Medium",
                        "completed": False
                    })
                elif isinstance(item, dict):
                    all_tasks.append({
                        "task": item.get("task", ""),
                        "due_date": item.get("due_date", "Not Set"),
                        "priority": item.get("priority", "Medium"),
                        "completed": item.get("completed", False)
                    })
        except:
            all_tasks = []
    else:
        all_tasks = []
def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(all_tasks, file, indent=4)
def update_counts():
    total = len(all_tasks)
    completed = 0
    for task in all_tasks:
        if task.get("completed", False):
            completed += 1
    pending = total - completed
    count_label.config(
        text=f"Total: {total}   |   Pending: {pending}   |   Completed: {completed}"
    )
def display_tasks(tasks=None):
    if tasks is None:
        tasks = all_tasks
    task_list.delete(0, tk.END)
    for task in tasks:
        text = task.get("task", "")
        due = task.get("due_date", "Not Set")
        priority = task.get("priority", "Medium")
        completed = task.get("completed", False)
        if completed:
            display_text = (
                f"✓ {text} | Due: {due} | Priority: {priority}"
            )
        else:
            display_text = (
                f"□ {text} | Due: {due} | Priority: {priority}"
            )
        task_list.insert(tk.END, display_text)
        index = task_list.size() - 1
        if completed:
            task_list.itemconfig(
                index,
                foreground="#777777"
            )
        elif priority == "High":
            task_list.itemconfig(
                index,
                foreground="#e74c3c"
            )
        elif priority == "Medium":
            task_list.itemconfig(
                index,
                foreground="#f39c12"
            )
        else:
            task_list.itemconfig(
                index,
                foreground="#27ae60"
            )
    update_counts()
def add_task():
    task = task_entry.get().strip()
    due_date = due_entry.get().strip()
    priority = priority_var.get()
    if task == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a task!"
        )
        return
    if due_date == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a due date!"
        )
        return
    new_task = {
        "task": task,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }
    all_tasks.append(new_task)
    save_tasks()
    display_tasks()
    task_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)
    priority_var.set("Medium")
def delete_task():
    selected = task_list.curselection()
    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a task!"
        )
        return
    index = selected[0]
    if index < len(all_tasks):
        answer = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to delete this task?"
        )
        if answer:
            del all_tasks[index]
            save_tasks()
            display_tasks()
def complete_task():
    selected = task_list.curselection()
    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a task!"
        )
        return
    index = selected[0]
    if index < len(all_tasks):
        all_tasks[index]["completed"] = not all_tasks[index].get(
            "completed",
            False
        )
        save_tasks()
        display_tasks()
def clear_tasks():
    if len(all_tasks) == 0:
        messagebox.showinfo(
            "Information",
            "There are no tasks to clear."
        )
        return
    answer = messagebox.askyesno(
        "Clear All",
        "Are you sure you want to delete all tasks?"
    )
    if answer:
        all_tasks.clear()
        save_tasks()
        display_tasks()
def search_tasks():
    keyword = search_entry.get().strip().lower()
    if keyword == "":
        display_tasks()
        return
    filtered_tasks = []
    for task in all_tasks:
        if (
            keyword in task.get("task", "").lower()
            or keyword in task.get("due_date", "").lower()
            or keyword in task.get("priority", "").lower()
        ):
            filtered_tasks.append(task)
    display_tasks(filtered_tasks)
def show_all():
    search_entry.delete(0, tk.END)
    display_tasks()
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()
def apply_theme():
    if dark_mode:
        bg = DARK_BG
        card = DARK_CARD
        text = DARK_TEXT
        entry_bg = DARK_ENTRY
        border = DARK_BORDER
        dark_button.config(
            text="☀ Light Mode"
        )
    else:
        bg = LIGHT_BG
        card = LIGHT_CARD
        text = LIGHT_TEXT
        entry_bg = LIGHT_ENTRY
        border = LIGHT_BORDER

        dark_button.config(
            text="☾ Dark Mode"
        )
    root.config(bg=bg)
    canvas.config(bg=bg)
    main_frame.config(bg=bg)
    header_frame.config(bg=bg)
    title_label.config(
        bg=bg,
        fg=text
    )
    subtitle_label.config(
        bg=bg,
        fg="#888888"
    )
    input_frame.config(
        bg=card,
        highlightbackground=border
    )
    task_label.config(
        bg=card,
        fg=text
    )
    due_label.config(
        bg=card,
        fg=text
    )
    priority_label.config(
        bg=card,
        fg=text
    )
    task_entry.config(
        bg=entry_bg,
        fg=text,
        insertbackground=text
    )
    due_entry.config(
        bg=entry_bg,
        fg=text,
        insertbackground=text
    )
    priority_menu.config(
        bg=entry_bg,
        fg=text,
        activebackground=entry_bg,
        activeforeground=text
    )
    search_frame.config(
        bg=card,
        highlightbackground=border
    )
    search_entry.config(
        bg=entry_bg,
        fg=text,
        insertbackground=text
    )
    list_frame.config(
        bg=card,
        highlightbackground=border
    )
    task_list.config(
        bg=entry_bg,
        fg=text,
        selectbackground="#4f46e5",
        selectforeground="white"
    )
    scrollbar.config(
        troughcolor=card,
        bg=entry_bg
    )
    count_label.config(
        bg=bg,
        fg=text
    )
    bottom_frame.config(
        bg=bg
    )
    for widget in [
        add_button,
        delete_button,
        complete_button,
        clear_button,
        search_button,
        show_button,
        dark_button
    ]:
        widget.config(
            bg=card,
            fg=text,
            activebackground=entry_bg,
            activeforeground=text
        )
def mouse_wheel(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )
root = tk.Tk()
root.title("To-Do List")
root.state("zoomed")
root.minsize(800, 600)
root.config(bg=LIGHT_BG)
canvas = tk.Canvas(
    root,
    bg=LIGHT_BG,
    highlightthickness=0
)
canvas.pack(
    side="left",
    fill="both",
    expand=True
)
main_scrollbar = tk.Scrollbar(
    root,
    orient="vertical",
    command=canvas.yview
)
main_scrollbar.pack(
    side="right",
    fill="y"
)
canvas.config(
    yscrollcommand=main_scrollbar.set
)
main_frame = tk.Frame(
    canvas,
    bg=LIGHT_BG
)
canvas_window = canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)
def update_scroll_region(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )
    canvas.itemconfig(
        canvas_window,
        width=canvas.winfo_width()
    )
main_frame.bind(
    "<Configure>",
    update_scroll_region
)
canvas.bind(
    "<Configure>",
    update_scroll_region
)
canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)
header_frame = tk.Frame(
    main_frame,
    bg=LIGHT_BG
)
header_frame.pack(
    fill="x",
    pady=(30, 20)
)
title_label = tk.Label(
    header_frame,
    text="📝  TO-DO LIST",
    font=("Arial", 30, "bold"),
    bg=LIGHT_BG,
    fg=LIGHT_TEXT
)
title_label.pack()
subtitle_label = tk.Label(
    header_frame,
    text="Organize your tasks and stay productive",
    font=("Arial", 12),
    bg=LIGHT_BG,
    fg="#777777"
)
subtitle_label.pack(
    pady=5
)
dark_button = tk.Button(
    header_frame,
    text="☾ Dark Mode",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=18,
    pady=8,
    command=toggle_dark_mode
)
dark_button.pack(
    pady=8
)
input_frame = tk.Frame(
    main_frame,
    bg=LIGHT_CARD,
    highlightbackground=LIGHT_BORDER,
    highlightthickness=1
)
input_frame.pack(
    fill="x",
    padx=120,
    pady=10
)
task_label = tk.Label(
    input_frame,
    text="Task",
    font=("Arial", 12, "bold"),
    bg=LIGHT_CARD,
    fg=LIGHT_TEXT
)
task_label.pack(
    pady=(20, 5)
)
task_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=55,
    relief="flat",
    bg=LIGHT_ENTRY,
    fg=LIGHT_TEXT
)
task_entry.pack(
    ipady=9,
    pady=(0, 15)
)
due_label = tk.Label(
    input_frame,
    text="Due Date (DD-MM-YYYY)",
    font=("Arial", 12, "bold"),
    bg=LIGHT_CARD,
    fg=LIGHT_TEXT
)
due_label.pack(
    pady=5
)
due_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=35,
    relief="flat",
    bg=LIGHT_ENTRY,
    fg=LIGHT_TEXT
)
due_entry.pack(
    ipady=9,
    pady=(0, 15)
)
priority_label = tk.Label(
    input_frame,
    text="Priority",
    font=("Arial", 12, "bold"),
    bg=LIGHT_CARD,
    fg=LIGHT_TEXT
)
priority_label.pack(
    pady=5
)
priority_var = tk.StringVar(
    value="Medium"
)
priority_menu = tk.OptionMenu(
    input_frame,
    priority_var,
    "High",
    "Medium",
    "Low"
)
priority_menu.config(
    font=("Arial", 11),
    width=15,
    relief="flat"
)
priority_menu.pack(
    pady=(0, 15)
)
add_button = tk.Button(
    input_frame,
    text="➕  ADD TASK",
    font=("Arial", 12, "bold"),
    relief="flat",
    padx=25,
    pady=9,
    command=add_task
)
add_button.pack(
    pady=(0, 20)
)
search_frame = tk.Frame(
    main_frame,
    bg=LIGHT_CARD,
    highlightbackground=LIGHT_BORDER,
    highlightthickness=1
)
search_frame.pack(
    fill="x",
    padx=120,
    pady=10
)
search_entry = tk.Entry(
    search_frame,
    font=("Arial", 12),
    width=45,
    relief="flat",
    bg=LIGHT_ENTRY,
    fg=LIGHT_TEXT
)
search_entry.pack(
    side="left",
    padx=(20, 10),
    pady=12,
    ipady=8
)
search_button = tk.Button(
    search_frame,
    text="🔍 SEARCH",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    command=search_tasks
)
search_button.pack(
    side="left",
    padx=5
)
show_button = tk.Button(
    search_frame,
    text="📋 SHOW ALL",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    command=show_all
)
show_button.pack(
    side="left",
    padx=5
)
list_frame = tk.Frame(
    main_frame,
    bg=LIGHT_CARD,
    highlightbackground=LIGHT_BORDER,
    highlightthickness=1
)
list_frame.pack(
    fill="both",
    expand=True,
    padx=120,
    pady=10
)
task_list = tk.Listbox(
    list_frame,
    font=("Arial", 12),
    relief="flat",
    bd=0,
    height=10,
    bg=LIGHT_ENTRY,
    fg=LIGHT_TEXT,
    selectbackground="#4f46e5",
    selectforeground="white"
)
task_list.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    pady=5
)
scrollbar = tk.Scrollbar(
    list_frame,
    orient="vertical",
    command=task_list.yview
)
scrollbar.pack(
    side="right",
    fill="y"
)
task_list.config(
    yscrollcommand=scrollbar.set
)
count_label = tk.Label(
    main_frame,
    text="Total: 0   |   Pending: 0   |   Completed: 0",
    font=("Arial", 12, "bold"),
    bg=LIGHT_BG,
    fg=LIGHT_TEXT
)
count_label.pack(
    pady=12
)
bottom_frame = tk.Frame(
    main_frame,
    bg=LIGHT_BG
)
bottom_frame.pack(
    pady=(5, 30)
)
delete_button = tk.Button(
    bottom_frame,
    text="🗑 DELETE",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=20,
    pady=9,
    command=delete_task
)
delete_button.pack(
    side="left",
    padx=8
)
complete_button = tk.Button(
    bottom_frame,
    text="☑ COMPLETE",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=20,
    pady=9,
    command=complete_task
)
complete_button.pack(
    side="left",
    padx=8
)
clear_button = tk.Button(
    bottom_frame,
    text="🧹 CLEAR ALL",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=20,
    pady=9,
    command=clear_tasks
)
clear_button.pack(
    side="left",
    padx=8
)
load_tasks()
display_tasks()
apply_theme()
root.mainloop()	
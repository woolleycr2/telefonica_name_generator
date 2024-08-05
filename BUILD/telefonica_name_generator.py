import tkinter as tk
from tkinter import ttk, messagebox

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self):
        "Display text in tooltip window"
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    tool_tip = ToolTip(widget, text)
    def enter(event):
        tool_tip.showtip()
    def leave(event):
        tool_tip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# Function to read the list from the text file
def read_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

# Function to update the list with the ID and Letter
def update_list():
    id_value = id_entry.get().strip()
    letter_value = letter_entry.get().strip()
    
    if not id_value:
        messagebox.showwarning("Input Error", "ID field is required")
        return
    
    updated_list = []
    for item in original_list:
        main_text, *description = item.split("//", 1)
        updated_item = f"{id_value}_{letter_value}_{main_text}" if letter_value else f"{id_value}_{main_text}"
        explanation = description[0].strip() if description else ""
        updated_list.append((updated_item, explanation))
    
    display_updated_list(updated_list)

# Function to display the updated list in the GUI
def display_updated_list(updated_list):
    for widget in list_frame.winfo_children():
        widget.destroy()
    
    for item, explanation in updated_list:
        frame = tk.Frame(list_frame)
        frame.pack(fill="x", padx=5, pady=2)
        
        label = tk.Label(frame, text=item, anchor="w")
        label.pack(side="left", fill="x", expand=True)
        
        if explanation:
            question_mark = tk.Label(frame, text="?", fg="blue", cursor="hand2")
            question_mark.pack(side="left")
            create_tooltip(question_mark, explanation)
        
        copy_button = tk.Button(frame, text="Copy", command=lambda text=item: copy_to_clipboard(text))
        copy_button.pack(side="right")

# Function to copy text to the clipboard
def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)

# Function to handle mouse wheel scrolling
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Main GUI setup
root = tk.Tk()
root.title("Telefonica Name Generator")

# Reading the original list from the text file
original_list = read_list('list.txt')

# Input fields and labels
tk.Label(root, text="Enter ID (e.g., 123456789_123456789):").pack(pady=(10, 0))
id_entry = tk.Entry(root, width=50)
id_entry.pack(pady=(0, 10))

tk.Label(root, text="Enter Site (optional):").pack(pady=(10, 0))
letter_entry = tk.Entry(root, width=50)
letter_entry.pack(pady=(0, 10))

# Update button
update_button = tk.Button(root, text="Update", command=update_list)
update_button.pack(pady=20)

# Canvas and scrollbar for the result frame
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Bind the mouse wheel event to the scroll function
canvas.bind_all("<MouseWheel>", on_mouse_wheel)
scrollable_frame.bind_all("<MouseWheel>", on_mouse_wheel)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Frame to display the updated list
list_frame = tk.Frame(scrollable_frame)
list_frame.pack(fill="both", expand=True)

# Start the main event loop
root.mainloop()

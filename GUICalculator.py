import tkinter as tk
from tkinter import ttk
import math

calculation = ""
history = []
memory = None  # Memory storage

# -------------------- Logic Functions --------------------

def add_to_calculation(symbol):
    """Adds clicked button value or typed key to the calculation."""
    global calculation
    calculation += str(symbol)
    text_result.delete(0, "end")
    text_result.insert(0, calculation)

def evaluate_calculation():
    """Evaluates the entered expression and updates the display."""
    global calculation, history
    try:
        result = str(eval(calculation))
        history.append(f"{calculation} = {result}")
        text_result.delete(0, "end")
        text_result.insert(0, result)
        calculation = result  # Store result for continued calculations
    except:
        clear_field()
        text_result.insert(0, "Error")

def clear_field():
    """Clears the input field and resets the calculation."""
    global calculation
    calculation = ""
    text_result.delete(0, "end")

def show_history():
    """Opens a new window displaying past calculations."""
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_window.geometry("300x300")
    history_window.configure(bg="white")

    history_text = tk.Text(history_window, height=10, width=40, bg="white", fg="black", font=("Arial", 12))
    history_text.pack(padx=10, pady=10)
    history_text.insert("end", "\n".join(history))

def memory_store():
    """Stores the current calculation result in memory."""
    global memory
    try:
        memory = float(eval(calculation))
    except:
        memory = None

def memory_recall():
    """Recalls the stored memory value."""
    if memory is not None:
        add_to_calculation(memory)

def memory_clear():
    """Clears stored memory."""
    global memory
    memory = None

def on_key_press(event):
    """Handles keyboard input."""
    key = event.char
    if key in "0123456789+-*/().":
        add_to_calculation(key)
    elif key == "\r":  # Enter key
        evaluate_calculation()
    elif key == "\x08":  # Backspace key
        clear_field()

# -------------------- UI Setup --------------------

root = tk.Tk()
root.geometry("500x650")  # Increased height for better spacing
root.title("Advanced Calculator")
root.configure(bg="white")
root.bind("<Key>", on_key_press)  # Enable keyboard input

# Custom Styled Buttons
style = ttk.Style()
style.configure("TButton", font=("Arial", 14), padding=10, relief="flat")

# Display Box
text_result = tk.Entry(root, font=("Arial", 24), bg="white", fg="black", borderwidth=3, relief="solid", justify="right")
text_result.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=12, pady=15, padx=10, sticky="nsew")

# Memory & History Buttons (Top Right)
memory_buttons = [
    ("M+", memory_store), ("MR", memory_recall), ("MC", memory_clear), ("History", show_history)
]

for i, (text, command) in enumerate(memory_buttons):
    ttk.Button(root, text=text, command=command, width=7).grid(row=i, column=4, padx=5, pady=5, sticky="nsew")

# Buttons Layout (Fixed "+" Position)
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("+", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("*", 3, 3),
    ("0", 4, 1), (" ", 4, 0), (" ", 4, 2), ("/", 4, 3),
    ("+", 5, 3)  
]

for (text, row, col) in buttons:
    btn = ttk.Button(root, text=text, command=lambda t=text: add_to_calculation(t), width=6)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

# Special Buttons (Bottom Row)
ttk.Button(root, text="=", command=evaluate_calculation, width=14).grid(row=5, column=2, columnspan=2, pady=8, sticky="nsew")
ttk.Button(root, text="C", command=clear_field, width=14).grid(row=5, column=0, columnspan=2, pady=8, sticky="nsew")

# Scientific Functions (Placed Vertically on Right Side)
scientific_buttons = [
    ("sin", "math.sin("), ("cos", "math.cos("), ("tan", "math.tan("),
    ("log", "math.log("), ("√", "math.sqrt("), ("^", "**")
]

for i, (text, func) in enumerate(scientific_buttons):
    ttk.Button(root, text=text, command=lambda f=func: add_to_calculation(f), width=7).grid(row=i+4, column=4, padx=5, pady=5, sticky="nsew")

# Ensure equal column width
for i in range(5):  # Adjusted to include scientific function column
    root.grid_columnconfigure(i, weight=1)
for i in range(8):  # Adjusted for better spacing
    root.grid_rowconfigure(i, weight=1)

root.mainloop()
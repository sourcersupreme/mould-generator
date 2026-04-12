import tkinter as tk
from tkinter import ttk, messagebox
from modules.brick import generate_brick_mould
from modules.zigzag import generate_zigzag_mould
# later: zigzag, ishape


def generate():
    mould = mould_var.get()
    cavities = int(cavity_var.get())

    if mould == "Brick Mould":
        generate_brick_mould("output.pdf", cavities)

    elif mould == "Zig-Zag Mould":
        generate_zigzag_mould("output.pdf", cavities)

    else:
        messagebox.showwarning("Error", "Not implemented")

    messagebox.showinfo("Success", "PDF Generated")


root = tk.Tk()
root.title("Mould Generator")
root.geometry("420x300")

title = tk.Label(root, text="Mould Generator", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Mould type
tk.Label(root, text="Select Mould Type").pack()
mould_var = tk.StringVar()
mould_dropdown = ttk.Combobox(root, textvariable=mould_var, state="readonly")
mould_dropdown['values'] = ("Brick Mould", "Zig-Zag Mould", "I-Shape Mould")
mould_dropdown.current(0)
mould_dropdown.pack(pady=5)

# Cavities
tk.Label(root, text="Select Cavities").pack()
cavity_var = tk.StringVar()
cavity_dropdown = ttk.Combobox(root, textvariable=cavity_var, state="readonly")
cavity_dropdown['values'] = ("4", "6", "8", "9", "10", "12", "14", "24")
cavity_dropdown.current(2)
cavity_dropdown.pack(pady=5)

# Button
btn = tk.Button(root, text="Generate PDF", command=generate, bg="green", fg="white")
btn.pack(pady=20)

root.mainloop()

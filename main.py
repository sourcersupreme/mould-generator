import tkinter as tk
from tkinter import ttk, messagebox
from modules.brick import generate_brick_mould


def generate():
    mould_type = mould_var.get()

    if mould_type == "Brick Mould":
        generate_brick_mould("output.pdf")
        messagebox.showinfo("Success", "PDF Generated: output.pdf")

    else:
        messagebox.showwarning("Error", "Invalid selection")


# GUI Window
root = tk.Tk()
root.title("Mould Generator")
root.geometry("400x250")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Mould Generator", font=("Arial", 16, "bold"))
title.pack(pady=15)

# Dropdown
mould_var = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=mould_var, state="readonly")
dropdown['values'] = ("Brick Mould",)
dropdown.current(0)
dropdown.pack(pady=10)

# Button
generate_btn = tk.Button(root, text="Generate PDF", command=generate, bg="green", fg="white", width=20)
generate_btn.pack(pady=20)

# Run
root.mainloop()

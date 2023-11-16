import tkinter
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter.messagebox import askyesno
from tkinter import ttk
import ctypes


def drop_action(e):
    if str(e.data).startswith('{'):
        path = str(e.data[1:len(str(e.data)) - 1])
    else:
        path = str(e.data)
    lb.delete(1)
    try:
        lb.insert(2, path[path.rfind("/") + 1:len(path)])
    except:
        lb.insert(2, path)
    return path


root = TkinterDnD.Tk()
root.geometry("800x600")
root.title("Logó felismerés")

global lb
lb = tk.Listbox(root, relief="flat", width=50, height=6, background="cyan",
                activestyle="none")
lb.configure(justify="center", font=("Calibri", 20))
lb.insert(1, "Húzza ide a fájlt")
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', lambda e: drop_action(e))
lb.bindtags((lb, root, "none"))
lb.pack(fill="x")
ctypes.windll.shcore.SetProcessDpiAwareness(1)
root.mainloop()


import tkinter
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter.messagebox import askyesno
from tkinter import ttk
import ctypes
import torch

img_path = ""

model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5/runs/train/yolo_logo_detect/weights/best.pt')


def get_result():
    if not img_path:
        message_label.configure(text="Nincs megadva útvonal")
    results = model(img_path)
    message_label.configure(results.pandas().xyxy[0])
    

def drop_action(e):
    global img_path
    if str(e.data).startswith('{'):
        img_path = str(e.data[1:len(str(e.data)) - 1])
    else:
        img_path = str(e.data)
    lb.delete(1)
    try:
        lb.insert(2, img_path[img_path.rfind("/") + 1:len(img_path)])
    except:
        lb.insert(2, img_path)
    return img_path


root = TkinterDnD.Tk()
root.geometry("1000x600")
root.title("Logó felismerés")

global lb
lb = tk.Listbox(root, relief="flat", height=3, background="cyan",
                activestyle="none")
lb.configure(justify="center", font=("Calibri", 20))
lb.insert(1, "Húzza ide a fájlt")
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', lambda e: drop_action(e))
lb.bindtags((lb, root, "none"))
lb.pack(fill="x")

start_button = tk.Button(root, text="Kép elemzése", width=20, height=3,bd=1, background="#03a1fc", activebackground="#0471b0", font=("Calibri", 20), command=get_result)
start_button.pack(fill="x")

message_label = tk.Label(root, text="", background="white", height=10, font=("Calibri", 20))
message_label.pack(fill="x", side=tk.BOTTOM)

ctypes.windll.shcore.SetProcessDpiAwareness(1)
root.mainloop()


import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import ctypes
import torch
import cv2
from PIL import Image, ImageTk

img_path = ""

model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5/runs/train/yolo_logo_detect/weights/best.pt')
window_height = 750

def draw_bounding_boxes(img, results_df):
    color = (0, 255, 0)  # BGR color format (green in this case)
    text_color = (255, 255, 255)  # White text
    background_color = (0, 0, 0)  # Black background
    background_opacity = 0.7  # Opacity of the background

    thickness = 2  # Thickness of the bounding box
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 2  # Increased font thickness for bold effect

    for index, row in results_df.iterrows():
        x0, y0, x1, y1 = map(int, row.iloc[0:4])
        
        # Draw bounding box
        cv2.rectangle(img, (x0, y0), (x1, y1), color, thickness)
        confidence = row.iloc[4]
        name = row[6]
        text = f"{name} {confidence:.2f}"
        if x0:
            message_label.configure(text="Kép sikeresen elemezve, logó megtalálva")
        
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

        # Reduce the gap between text and bounding box
        text_offset_x = 5
        text_offset_y = 5

        text_position = (x0 + text_offset_x, y0 - text_offset_y) if y0 - text_offset_y > 18 else (x0 + text_offset_x, y1 + text_offset_y)

        # Draw filled rectangle as the background with opacity
        background_rect = ((text_position[0], text_position[1] - text_size[1]),
                           (text_position[0] + text_size[0] + 2 * text_offset_x, text_position[1] + text_size[1] + text_offset_y))
        img = cv2.rectangle(img, (int(background_rect[0][0]), int(background_rect[0][1])),
                            (int(background_rect[1][0]), int(background_rect[1][1])),
                            background_color, cv2.FILLED)
        img = cv2.addWeighted(img, background_opacity, img, 1 - background_opacity, 0)

        # Draw text on top of the background
        cv2.putText(img, text, text_position, font, font_scale, text_color, font_thickness)

    # Calculate the scaling factor to fit the image height to the window height
    scale_factor = window_height / img.shape[0]
    
    # Resize the image based on the scaling factor
    img_resized = cv2.resize(img, (int(img.shape[1] * scale_factor), window_height))

    img_pil = Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(img_pil)

    # Update the Tkinter label with the new image
    label.config(image=img_tk)
    label.image = img_tk


def get_result():
    if not img_path:
        message_label.configure(text="Nincs kép behúzva")
    image = cv2.imread(img_path)
    try:
        results = model(img_path)
        results_df = results.pandas().xyxy[0]
        confidence = results_df.iat[0, 4]
        name = results_df.iat[0, 6]
        print(results.pandas().xyxy[0])
        
        draw_bounding_boxes(image, results_df)
    except:
        try:
            draw_bounding_boxes(image, results_df)
            message_label.configure(text="A képen nem detektálható logó")
        except:
            label.image = None
            blank_image = tk.PhotoImage(width=1, height=1)
            label.config(image=blank_image)
            message_label.configure(text="A behúzott fájl nem kép")

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
        # Calculate the scaling factor to fit the image height to the window height
    try:
        img = cv2.imread(img_path)
        scale_factor = window_height / img.shape[0]
        
        # Resize the image based on the scaling factor
        img_resized = cv2.resize(img, (int(img.shape[1] * scale_factor), window_height))

        img_pil = Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(img_pil)

        # Update the Tkinter label with the new image
        label.config(image=img_tk)
        label.image = img_tk
        message_label.configure(text="Kép sikeresen beolvasva")
    except:
        label.image = None
        blank_image = tk.PhotoImage(width=1, height=1)
        label.config(image=blank_image)
        message_label.configure(text="A behúzott fájl nem kép")
    return img_path


root = TkinterDnD.Tk()
root.geometry("1000x980")
root.title("Logó felismerés")

global lb
lb = tk.Listbox(root, relief="flat", height=3, background="cyan",
                activestyle="none")
lb.configure(justify="center", font=("Calibri", 20))
lb.insert(1, "Húzd ide a képet")
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', lambda e: drop_action(e))
lb.bindtags((lb, root, "none"))
lb.pack(fill="x")

start_button = tk.Button(root, text="Kép elemzése", width=20, height=2,bd=1, background="#03a1fc", activebackground="#0471b0", font=("Calibri", 20), command=get_result)
start_button.pack(fill="x")

# Create a label for displaying the image
label = tk.Label(root)
label.pack()

message_label = tk.Label(root, text="", background="white", height=10, font=("Calibri", 20))
message_label.place(relx=0.5, rely=1.0, anchor=tk.S, relwidth=1, height=30)

ctypes.windll.shcore.SetProcessDpiAwareness(1)
root.mainloop()


import tensorflow as tf

from keras import layers, models
from keras.src.activations import relu, softmax
import matplotlib.pyplot as plt

import cv2
import os
import numpy as np
import math


image_folder = 'logos/audi'
output_folder = 'logos/output'

bbox_file = 'logos/audi/audi.txt'

box_colors = [(0, 0, 255)]
box_thickness = 3
os.makedirs(output_folder, exist_ok=True)
j = 0
image = []
image2 = []
label_list = []
label_l = []

with open(bbox_file, 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.strip().split(', ')
    image_file = parts[0]
    image_path = os.path.join(image_folder, image_file)
    image.append(cv2.imread(image_path))

    if image[j] is not None:
        for i in range(1, len(parts), 6):
            x0, y0, x1, y1, label, label_number = map(str.strip, parts[i:i+6])
            x0, y0, x1, y1, label_number = int(x0), int(y0), int(x1), int(y1), int(label_number)

            kozeppont_x = (x1-x0) // 2
            kozeppont_y = (y1-y0) // 2
            kozep_x2 = x0 + kozeppont_x
            kozep_y2 = y0 + kozeppont_y
            rec_x0 = math.floor(kozep_x2 - 50)
            rec_x1 = math.floor(kozep_x2 + 50)
            rec_y0 = math.floor(kozep_y2 - 50)
            rec_y1 = math.floor(kozep_y2 + 50)

            img = image[j]

            image2 = img[rec_y0:rec_y1, rec_x0:rec_x1]
            label_list.append(label_number)

        output_image_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_image_path, image2)

        j += 1
    else:
        print(f"Hiba: Nem sikerült betölteni a képet: {image_file}")

cv2.destroyAllWindows()


image2 = image2 / 255.0
class_names = ['apple', 'audi', 'barilla', 'bmw', 'mcdonalds', 'nike', 'other']
label_np = np.array(label_list)

# konvolúciós alap
# Conv2D és MaxPooling2D rétegek
model = models.Sequential()
# egy konvolúció egy 3x3-as szűrővel
model.add(layers.Conv2D(32, (3, 3), activation=relu, input_shape=(100, 100, 3)))
# egy maximumkiválasztás egy 2x2-es sablont használva
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation=relu))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation=relu))
# “kihajtogatja” a bemeneti tenzort
model.add(layers.Flatten())
# 64 db neuront hoz létre
model.add(layers.Dense(64, activation=relu))
# a 7-ből melyik osztalyba tartozik a logo
model.add(layers.Dense(7, activation=softmax))
model.summary()

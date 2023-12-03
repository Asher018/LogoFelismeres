#import tensorflow as tf

from keras import layers, models
from keras.src.activations import relu, softmax
import matplotlib.pyplot as plt

import cv2
import os
import numpy as np
import math


# a box kozeppontja
def center(start, end):
    center_pont = (end - start) // 2
    return start + center_pont


image_folder = 'logos/images'
output_folder = 'logos/output'

bbox_file = 'logos/images/images.txt'

box_colors = [(0, 0, 255)]
box_thickness = 3
os.makedirs(output_folder, exist_ok=True)
j = 0
image2 = []
label_list = []

with open(bbox_file, 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.strip().split(', ')
    image_file = parts[0]
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)

    if image is not None:
        for i in range(1, len(parts), 6):
            x0, y0, x1, y1, label, label_number = map(str.strip, parts[i:i+6])
            x0, y0, x1, y1, label_number = int(x0), int(y0), int(x1), int(y1), int(label_number)

            center_x = center(x0, x1)
            center_y = center(y0, y1)
            rec_x0 = math.floor(center_x - 50)
            rec_x1 = math.floor(center_x + 50)
            rec_y0 = math.floor(center_y - 50)
            rec_y1 = math.floor(center_y + 50)

            image2 = image[rec_y0:rec_y1, rec_x0:rec_x1]
            label_list.append(label_number)

        output_image_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_image_path, image2)

        j += 1
    else:
        print(f"Hiba: Nem sikerült betölteni a képet: {image_file}")

cv2.destroyAllWindows()

image2 = image2 / 255.0
class_names = ['apple', 'audi', 'barilla', 'bmw', 'mcdonalds', 'nike']
label_np = np.array(label_list)

# CNN konvolúciós neurális hálózat
model = models.Sequential()
# egy konvolúciós réteg egy 3x3-as szűrővel
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
model.add(layers.Dense(6, activation=softmax))
model.summary()

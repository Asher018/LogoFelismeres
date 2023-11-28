import cv2
import os
import shutil
from sklearn.model_selection import train_test_split


# a box kozeppontja
def center(start, end):
    center_pont = (end - start) // 2
    return start + center_pont


# train es test kepek es labelek kulon folderekbe
def copy(split, path):
    if not os.path.isdir(path):
        os.makedirs(path)
    for x in split:
        shutil.copy(x, path)


image_folder = 'logos/images'
all_labels = 'logos/images/images.txt'
labels = 'logos/labels/'

train_logos = 'logos/train/images/'
train_labels = 'logos/train/labels/'
test_logos = 'logos/test/images/'
test_labels = 'logos/test/labels/'
val_logos = 'logos/val/images/'
val_labels = 'logos/val/labels/'

j = 0
label_list = []
image_list = []

with open(all_labels, 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.strip().split(', ')
    image_file = parts[0]
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)
    image_list.append(image_path)

    if image is not None:
        img_width, img_height, img_depth = image.shape

        for i in range(1, len(parts), 6):
            x0, y0, x1, y1, label, label_number = map(str.strip, parts[i:i + 6])
            x0, y0, x1, y1, label_number = int(x0), int(y0), int(x1), int(y1), int(label_number)

            center_x = center(x0, x1)
            center_y = center(y0, y1)

            # uj txt fajl a label-oknek
            image_filename = image_file.split('.')
            f = open(labels + image_filename[0] + ".txt", 'w')

            width = x1 - x0
            height = y1 - y0

            # a box kozeppontja, szelessege es magassaga [0,1] tartomanyban, 3 tizedesjegyre kerekitve
            center_x = round(center_x / img_width, 3)
            center_y = round(center_y / img_height, 3)
            width = round(width / img_width, 3)
            height = round(height / img_height, 3)

            f.write(" ".join([str(label_number), str(center_x), str(center_y), str(width), str(height)]))
            f.close()

            label_list.append(labels + image_filename[0] + ".txt")

        j += 1
    else:
        print(f"Hiba: Nem sikerült betölteni a képet: {image_file}")

cv2.destroyAllWindows()

# a kepek es labelek tanito- es teszthalmazra bontasa
img_train, img_test, label_train, label_test = train_test_split(image_list, label_list, test_size=0.2, random_state=1)
img_val, img_test, label_val, label_test = train_test_split(img_test, label_test, test_size=0.5, random_state=1)

copy(img_train, train_logos)
copy(img_test, test_logos)
copy(img_val, val_logos)
copy(label_train, train_labels)
copy(label_test, test_labels)
copy(label_val, val_labels)

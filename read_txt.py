import cv2
import os

image_folder = 'logos/mcdonalds'
output_folder = 'logos/output'

bbox_file = 'logos/mcdonalds/mcdonalds.txt'

box_colors = [(0, 0, 255)]
box_thickness = 3
os.makedirs(output_folder, exist_ok=True)

with open(bbox_file, 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.strip().split(', ')
    image_file = parts[0]
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)

    if image is not None:
        for i in range(1, len(parts), 5):
            x0, y0, x1, y1, label = map(str.strip, parts[i:i+5])
            x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

            cv2.rectangle(image, (x0, y0), (x1, y1), box_colors[0], box_thickness)
            cv2.putText(image, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_colors[0], 2)

        output_image_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_image_path, image)
    else:
        print(f"Hiba: Nem sikerült betölteni a képet: {image_file}")

cv2.destroyAllWindows()

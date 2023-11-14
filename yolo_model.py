import cv2
import math
import numpy as np

image_path = 'test_logo/logo_test.jpg'
image = cv2.imread(image_path)
logo_image_path = 'logos/test/audi_1.jpg'
image_logo = cv2.imread(logo_image_path)


# Képek közötti hasonlóság számítása és megjelenítése.
def compare(img1, img2):
    diff = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    diff /= float(img1.shape[0] * img1.shape[1])
    compare_result = 'Result: {:.2f}'.format(diff)
    print(compare_result)
    cv2.waitKey(0)
    return compare_result


x1, y1 = 0, 0
x2, y2 = 100, 100
box_colors = [(0, 0, 255)]
box_thickness = 3

if image is not None:
    height, width, channels = image.shape

    box_height = math.floor(height / 100)
    box_width = math.floor(width / 100)
    box_w, box_h = 0, 0

    min = 1000000000.0
    min_x1, min_x2 = 0, 0
    min_y1, min_y2 = 0, 0
    img_box2 = ""

    # kép berácsozása
    for j in range(y1, height, y2):
        box_h += 1
        for i in range(x1, (width//12)*7, x2):
            box_w += 1
            if box_w <= box_width or box_h <= box_height:
                cv2.rectangle(image, (i, j), (i + x2, j + y2), box_colors[0], box_thickness)

                print(i, j)
                print(i + x2, j + y2)

                img_box = image[i:i + x2, j:j + y2]
                h, w = img_box.shape[:2]
                h2, w2 = image_logo.shape[:2]

                print(h, w)
                print(h2, w2)

                result = compare(img_box, image_logo)
                result_split = result.split(": ")

                if min > float(result_split[1]):
                    min = float(result_split[1])
                    min_x1 = i
                    min_x2 = i + x2
                    min_y1 = j
                    min_y2 = j + y2
                    img_box2 = image[min_x1:min_x2, min_y1:min_y2]


    print(min)
    print('(x,y)=', min_x1, min_y1)
    print('(x2,y2)=', min_x2, min_y2)
    cv2.imwrite("logos/test/image.jpg", image)
    cv2.imwrite("logos/test/image2.jpg", img_box2)
else:
    print(f"Error: {image_path}")


# 3950.62
# (x,y)= 300 200
# (x2,y2)= 400 300

import cv2
import numpy as np
import os


images_path = "original_logos/bmw"
image_width = 1000
image_height = 1000

for image_path in os.listdir(images_path):
    image = cv2.imread(f"{images_path}/{image_path}")
    height, width, channels = image.shape
    if height < 1000 or width < 1000:
        raise "Túl kicsi kép"

    # Calculate the coordinates for cropping
    x_start = (width - image_width) // 2
    y_start = (height - image_height) // 2
    x_end = x_start + image_width
    y_end = y_start + image_height

    # Crop the middle x*y pixel area
    cropped_image = image[y_start:y_end, x_start:x_end]

    # Normalize the image
    normalized_image = image.astype(np.float32)
    cv2.normalize(normalized_image, normalized_image, 0, 1, cv2.NORM_MINMAX)

    # Write output image
    os.makedirs(f"{images_path}/corrected", exist_ok=True)
    cv2.imwrite(f"{images_path}/corrected/{image_path}", cropped_image)
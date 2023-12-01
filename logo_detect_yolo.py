import torch

# egy kiválasztott képen lévő logó detektálás

model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5/runs/train/yolo_logo_detect/weights/best.pt')

img_path = 'logos/test/images/test.jpg'

results = model(img_path)

print(results.pandas().xyxy[0])


import subprocess

# az összes test mappában található kép detektálása

command = [
    "python",
    "yolov5/detect.py",
    "--source",
    "logos/test/images/",
    "--weights",
    "yolov5/runs/train/yolo_logo_detect/weights/best.pt",
    "--conf",
    "0.3",
    "--name",
    "yolo_logo_detection",
    "--save-txt"
]

subprocess.run(command)
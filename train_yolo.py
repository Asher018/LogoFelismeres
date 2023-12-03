import subprocess

command = [
    "python",
    "yolov5/train.py",
    "--img",
    "640",
    "--cfg",
    "yolov5s.yaml",
    "--hyp",
    "hyp.scratch-low.yaml",
    "--batch",
    "16",
    "--epochs",
    "200",
    "--data",
    "logo_detection.yaml",
    "--weights",
    "yolov5s.pt",
    "--workers",
    "24",
    "--name",
    "yolo_logo_detect"
]

subprocess.run(command)

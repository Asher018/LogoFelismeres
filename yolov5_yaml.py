import os.path

from git import Repo


def write_to_file():
    f = open("yolov5/data/logo_detection.yaml", 'w')
    f.write("path: ../logos \ntrain: train \ntest: test \nval: val \n\nnc: 6 \n\nnames: \n 0: apple \n 1: audi \n" +
            " 2: barilla \n 3: bmw \n 4: mcdonalds \n 5: nike")
    f.close()


if os.path.exists("yolov5"):
    write_to_file()
else:
    Repo.clone_from("https://github.com/ultralytics/yolov5.git", "yolov5")
    write_to_file()

#Futtasd: pip install -r yolov5/requirements.txt

from mathreader.image_processing import preprocessing as preprocessing
import numpy as np
import cv2
import os
import re
import math
from sklearn.utils import shuffle
from threading import Thread
from union import treatment_dir


treated_dir = "treated_data/"
main_dir = treatment_dir + "datasets/kaggle/"
if not os.path.exists(treatment_dir + treated_dir):
    os.mkdir(treatment_dir + treated_dir)


def get_symbols():
    training_images, training_labels, testing_images, testing_labels = [], [], [], []
    dirs = [
        "0/",
        "1/",
        "2/",
        "3/",
        "4/",
        "5/",
        "6/",
        "7/",
        "8/",
        "9/",
        "=/",
        "-/",
        ",/",
        "(/",
        ")/",
        "[/",
        "]/",
        "{/",
        "}/",
        "+/",
        "a/",
        "b/",
        "c/",
        "m/",
        "mul/",
        "sqrt/",
        "x/",
        "y/",
        "z/",
        "neq/",
    ]

    labels = {
        "0/": "0",
        "1/": "1",
        "2/": "2",
        "3/": "3",
        "4/": "4",
        "5/": "5",
        "6/": "6",
        "7/": "7",
        "8/": "8",
        "9/": "9",
        "=/": "10",
        "-/": "10",
        "(/": "11",
        ")/": "12",
        "[/": "13",
        "]/": "14",
        "{/": "15",
        "}/": "16",
        "+/": "17",
        "a/": "18",
        "b/": "19",
        "c/": "20",
        "m/": "21",
        "n/": "22",
        "sqrt/": "23",
        "x/": "24",
        "y/": "25",
        "z/": "26",
        "neq/": "27",
        ",/": "28",
        "mul/": "29",
    }

    configs = {"black": False, "dilate": True, "dataset": True, "resize": "smaller"}

    def parallel(interval):
        train_images, train_labels, test_images, test_labels = [], [], [], []
        for j in range(interval[0], interval[1] + 1):
            files = dirs[j]
            f = os.listdir(main_dir + files)
            count, amount = 1, len(f)
            training_size, testing_size = math.floor(amount * 80 / 100), math.floor(amount * 20 / 100)
            for filename in f:
                if re.search("\.(jpg|jpeg|png)$", filename, re.IGNORECASE):
                    image = cv2.imread(main_dir + files + filename)
                    image = preprocessing.ImagePreprocessing(configs).treatment_sem_segment(image)
                    if image and count <= training_size:
                        train_images.append(image)
                        train_labels.append(labels[files])
                    elif image and count <= training_size + testing_size:
                        test_images.append(image)
                        test_labels.append(labels[files])
                    else:
                        break
                    count += 1
        training_images.extend(train_images)
        training_labels.extend(train_labels)
        testing_images.extend(test_images)
        testing_labels.extend(test_labels)

    size, remain = len(dirs) // 16, len(dirs) % 16
    initial, threads = 0, []
    for i in range(size, len(dirs) + 1, size):
        if i == len(dirs) - remain:
            interval = (initial, i - 1 + remain)
        else:
            interval = (initial, i - 1)
        initial += size
        t = Thread(target=parallel, args=(interval, i))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    training_labels, training_images = shuffle(training_labels, training_images)
    training_images = np.asarray(training_images)
    training_labels = np.asarray(training_labels)

    testing_labels, testing_images = shuffle(testing_labels, testing_images)
    testing_images = np.asarray(testing_images)
    testing_labels = np.asarray(testing_labels)

    np.savez(treatment_dir + treated_dir + "kaggle_all_training_images", training_images)
    np.savez(treatment_dir + treated_dir + "kaggle_all_training_labels", training_labels)

    np.savez(treatment_dir + treated_dir + "kaggle_all_testing_images", testing_images)
    np.savez(treatment_dir + treated_dir + "kaggle_all_testing_labels", testing_labels)


get_symbols()

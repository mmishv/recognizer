import os
import numpy as np
from sklearn.utils import shuffle


def load_and_save_data(file_prefix, directory):
    path = os.path.join(directory, str(file_prefix))
    images = np.load(path + "_images.npz")["arr_0"]
    labels = np.load(path + "_labels.npz")["arr_0"]
    shuffled_images, shuffled_labels = shuffle(images, labels)
    np.savez(os.path.join(directory, "shuffled_" + str(file_prefix) + "_images.npz"), shuffled_images)
    np.savez(os.path.join(directory, "shuffled_" + str(file_prefix) + "_labels.npz"), shuffled_labels)


treatment_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
treated_dir = "treated_data/"

load_and_save_data("kaggle_all_training", os.path.join(treatment_dir, treated_dir))
load_and_save_data("kaggle_all_testing", os.path.join(treatment_dir, treated_dir))

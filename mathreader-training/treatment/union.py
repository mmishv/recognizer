# -*- coding: utf-8 -*-
import numpy as np
from sklearn.utils import shuffle

treatment_dir = "/home/user/PycharmProjects/mathreader/mathreader-training/treatment/"
treated_dir = "treated_data/"

path = treatment_dir + treated_dir

symbol = np.load(path + "kaggle_all_training_images.npz")
symbol = symbol["arr_0"]
symbol_labels = np.load(path + "kaggle_all_training_labels.npz")
symbol_labels = symbol_labels["arr_0"]

all_training_images = np.concatenate([symbol])
all_training_labels = np.concatenate([symbol_labels])
result_symbols, result_symbols_labels = shuffle(all_training_images, all_training_labels)

training_images = []
training_labels = []

for i in range(0, len(result_symbols)):
    training_images.append(result_symbols[i])
    training_labels.append(result_symbols_labels[i])

np.savez(path + "training_images_dataset", training_images)
np.savez(path + "training_labels_dataset", training_labels)


symbol_testing = np.load(path + "kaggle_all_testing_images.npz")
symbol_testing = symbol_testing["arr_0"]
symbol_testing_labels = np.load(path + "kaggle_all_testing_labels.npz")
symbol_testing_labels = symbol_testing_labels["arr_0"]

all_testing_images = np.concatenate([symbol_testing])
all_testing_labels = np.concatenate([symbol_testing_labels])

result_symbols_testing, result_symbols_testing_labels = shuffle(all_testing_images, all_testing_labels)

testing_images = []
testing_labels = []

for i in range(0, len(result_symbols_testing)):
    testing_images.append(result_symbols_testing[i])
    testing_labels.append(result_symbols_testing_labels[i])

np.savez(path + "testing_images_dataset", testing_images)
np.savez(path + "testing_labels_dataset", testing_labels)

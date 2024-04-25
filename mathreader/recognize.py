import cv2 as cv
import numpy as np
from tensorflow.keras.models import load_model

from mathreader import helpers
from mathreader.image_processing import postprocessing as postprocessing
from mathreader.image_processing import preprocessing as preprocessing

helpers_labels = helpers.get_labels()
labels = helpers_labels["labels_parser"]


class Recognize:
    def __init__(self, image):
        self.prediction = []
        self.image = None

        try:
            if isinstance(image, str):
                nparr = np.fromstring(image, np.uint8)
                img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            else:
                img = image.copy()
            self.image = img
        except Exception as e:
            print(e)

    @staticmethod
    def classification(img):
        img = img.reshape(1, 28, 28, 1)
        model = load_model(
            "/home/user/PycharmProjects/mathreader/mathreader-training/training/model/model_26-04-2024_03-54-57-BEST.h5"
        )
        prediction = model.predict(img)
        index = np.argmax(prediction)
        label_rec = helpers_labels["labels_parser"][str(index)]
        return {
            "label": helpers_labels["labels_recognition"][label_rec],
            "prediction": prediction,
            "type": "not-number",
        }

    def to_recognize(self):

        expression = {}

        helpers.debug(
            "[recognize.py] to_recognize | \
            Showing the image of the expression...\n"
        )

        helpers.debug(
            "[recognize.py] to_recognize | \
            Starting image preprocessing...\n"
        )
        p = preprocessing.ImagePreprocessing()
        segmentation, normalized_image = p.treatment(self.image)

        helpers.debug(
            "[recognize.py] to_recognize | \
            Showing preprocessed image\n"
        )

        helpers.debug(
            "[recognize.py] to_recognize | \
            Image preprocessing finished.\n"
        )

        helpers.debug(
            "[recognize.py] to_recognize | \
            Starting symbol classification...\n"
        )

        try:
            for s in segmentation:

                helpers.debug("... segmentation ...")
                helpers.debug("... recognize ...")

                reconhecer = self.classification(s["image"])
                reconhecer["label"] = str(reconhecer["label"])

                s["label"] = reconhecer["label"]
                s["prediction"] = reconhecer["prediction"]

                symbol_prediction = {"identity": labels[s["label"]]}

                symbol_prediction.update(reconhecer)
                self.prediction.append(symbol_prediction)

                helpers.debug(
                    "[recognize.py] to_recognize | \
                    Símbolo: %s "
                    % labels[s["label"]]
                )

            helpers.debug(
                "\n[recognize.py] to_recognize | \
                << Symbol classification finished.\n"
            )

        except Exception as e:
            print(e)

        pos = postprocessing.ImagePostprocessing(normalized_image)
        new = pos.segment_equality(segmentation)

        # teste
        for n in new:
            print("label: ", n["label"])

        expression["symbols"] = new

        return expression, normalized_image

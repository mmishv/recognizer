import cv2
import numpy as np
from recognizer import helpers


class ImagePreprocessing:
    def __init__(self, configs=None):
        self.image = None
        self.configs = {"black": False, "dilate": False, "dataset": False, "erode": False, "resize": "smaller"}
        if configs:
            self.configs.update(configs)

    @staticmethod
    def to_gray_denoise(image):
        if (img := image.copy()).ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return np.array(cv2.fastNlMeansDenoising(img, None, 5, 9))

    @staticmethod
    def invert(image):
        return 255 - image.copy()

    def binarization(self, image):
        img = self.invert(image.copy())
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        return self.invert(img)

    def normalize(self, image):
        img = self.to_gray_denoise(image)
        if not self.configs["black"]:
            img = self.invert(img)
        kernel = np.ones((2, 2), np.uint8)
        if "dilate" in self.configs and self.configs["dilate"]:
            img = cv2.dilate(img, kernel, iterations=2)
        if "erode" in self.configs and self.configs["erode"]:
            img = cv2.erode(img, kernel, iterations=1)
        return img

    @staticmethod
    def set_255_to_1(image):
        return image.copy() / 255

    def resize(self, image):
        old_size = image.shape[:2]
        height, width, ratio = old_size[0], old_size[1], float(26) / max(old_size)
        size_height, size_width = (size := tuple([int(x * ratio) for x in old_size]))
        size_height, size_width = size_height if size_height > 0 else 1, size_width if size_width > 0 else 1
        division_height, division_width = int(height / 2), int(width / 2)
        around_w, around_h, middle_height, middle_width = round(width * 20 / 100), round(height * 20 / 100), [], []
        for a in range(division_height - around_h, division_height + around_h):
            middle_height.append(image[a][division_width])
        for b in range(division_width - around_w, division_width + around_w):
            middle_width.append(image[division_height][division_width])
        if 15 >= size_width >= 20 and (any(i > 0.0000 for i in middle_height) or any(i > 0.0000 for i in middle_width)):
            new_size = tuple([int(10 if size_height > 10 else size_height), 26])
        else:
            if size_width / size_height >= 2:
                image = cv2.dilate(image, np.ones((2, 2), np.uint8), iterations=7)
                image = image[0:height, int(width * 5 / 100):int(width * 85 / 100)]
            new_size = size
        if self.configs["resize"] == "smaller":
            image = cv2.resize(image.copy(), (new_size[1], new_size[0]), interpolation=cv2.INTER_AREA)
        elif self.configs["resize"] == "bigger":
            image = cv2.resize(image.copy(), (new_size[1], new_size[0]), interpolation=cv2.INTER_LINEAR)
        delta_w, delta_h = 28 - new_size[1], 28 - new_size[0]
        top, bottom, left, right = delta_h // 2, delta_h - (delta_h // 2), delta_w // 2, delta_w - (delta_w // 2)
        return cv2.copyMakeBorder(image.copy(), top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    @staticmethod
    def resize_full(image):
        h, w = image.shape[:2]
        if w > 4000:
            width = int(w * 20 / 100)
            image = cv2.resize(image, (width, int(h * width / float(w))))
        return image

    def segment(self, img):
        image, symbols = img.copy(), []
        contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            if cv2.contourArea(contours[i]) < 10 or self.configs["dataset"] and len(contours) > 1:
                continue
            try:
                mask = np.zeros_like(image)
                cv2.drawContours(mask, contours, i, (255, 255, 255), -50)
                out = np.zeros_like(image)
                out[mask > 0] = image[mask > 0]
                x, y, w, h = cv2.boundingRect(contours[i])
                result_image = self.set_255_to_1(self.binarization(self.resize(out[y:y + h + 1, x:x + w + 1])))
                helpers.show_image(result_image)
                attributes = {"index": i, "image": result_image.copy(), "xmin": x, "xmax": x + w, "ymin": y,
                              "ymax": y + h, "w": w, "h": h, "centroid": [(x + (x + w)) / 2, (y + (y + h)) / 2]}
                symbols.append(attributes)
                self.image = image
            except BaseException:
                continue
        return symbols, self.image

    def treatment_segment(self, img):
        image = cv2.imread(img) if type(img) is str else img
        normalized = self.normalize(image)
        resized = self.resize(normalized)
        return self.set_255_to_1(resized)

    def treatment(self, img):
        image = self.resize_full(cv2.imread(img) if type(img) is str else img)
        normalized = self.normalize(image)
        self.image = normalized.copy()
        return self.segment(normalized)

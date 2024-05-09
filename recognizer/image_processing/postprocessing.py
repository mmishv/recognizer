from recognizer.image_processing import preprocessing as preprocessing


class ImagePostprocessing:
    def __init__(self, image):
        self.image = image

    def segment_equality(self, symbols):
        xmin_sorted,  c, i, candidate_index = sorted(symbols, key=lambda k: k["xmin"], reverse=False), 0, 0, 0
        for symbol in xmin_sorted:
            if c == 0 and symbol["label"] == "10":
                candidate, c, candidate_index = symbol.copy(), 1, i
            elif c == 1 and symbol["label"] == "10":
                diff = abs(candidate["w"] / symbol["w"])
                line1x = range(candidate["xmin"], candidate["xmax"] + 1)
                line2x = range(symbol["xmin"], symbol["xmax"] + 1)
                len_line1x, len_line2x = len(line1x), len(line2x)
                x_set = set(line1x) if len_line1x < len_line2x else set(line2x)
                x_intersection = x_set.intersection(line1x if len_line1x >= len_line2x else line2x)
                if x_intersection and 2 >= diff >= 0.5:
                    abacate, c = self.image.copy(), 0
                    ymin, ymax = min(symbol["ymin"], candidate["ymin"]), max(symbol["ymax"], candidate["ymax"])
                    xmin, xmax = min(symbol["xmin"], candidate["xmin"]), max(symbol["xmax"], candidate["xmax"])
                    pre = preprocessing.ImagePreprocessing()
                    resized = pre.set_255_to_1(pre.binarization(pre.resize(abacate[ymin: ymax + 1, xmin: xmax + 1])))
                    symbol["image"] = resized
                    symbol["label"] = "30"
                    symbol["xmin"] = xmin
                    symbol["xmax"] = xmax
                    symbol["ymin"] = ymin
                    symbol["ymax"] = ymax
                    symbol["w"] = xmax - xmin
                    symbol["h"] = ymax - ymin
                    symbol["centroid"] = [xmin + (xmax - xmin) / 2, ymin + (ymax - ymin) / 2]
                    del xmin_sorted[candidate_index]
                else:
                    candidate = symbol.copy()
                    candidate_index = i
            i += 1
        return xmin_sorted

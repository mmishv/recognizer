import base64

import cv2
import numpy as np

from recognizer.parser import parser
from recognizer.recognize import Recognize


class HMERecognizer:
    def __init__(self):
        self.expression_after_parser = None
        self.expression_after_recognition = None
        self.predictions = None
        self.configurations = None
        self.processed_image = None
        self.parsed_expression = None
        self.image = None
        self.expression_after_grammar = ""
        self.parser_tree = None
        self.parser_list = None
        self.lex_errors_history = None
        self.lex_pure_errors = None

    def __parse(self, expression):
        parse = parser.Parser(expression)
        parsed_data = parse.parse()
        if not parsed_data:
            return
        self.lex_errors_history = parsed_data["lex_errors_history"]
        self.lex_pure_errors = parsed_data["lex_pure_errors"]
        self.latex_string_original = parsed_data["latex_string_original"]
        self.expression_after_parser = parsed_data["latex_before_cg"]
        self.expression_after_grammar = parsed_data["latex"]
        self.parser_tree = parsed_data["tree"]
        self.parser_list = parsed_data["tlist"]
        return parsed_data["latex_string"]

    def load_image(self, image, data_type="base64"):
        try:
            if data_type == "base64":
                im_bytes = base64.b64decode(image)
                im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
                img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            elif data_type == "path":
                img = cv2.imread(image, 0)
            elif data_type == "byte":
                im_arr = np.frombuffer(image, dtype=np.uint8)
                img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            else:
                raise Exception("Wrong file format")
            self.image = img
        except BaseException as e:
            self.image = None
            raise e

    def recognize(self):
        img = self.image
        if isinstance(img, np.ndarray) and len(img) > 0:
            hme = Recognize(img)
            expression, image = hme.to_recognize()
            self.expression_after_recognition = expression.copy()
            self.predictions = hme.prediction
            parsed_expression = self.__parse(expression)
            self.parsed_expression = parsed_expression
            self.processed_image = image
            return parsed_expression, image

    def get_lex_errors(self):
        return self.lex_errors_history

    def get_lex_pure_errors(self):
        return self.lex_pure_errors

    def get_latex_string_original(self):
        return self.latex_string_original

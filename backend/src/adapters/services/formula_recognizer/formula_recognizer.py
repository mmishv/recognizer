import logging
import os
import sys

from core.exceptions.recognizer_exceptions import GrammarException
from ports.services.formula_recognizer.formula_recognizer import IFormulaRecognizer

# temporary as recognizer is not library but module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')))
from recognizer.hme_recognizer import HMERecognizer
from recognizer.helpers.exceptions import GrammarError, LexicalError


logger = logging.getLogger()


class FormulaRecognizer(IFormulaRecognizer):
    def __init__(self):
        self.recognizer = HMERecognizer()

    def recognize_hme_formula(self, image64: str) -> str:
        self.recognizer.load_image(image64, data_type="base64")
        try:
            expression, img = self.recognizer.recognize()
        except GrammarError as e:
            logger.error(f"Image validation error: grammar error {self.recognizer.get_lex_errors()}")
            raise GrammarException
        except LexicalError as e:
            logger.error(f"Image validation error: lexical error {self.recognizer.get_lex_errors()}")
            raise LexicalError
        return expression

import base64

from ports.services.formula_recognizer.formula_recognizer import IFormulaRecognizer
from ports.services.latex_visualizer.latex_visualizer import ILatexVisualizer


class RecognizeHMEFormulaUseCase:
    def __init__(self, recognizer: IFormulaRecognizer, visualizer: ILatexVisualizer):
        self.recognizer = recognizer
        self.visualizer = visualizer

    def __call__(self, image: bytes) -> tuple[str, str]:
        image64 = base64.b64encode(image).decode('utf-8')
        expression = self.recognizer.recognize_hme_formula(image64)
        image64 = self.visualizer.visualize(expression)
        return expression, image64




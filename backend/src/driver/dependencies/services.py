from adapters.services.formula_recognizer.formula_recognizer import FormulaRecognizer
from adapters.services.latex_visualizer.latex_visualizer import LatexVisualizer
from ports.services.formula_recognizer.formula_recognizer import IFormulaRecognizer
from ports.services.latex_visualizer.latex_visualizer import ILatexVisualizer


def get_latex_visualizer() -> ILatexVisualizer:
    return LatexVisualizer()


def get_formula_recognizer() -> IFormulaRecognizer:
    return FormulaRecognizer()

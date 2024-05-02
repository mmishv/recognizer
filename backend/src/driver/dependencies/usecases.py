from typing import Annotated

from fastapi import Depends

from ports.services.formula_recognizer.formula_recognizer import IFormulaRecognizer
from ports.services.latex_visualizer.latex_visualizer import ILatexVisualizer
from driver.dependencies.services import get_latex_visualizer, get_formula_recognizer
from use_cases.recognize_hme_formula_use_case import RecognizeHMEFormulaUseCase


def get_recognize_hme_formula_use_case(
    visualizer: Annotated[ILatexVisualizer, Depends(get_latex_visualizer)],
    recognizer: Annotated[IFormulaRecognizer, Depends(get_formula_recognizer)]
) -> RecognizeHMEFormulaUseCase:
    return RecognizeHMEFormulaUseCase(recognizer, visualizer)



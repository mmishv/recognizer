from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends

from driver.app import app
from driver.dependencies.usecases import get_recognize_hme_formula_use_case
from driver.v1.schema import RecognizerResponse
from use_cases.recognize_hme_formula_use_case import RecognizeHMEFormulaUseCase

router = APIRouter(prefix="/v1/recognizer", tags=["Recognizer"])


@router.post("/", response_model=RecognizerResponse)
async def recognize(
    image: UploadFile,
    use_case: Annotated[RecognizeHMEFormulaUseCase, Depends(get_recognize_hme_formula_use_case)]
):
    image = await image.read()
    expression, img = use_case(image)
    return RecognizerResponse.from_entity(expression=expression, image=img)


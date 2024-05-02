from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions.recognizer_exceptions import GrammarException, LexicalException


async def recognizer_grammar_exception_handler(request: Request, exc: GrammarException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={f"detail": exc}
    )


async def recognizer_lex_exception_handler(request: Request, exc: LexicalException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={f"detail": exc}
    )

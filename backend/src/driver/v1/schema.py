from pydantic import BaseModel


class RecognizerResponse(BaseModel):
    expression: str
    image: str

    @classmethod
    def from_entity(cls, image: str, expression: str) -> 'RecognizerResponse':
        return cls(
            expression=expression,
            image=image,
        )

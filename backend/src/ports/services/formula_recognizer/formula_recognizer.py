from abc import ABC, abstractmethod


class IFormulaRecognizer(ABC):
    @abstractmethod
    def recognize_hme_formula(self, image64: str) -> str:
        pass

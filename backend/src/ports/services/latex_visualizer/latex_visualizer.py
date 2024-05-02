from abc import ABC, abstractmethod


class ILatexVisualizer(ABC):
    @abstractmethod
    def visualize(self, expression: str) -> str:
        pass

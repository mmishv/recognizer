import base64
from io import BytesIO
from matplotlib import pyplot as plt

from ports.services.latex_visualizer.latex_visualizer import ILatexVisualizer


class LatexVisualizer(ILatexVisualizer):

    def visualize(self, expression: str) -> str:
        plt.text(0.5, 0.5, f"${expression}$", fontsize=50, horizontalalignment="center", verticalalignment="center")
        plt.axis("off")
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format="png")
        plt.clf()
        img_buffer.seek(0)
        img_bytes = img_buffer.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        return img_base64

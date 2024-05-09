from matplotlib import pyplot as plt


from recognizer.helpers.exceptions import GrammarError, LexicalError
import recognizer
from recognizer.hme_recognizer import HMERecognizer


class Example:
    def __init__(self):
        expression = ""
        hme_recognizer = HMERecognizer()
        #  9, 79, 37b - not solve (
        images = [recognizer.__path__[0] + "/images/58.png"]
        for image in images:
            try:
                hme_recognizer.load_image(image, data_type="path")
                expression, img = hme_recognizer.recognize()
                lex_errors = hme_recognizer.get_lex_errors()
                pure_lex_errors = hme_recognizer.get_lex_pure_errors()
                latex_string_original = hme_recognizer.get_latex_string_original()
                print("\nLex errors: ", lex_errors)
                print("\nPure Lex Errors:", pure_lex_errors)
                print("\nOriginal Expression: ", latex_string_original)
            except (GrammarError, LexicalError) as e:
                if "latex_string_original" in e.data:
                    expression = e.data["latex_string_original"]
                print(e)
            print("\nExpression: ", expression)
            plt.text(0.5, 0.5, f"${expression}$", fontsize=12, horizontalalignment="center", verticalalignment="center")
            plt.axis("off")
            plt.show()


Example()

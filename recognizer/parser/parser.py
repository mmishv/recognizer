from recognizer.parser import check_grammar as cg
from recognizer.parser import structural_analysis as sa


class Parser:
    def __init__(self, expression):
        self.symbols = expression['symbols']

    @staticmethod
    def __remove_contains(tstring):
        if isinstance(tstring, str):
            tstring = tstring.replace('contains', '')
        elif isinstance(tstring, list) and "contains" in tstring:
            tstring = tstring.remove('contains')
        return tstring

    def organize_latex_data(self, tstring):
        latex = []
        latex_list = []
        for symbol in tstring:
            if symbol['label'] != '' and symbol['label'] != 'contains':
                latex.append(symbol)
                latex_list.append(symbol['label'])
        latex_string = " ".join(latex_list)
        latex_string = self.__remove_contains(latex_string)
        return {
            'latex': latex,
            'latex_list': latex_list,
            'latex_string': latex_string,
            'lstring': latex_string
        }

    def parse(self):
        structural_analysis = sa.StructuralAnalysis(self.symbols)
        structured_data = structural_analysis.analyze()
        if not structured_data:
            return
        latex_data = self.organize_latex_data(structured_data['latex'])
        check_grammar = cg.CheckGrammar()
        check_grammar_data = check_grammar.check(latex_data)
        data = {}
        data.update(check_grammar_data)
        data.update({'latex_before_cg': structured_data['latex']})
        data.update({
            'tree': structured_data['tree'],
            'tlist': structured_data['tlist']
        })
        return data

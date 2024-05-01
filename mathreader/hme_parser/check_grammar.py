from mathreader.hme_parser import check_grammar_lex as check_grammar_lex
from mathreader.hme_parser import check_grammar_yacc as check_grammar_yacc
from mathreader.helpers.exceptions import GrammarError, LexicalError, CustomSyntaxError


class CheckGrammar:

    def __init__(self):
        self.__attempts_lex = 0
        self.__attempts_grammar = 0

    def check(self, latex_data):
        latex = latex_data['latex']
        latex_list = latex_data['latex_list']
        latex_string = latex_data['latex_string']
        try:
            check_lex_data = self.__check_lex(latex_string, latex, latex_list)
            check_yacc_data = self.__check_yacc(check_lex_data)
            check_yacc_data.update({'latex_string_original': latex_string})
            return check_yacc_data
        except (GrammarError, CustomSyntaxError, LexicalError) as ex:
            ex.data.update({'latex_string_original': latex_string})
            raise ex

    def __check_lex(self, latex_string, latex, latex_list):
        cgl = check_grammar_lex.CheckLex()
        cgl.latex_string = latex_string
        cgl.latex = latex
        cgl.latex_list = latex_list
        cgl.attempts = self.__attempts_lex
        check_lex_data = cgl.check_correct_lex()
        return check_lex_data

    def __check_yacc(self, check_lex_data=None):
        cgs = check_grammar_yacc.CheckSyntax()
        cgs.attempts = self.__attempts_grammar
        if check_lex_data:
            cgs.set_lex_data(check_lex_data)
        check_data_yacc = cgs.check_correct_grammar()
        return check_data_yacc

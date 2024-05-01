from copy import copy

from mathreader.hme_parser.grammar import yacc as yacc
from mathreader.hme_parser import check_grammar_lex as check_grammar_lex
from mathreader.helpers.exceptions import GrammarError


class CheckSyntax:

    def __init__(self):
        self.__first_error = True
        self.latex_string = ""
        self.latex = ""
        self.latex_list = ""
        self.attempts = 0
        self.index = 0
        self.lex_errors_history = []
        self.yacc_errors_history = []
        self.yacc_error_list = None
        self.lex_error_list = None
        self.pure_yacc_errors = []
        self.pure_lex_errors = []

    def set_lex_data(self, check_lex_data):
        self.latex = check_lex_data['latex']
        self.latex_list = check_lex_data['latex_list']
        self.latex_string = check_lex_data['latex_string']
        self.lex_errors_history = check_lex_data['errors_history']
        self.pure_lex_errors = check_lex_data['pure_errors']

    def __locate_grammar_error(self, yacc_error_list):
        yacc_error_list = copy(yacc_error_list)
        latex = copy(self.latex)
        yacc_errors = []
        yacc_errors_history = self.yacc_errors_history.copy()
        for error in yacc_error_list:
            if error['value'] is not None:
                count = 0
                count_list = 0
                latex_error_pos = error['lexpos']
                latex_error_token = error['value']
                for symbol in latex:
                    if symbol['label'] == latex_error_token and \
                            count == latex_error_pos:
                        yacc_errors.append({
                            'pos': latex_error_pos,
                            'pos_list': count_list,
                            'label': symbol['label'],
                            'prediction': symbol['prediction'],
                            'attempts': [symbol['label']]
                        })
                        yacc_errors_history.extend(yacc_errors)
                        break
                    count += len(symbol['label'])
                    count_list += 1
            else:
                continue
        return yacc_errors, yacc_errors_history

    def check_correct_grammar(self):
        if not self.yacc_error_list and \
                self.__first_error and \
                self.attempts < 3 and \
                self.latex_string:
            yacc_error_list = yacc.latex_parse(self.latex_string)
            if yacc_error_list:
                yacc_errors = self.__process_yacc_errors(yacc_error_list)
                self.__first_error = False
                self.__process_error(yacc_errors)
        elif self.yacc_error_list and \
                not self.__first_error and \
                self.attempts < 3 and \
                self.latex_string:
            self.__find_lexical_errors()
            second_yacc_error_list = yacc.latex_parse(self.latex_string)
            if second_yacc_error_list:
                yacc_errors = self.__process_yacc_errors(second_yacc_error_list)
                self.__process_error(yacc_errors)

        elif (self.yacc_error_list and self.attempts >= 3) or \
                not self.latex_string:
            raise GrammarError({
                'latex': self.latex,
                'latex_list': self.latex_list,
                'latex_string': self.latex_string,
                'error': self.yacc_error_list,
                'errors_history': self.yacc_errors_history,
                'pure_errors': self.pure_yacc_errors
            })
        return {
            'latex': self.latex,
            'latex_list': self.latex_list,
            'latex_string': self.latex_string,
            'yacc_errors_history': self.yacc_errors_history,
            'lex_errors_history': self.lex_errors_history,
            'yacc_pure_errors': self.pure_yacc_errors,
            'lex_pure_errors': self.pure_lex_errors
        }

    def __process_yacc_errors(self, yacc_error_list):
        self.pure_yacc_errors.extend(yacc_error_list)
        if yacc_error_list[0]['lexpos'] is None:
            yacc_error_list[0].update({
                'lexpos': len(self.latex_string) - 1
            })
            yacc_error_list[0].update({
                'value': self.latex_string[-1]
            })
        yacc_errors, yacc_errors_history = self.__locate_grammar_error(yacc_error_list)
        self.yacc_error_list = yacc_errors
        self.yacc_errors_history = yacc_errors_history
        return yacc_errors

    def __find_lexical_errors(self):
        cgl = check_grammar_lex.CheckLex()
        cgl.latex_string = self.latex_string
        cgl.latex = self.latex
        cgl.latex_list = self.latex_list
        cgl.attempts = 0
        check_lex_data = cgl.check_correct_lex()
        self.latex = check_lex_data['latex']
        self.latex_list = check_lex_data['latex_list']
        self.latex_string = check_lex_data['latex_string']
        self.pure_lex_errors = check_lex_data['pure_errors']
        lex_errors_history = check_lex_data['errors_history']
        self.lex_errors_history.extend(lex_errors_history)

    def __process_error(self, yacc_errors):
        self.yacc_error_list = yacc_errors
        if self.yacc_error_list:
            self.yacc_errors_history = copy(self.yacc_error_list)
        self.attempts += 1
        return self.check_correct_grammar()

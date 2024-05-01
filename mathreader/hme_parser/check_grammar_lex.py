from copy import copy

from mathreader.hme_parser import correct_grammar
from mathreader.hme_parser.grammar import lex as lex
from mathreader.helpers.exceptions import LexicalError


class CheckLex:

    def __init__(self):
        self.__first_error = True
        self.latex_string = ""
        self.latex = ""
        self.latex_list = ""
        self.attempts = 0
        self.lex_error_list = None
        self.index = 0
        self.lex_errors_history = []
        self.pure_lex_errors = []

    def __locate_lex_error(self, lex_error_list):
        error_list = copy(lex_error_list)
        latex = copy(self.latex)
        lex_errors = []
        lex_errors_history = self.lex_errors_history.copy()
        for error in error_list:
            if isinstance(error, dict):
                error = error['label'], error['pos']
            if error[1] != -1:
                count = 0
                count_list = 0
                latex_error_pos = error[1]
                latex_error_token = error[0]
                for symbol in latex:
                    if symbol['label'] != latex_error_token:
                        count += len(symbol['label'])
                        count_list += 1
                    elif count == latex_error_pos:
                        lex_errors.append({
                            'pos': latex_error_pos,
                            'pos_list': count_list,
                            'label': symbol['label'],
                            'prediction': symbol['prediction'],
                            'attempts': [symbol['label']]
                        })
                        lex_errors_history.extend(lex_errors)
                        break
            else:
                continue
        return lex_errors, lex_errors_history

    def check_correct_lex(self):
        if not self.lex_error_list and \
                self.__first_error and \
                self.attempts < 3 and \
                self.latex_string:
            lex_error_list = lex.latex_lexer(self.latex_string)
            if lex_error_list:
                self.pure_lex_errors.extend(lex_error_list)
                lex_errors, lex_errors_history = self.__locate_lex_error(lex_error_list)
                self.lex_error_list = lex_errors
                self.lex_errors_history = lex_errors_history
                self.__first_error = False
                self.__attempt_to_fix_error(lex_errors)
        elif self.lex_error_list and \
                not self.__first_error and \
                self.attempts < 3 and \
                self.latex_string:
            second_lex_error_list = lex.latex_lexer(self.latex_string)
            if second_lex_error_list:
                self.pure_lex_errors.extend(second_lex_error_list)
                if second_lex_error_list[0][1] == -1:
                    second_lex_error_list.reverse()
                    second_lex_error_list.pop()
                    second_lex_error_list.reverse()
                lex_errors, lex_errors_history = self.__locate_lex_error(second_lex_error_list)
                self.lex_error_list = lex_errors
                self.lex_errors_history = lex_errors_history
                self.__attempt_to_fix_error(lex_errors)
        elif (self.lex_error_list and self.attempts >= 3) or \
                not self.latex_string:
            raise LexicalError({
                'latex': self.latex,
                'latex_list': self.latex_list,
                'latex_string': self.latex_string,
                'error': self.lex_error_list,
                'errors_history': self.lex_errors_history,
                'pure_errors': self.pure_lex_errors
            })
        return {
            'latex': self.latex,
            'latex_list': self.latex_list,
            'latex_string': self.latex_string,
            'errors_history': self.lex_errors_history,
            'pure_errors': self.pure_lex_errors
        }

    def __attempt_to_fix_error(self, lex_errors):
        bg = correct_grammar.CorrectGrammar()
        corrected_data = bg.correct_grammar_lex(lex_errors, self.latex,
                                                self.latex_list, 0,
                                                self.lex_errors_history)
        update_latex_string = corrected_data['latex_string']
        self.lex_error_list = corrected_data['errors']
        self.index = corrected_data['index']
        if self.lex_error_list:
            self.lex_errors_history = copy(self.lex_error_list)
        self.latex_string = update_latex_string
        self.attempts += 1
        return self.check_correct_lex()

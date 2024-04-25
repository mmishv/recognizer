import numpy as np
from mathreader import helpers
from mathreader.hme_parser.grammar import lex as lex
from mathreader.hme_parser.grammar import yacc as yacc

helpers_labels = helpers.get_labels()
labels = helpers_labels['labels_parser']


class CorrectGrammar():

    def __init__(self):
        pass

    def correct_grammar_lex(self, errors, latex, latex_list, index=0,
                            previous_errors=None):
        if previous_errors is None:
            previous_errors = []
        latex_string = ""
        previous_attemptions = []

        # It adds previous attempts to the array
        for error in previous_errors:
            if error['attempts'] and len(error['attempts']) > 0:
                previous_attemptions.extend(error['attempts'])
        if len(errors) > 0:

            pos = errors[index]['pos']
            pos_list = errors[index]['pos_list']
            pred = errors[index]['prediction'].copy()
            subst = helpers.subst
            # When there's predictions it is a numpy array, not a list.
            if not isinstance(pred, list):
                json_label = 'labels_parser'

                def get_new_index(pred):

                    new_pred = pred.copy()
                    new_pred[0][np.argmax(pred)] = 0
                    new_index = np.argmax(new_pred)
                    return new_index, new_pred

                def recur_get_new_index(pred):
                    new_index, pred = get_new_index(pred)
                    label_recog = helpers_labels[json_label][str(new_index)]
                    new_label = helpers_labels["labels_recognition"][label_recog]
                    new_identification = labels[new_label]
                    if new_identification in errors[index]['attempts'] or \
                            new_identification in previous_attemptions:
                        return recur_get_new_index(pred)
                    else:
                        if new_identification == '{':
                            new_identification = '\\{'
                        if new_identification == '}':
                            new_identification = '\\}'

                        return new_index, pred, new_identification

                new_index, new_pred, new_identification = recur_get_new_index(pred)
                errors[index]['prediction'] = new_pred
                errors[index]['attempts'].append(new_identification)
                # Make it more 'Pythonic' later
                if new_identification in subst:
                    # list of substitutions
                    substitution_list = subst[new_identification]
                    for substitution_index in range(0, len(substitution_list)):
                        for substitution in substitution_list[substitution_index]:
                            if new_identification == substitution:
                                new_identification = substitution_list[substitution_index][substitution]
                latex_list[pos_list] = new_identification
                latex[pos_list]['label'] = new_identification
                latex[pos_list]['prediction'] = new_pred
                latex_string = latex_string.join(latex_list)
        return {
            'latex_string': latex_string or "".join(latex_list),
            'errors': errors,
            'index': index
        }

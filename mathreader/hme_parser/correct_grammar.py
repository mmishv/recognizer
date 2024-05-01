import numpy as np
from mathreader import helpers

helpers_labels = helpers.get_labels()
labels = helpers_labels['labels_parser']


class CorrectGrammar:

    def __init__(self):
        pass

    @staticmethod
    def correct_grammar_lex(errors, latex, latex_list, index=0,
                            previous_errors=None):
        if previous_errors is None:
            previous_errors = []
        latex_string = ""
        previous_attempts = []
        for error in previous_errors:
            if error['attempts'] and len(error['attempts']) > 0:
                previous_attempts.extend(error['attempts'])
        if len(errors) > 0:
            pos_list = errors[index]['pos_list']
            pred = errors[index]['prediction'].copy()
            subst = helpers.subst
            if not isinstance(pred, list):
                json_label = 'labels_parser'

                def get_new_index(last):
                    new_last = last.copy()
                    new_last[0][np.argmax(last)] = 0
                    new_idx = np.argmax(new_last)
                    return new_idx, new_last

                def get_new_index_recursive(last):
                    new_idx, last = get_new_index(last)
                    label_rec = helpers_labels[json_label][str(new_idx)]
                    new_label = helpers_labels["labels_recognition"][label_rec]
                    new_ident = labels[new_label]
                    if new_ident in errors[index]['attempts'] or \
                            new_ident in previous_attempts:
                        return get_new_index_recursive(last)
                    else:
                        if new_ident == '{':
                            new_ident = '\\{'
                        if new_ident == '}':
                            new_ident = '\\}'
                        return new_idx, last, new_ident

                new_index, new_pred, new_identification = get_new_index_recursive(pred)
                errors[index]['prediction'] = new_pred
                errors[index]['attempts'].append(new_identification)
                if new_identification in subst:
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

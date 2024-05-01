import re

from mathreader import helpers
from mathreader.helpers import data_structures as DS

helpers_labels = helpers.get_labels()
labels = helpers_labels["labels_parser"]


class StructuralAnalysis:
    def __init__(self, symbol_list):
        self.symbols = symbol_list

    def analyze(self):
        tree = self.__main_parsing(self.__preprocessing(self.symbols))
        if not tree:
            return
        tlist = self.__tree_to_list(tree)
        latex = self.__list_to_latex_obj(tlist)
        return {"latex": latex, "tree": tree, "tlist": tlist}

    @staticmethod
    def __preprocessing(symbols):
        symbols = sorted(symbols, key=lambda i: i["xmin"])
        for i in range(0, len(symbols)):
            s = symbols[i]
            s["centroid"] = list(s["centroid"])
            s["checked"] = False
            if s["label"] in ["11", "13", "15"]:
                s["type"] = "Open"
            elif s["label"] in ["12", "14", "16"]:
                s["type"] = "Close"
            else:
                s["type"] = "Normal"
            if (
                    re.search("^[0-9]$", str(s["label"]))
                    or s["label"] == "19"
                    or s["label"] == "23"
                    or s["type"] == "Open"
                    or s["type"] == "Close"
            ):
                s["centroid_class"] = "Ascending"
                s["centroid"][1] = s["ymin"] + (2 / 3) * (s["h"])  # 3/5
            elif s["label"] == "25":
                s["centroid_class"] = "Descending"
                s["centroid"][1] = s["ymin"] + (1 / 3) * s["h"]
            else:
                s["centroid_class"] = "Centred"
                s["centroid"][1] = s["ymin"] + ((s["h"]) / 2)
            s["wall"] = {}
            s["wall"]["top"] = -1
            s["wall"]["bottom"] = 9999999999999
            s["wall"]["left"] = -1
            s["wall"]["right"] = 9999999999999
        return symbols

    def __main_parsing(self, symbols):
        list_in, tree, queue, stack = symbols, DS.Tree(), DS.Queue(), DS.Stack()
        r = [[0, 0], [9999999999, 9999999999]]
        if (start := self.__sp(list_in, r)) == -1:
            return
        queue.enqueue(start)
        queue.enqueue(tree.root_node)
        list_in[start]["checked"] = True
        while not queue.is_empty():
            while not queue.is_empty():
                temp1, parent_node = queue.dequeue(), queue.dequeue()
                symbol_node = DS.SymbolNode(list_in[temp1])
                tree.insert(symbol_node, parent_node, "Node")
                stack.push(temp1)
                stack.push(symbol_node)
                temp2 = self.__hor(list_in, temp1)
                while temp2 != -1:
                    list_in[temp2]["checked"] = True
                    list_in[temp2]["wall"] = list_in[temp1]["wall"].copy()
                    symbol_node = DS.SymbolNode(list_in[temp2])
                    tree.insert(symbol_node, parent_node, "Node")
                    stack.push(temp2)
                    stack.push(symbol_node)
                    list_in[temp1]["wall"]["right"] = list_in[temp2]["xmin"]
                    temp1 = temp2
                    temp2 = self.__hor(list_in, temp1)
            stack.push("EOBL")
            while not stack.is_empty():
                if stack.peek() == "EOBL":
                    stack.pop()
                symbol_node, temp1 = stack.pop(), stack.pop()
                label = int(list_in[temp1]["label"])
                upper_threshold = list_in[temp1]["ymin"] + ((1 / 6.5) * list_in[temp1]["h"])
                lower_threshold = list_in[temp1]["ymin"] + ((5.5 / 6.5) * list_in[temp1]["h"])
                left_threshold = (
                    (list_in[temp1]["xmin"] + ((1 / 6) * list_in[temp1]["w"])) if label != 10 else list_in[temp1][
                        "xmin"]
                )
                right_threshold = (
                    (list_in[temp1]["xmax"] - ((1 / 6) * list_in[temp1]["w"])) if label != 10 else list_in[temp1][
                        "xmax"]
                )
                r = [
                    {"above": [[left_threshold, list_in[temp1]["wall"]["top"]], [right_threshold, upper_threshold]]},
                    {"below": [[left_threshold, lower_threshold], [right_threshold, list_in[temp1]["wall"]["bottom"]]]},
                ]

                def check():
                    temp2 = self.__start(list_in, reg)
                    if temp2 != -1:
                        if not list_in[temp2]["checked"]:
                            list_in[temp2]["checked"] = True
                            list_in[temp2]["wall"]["left"] = reg[0][0]
                            list_in[temp2]["wall"]["right"] = reg[1][0]
                            list_in[temp2]["wall"]["top"] = reg[0][1]
                            list_in[temp2]["wall"]["bottom"] = reg[1][1]
                            relation_node = DS.RegionNode(list(region.keys())[0])
                            tree.insert(relation_node, symbol_node, "Node")
                            queue.enqueue(temp2)
                            queue.enqueue(relation_node)

                for region in r:
                    reg = region[list(region.keys())[0]]
                    region_name = list(region.keys())[0]
                    operators = bool(label in range(11, 17) or label in range(27, 31) or label == 17 or label == 23)
                    if (region_name == "above" and not operators) or (region_name == "below" and not operators):
                        check()
                r = [
                    {
                        "contains": [
                            [list_in[temp1]["xmin"], list_in[temp1]["ymin"]],
                            [list_in[temp1]["xmax"], list_in[temp1]["ymax"]],
                        ]
                    },
                    {
                        "super": [
                            [right_threshold, list_in[temp1]["wall"]["top"]],
                            [list_in[temp1]["wall"]["right"], upper_threshold],
                        ]
                    },
                    {
                        "subsc": [
                            [right_threshold, lower_threshold],
                            [list_in[temp1]["wall"]["right"], list_in[temp1]["wall"]["bottom"]],
                        ]
                    },
                ]
                for region in r:
                    reg = region[list(region.keys())[0]]
                    region_name = list(region.keys())[0]
                    operators = bool(label == 10 or label in range(27, 31) or label == 17)
                    if (
                            (region_name == "super" and not operators)
                            or (region_name == "subsc" and not operators)
                            or (region_name == "contains" and int(list_in[temp1]["label"]) == 23)
                    ):
                        check()
        return tree

    @staticmethod
    def __overlap(symbol_index, top, bottom, list_in):
        list_index, stop, n, main_line = symbol_index, False, len(list_in), -1
        if list_in[symbol_index]["label"] == "10":
            max_length = list_in[symbol_index]["xmax"] - list_in[symbol_index]["xmin"]
        else:
            max_length = -1
        while list_index > 0 and not stop:
            if list_in[list_index - 1]["xmin"] <= list_in[symbol_index]["xmin"]:
                list_index -= 1
            else:
                stop = True
        line1x = range(list_in[symbol_index]["xmin"], list_in[symbol_index]["xmax"] + 1)
        len_line1x = len(line1x)
        while list_index < n and list_in[list_index]["xmin"] < list_in[symbol_index]["xmax"]:
            line2x = range(list_in[list_index]["xmin"], list_in[list_index]["xmax"] + 1)
            len_line2x = len(line2x)
            x_set = set(line1x) if len_line1x < len_line2x else set(line2x)
            x_intersection = x_set.intersection(line1x if len_line1x >= len_line2x else line2x)
            min_line = min(len_line1x, len_line2x)
            if (
                    not list_in[list_index]["checked"]
                    and list_in[list_index]["label"] == "10"
                    and top <= list_in[list_index]["centroid"][1] <= bottom
                    and list_in[list_index]["xmin"] <= (list_in[symbol_index]["xmin"] + 8)
                    and len(x_intersection) > (min_line / 2)
                    and (list_in[list_index]["xmax"] - list_in[list_index]["xmin"]) > max_length
            ):
                max_length = list_in[list_index]["xmax"] - list_in[list_index]["xmin"]
                main_line = list_index
            list_index += 1
        if main_line == -1:
            return symbol_index
        else:
            return main_line

    def __start(self, list_in, r):
        left, top, right, bottom = r[0][0], r[0][1], r[1][0], r[1][1]
        leftmost_index, list_index, n = -1, 0, len(list_in)
        while leftmost_index == -1 and list_index < n:
            if (
                    not list_in[list_index]["checked"]
                    and list_in[list_index]["centroid"][0] >= left
                    and list_in[list_index]["centroid"][1] >= top
                    and list_in[list_index]["centroid"][0] <= right
                    and list_in[list_index]["centroid"][1] <= bottom
            ):
                leftmost_index = list_index
            else:
                list_index = list_index + 1
        if leftmost_index == -1:
            return leftmost_index
        else:
            return self.__overlap(leftmost_index, top, bottom, list_in)

    def __sp(self, list_in, r):
        return self.__start(list_in, r)

    def __hor(self, list_in, index):
        stop, a, label = False, -1, int(list_in[index]["label"])
        right, left = list_in[index]["wall"]["right"], list_in[index]["xmin"]
        top = list_in[index]["ymin"] + (list_in[index]["h"] * (1 / 6.5))
        bottom = list_in[index]["ymin"] + (list_in[index]["h"] * (5.5 / 6.5))
        if label == 10 or label in [27, 28, 29, 30]:
            top, bottom = list_in[index]["wall"]["top"], list_in[index]["wall"]["bottom"]
        if label == 23:
            left = list_in[index]["xmax"]
        if label in range(10, 17):
            r = [[list_in[index]["xmax"], top], [right, bottom]]
            a, stop = self.__start(list_in, r), True
        else:
            for s in range(0, len(list_in)):
                if not list_in[s]["checked"]:
                    symbol = list_in[s]
                    if left <= symbol["centroid"][0] <= right and bottom >= symbol["centroid"][1] >= top:
                        a, stop = s, True
                        break
        if stop and a != -1:
            return self.__overlap(a, list_in[a]["wall"]["top"], list_in[a]["wall"]["bottom"], list_in)
        else:
            return -1

    @staticmethod
    def __tree_to_list(tree, node=None):
        latex = []

        def recursive_to_list(root_node):
            current = tree.root_node if not root_node else root_node
            if current is None:
                return
            if isinstance(current.data, str):
                latex.append(current.data)
            else:
                real_label = labels[current.data["label"]]
                if real_label == "{":
                    real_label = "\\{"
                if real_label == "}":
                    real_label = "\\}"
                current.data["label"] = real_label
                latex.append(current.data)
            if current.node_type == "RegionNode":
                latex.append("{")
            for n in current.children:
                recursive_to_list(n)
            if current.node_type == "RegionNode":
                latex.append("}")

        recursive_to_list(node)
        if latex[0] == "Expression":
            latex.remove("Expression")
            if latex[-1] == "}":
                latex.pop()
            if latex[0] == "{":
                latex.reverse()
                latex.pop()
                latex.reverse()
        return latex

    def __list_to_latex_obj(self, tlist):
        latex = []
        for symbol in tlist:
            if isinstance(symbol, dict):
                latex.append(
                    {
                        "label": symbol["label"],
                        "prediction": symbol["prediction"] if "prediction" in symbol else [],
                        "type": symbol["type"] or "",
                    }
                )
            else:
                latex.append({"label": symbol, "prediction": [], "type": "context"})
        grammar = {
            "-": "frac",
            "below": "below",
            "sqrt": "sqrt",
            "super": "super",
            "*": "mult",
            "subsc": "subsc",
            "neq": "neq",
        }
        subst = helpers.subst
        latex = self.__token_substitution(latex, grammar, subst)
        return latex

    @staticmethod
    def __token_substitution(latex, grammar, subst):
        def __list_substitution(idx, nomatch, aux, initial_index, subst_list, substitution_index):
            for substitution in subst_list[substitution_index]:
                try:
                    if latex[idx]["label"] == substitution:
                        aux.append({"index": idx, "label": subst_list[substitution_index][substitution]})
                        idx += 1
                    else:
                        idx -= 1
                        nomatch = True
                except IndexError:
                    nomatch = True
                    break
                if nomatch:
                    idx = initial_index
                    break
            return idx, nomatch

        def __change_label(idx, subst_list):
            for substitution_index in range(0, len(subst_list)):
                aux = []
                idx, nomatch = __list_substitution(idx, False, aux, idx, subst_list, substitution_index)
                if not nomatch:
                    for matched in aux:
                        latex[matched["index"]]["label"] = matched["label"]
            return idx

        for i in range(0, len(latex)):
            if latex[i]["label"] in grammar:
                if (label := grammar[latex[i]["label"]]) in subst:
                    __change_label(i, subst[label])
        return latex

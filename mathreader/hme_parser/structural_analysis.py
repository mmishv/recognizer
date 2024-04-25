import re

from mathreader import helpers
from mathreader.helpers import data_structures as DS

helpers_labels = helpers.get_labels()
labels = helpers_labels["labels_parser"]


class StructuralAnalysis:
    def __init__(self, symbol_list):
        self.symbols = symbol_list

    def analyze(self):
        symbols = self.symbols
        symbols = self.__preprocessing(symbols)
        tree = self.__main_parsing(symbols)
        if not tree:
            return
        tlist = self.__tree_to_list(tree)
        latex = self.__list_to_latex_obj(tlist)
        return {"latex": latex, "tree": tree, "tlist": tlist}

    def __preprocessing(self, symbols):
        xmin_sorted = sorted(symbols, key=lambda i: i["xmin"])
        symbols = xmin_sorted
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
        listin = symbols
        T = DS.Tree()
        Q = DS.Queue()
        S = DS.Stack()
        temp1 = 0
        temp2 = 0
        R = [[0, 0], [9999999999, 9999999999]]
        sstart = self.__sp(listin, R)
        if sstart == -1:
            return
        listin[sstart]
        Q.enqueue(sstart)
        Q.enqueue(T.root_node)
        listin[sstart]["checked"] = True
        while not Q.is_empty():
            while not Q.is_empty():
                temp1 = Q.dequeue()  # a, 2
                ParentNode = Q.dequeue()
                SymbolNode = DS.SymbolNode(listin[temp1])
                T.insert(SymbolNode, ParentNode, "Node")
                S.push(temp1)  # a, 2
                S.push(SymbolNode)
                temp2 = self.__hor(listin, temp1)  # b, -
                while temp2 != -1:
                    listin[temp2]["checked"] = True
                    listin[temp2]["wall"] = listin[temp1]["wall"].copy()
                    SymbolNode = DS.SymbolNode(listin[temp2])
                    T.insert(SymbolNode, ParentNode, "Node")
                    S.push(temp2)
                    S.push(SymbolNode)
                    listin[temp1]["wall"]["right"] = listin[temp2]["xmin"]
                    temp1 = temp2  # b
                    temp2 = self.__hor(listin, temp1)  # c - 1
            S.push("EOBL")
            while not S.is_empty():
                if S.peek() == "EOBL":
                    S.pop()
                SymbolNode = S.pop()
                temp1 = S.pop()  # c
                label = int(listin[temp1]["label"])
                # 1/6
                upperThreshold = listin[temp1]["ymin"] + ((1 / 6.5) * listin[temp1]["h"])
                # 5/6
                lowerThreshold = listin[temp1]["ymin"] + ((5.5 / 6.5) * listin[temp1]["h"])
                leftThreshold = (
                    (listin[temp1]["xmin"] + ((1 / 6) * listin[temp1]["w"])) if label != 10 else listin[temp1]["xmin"]
                )
                rightThreshold = (
                    (listin[temp1]["xmax"] - ((1 / 6) * listin[temp1]["w"])) if label != 10 else listin[temp1]["xmax"]
                )
                R = [
                    {"above": [[leftThreshold, listin[temp1]["wall"]["top"]], [rightThreshold, upperThreshold]]},
                    {"below": [[leftThreshold, lowerThreshold], [rightThreshold, listin[temp1]["wall"]["bottom"]]]},
                ]
                for region in R:
                    # For each region, it looks for the initial symbol
                    reg = region[list(region.keys())[0]]
                    region_name = list(region.keys())[0]
                    # ( ) [ ] { } . * = neq + sqrt
                    operators = bool(label in range(11, 17) or label in range(27, 31) or label == 17 or label == 23)
                    if (region_name == "above" and not operators) or (region_name == "below" and not operators):
                        temp2 = self.__start(listin, reg)
                        if temp2 != -1:
                            if not listin[temp2]["checked"]:
                                listin[temp2]["checked"] = True
                                listin[temp2]["wall"]["left"] = reg[0][0]
                                listin[temp2]["wall"]["right"] = reg[1][0]
                                listin[temp2]["wall"]["top"] = reg[0][1]
                                listin[temp2]["wall"]["bottom"] = reg[1][1]
                                RelationNode = DS.RegionNode(list(region.keys())[0])
                                T.insert(RelationNode, SymbolNode, "Node")
                                Q.enqueue(temp2)
                                Q.enqueue(RelationNode)
                R = [
                    {
                        "contains": [
                            # left, top
                            [listin[temp1]["xmin"], listin[temp1]["ymin"]],
                            # right, bottom
                            [listin[temp1]["xmax"], listin[temp1]["ymax"]],
                        ]
                    },
                    {
                        "super": [
                            # left, top
                            [rightThreshold, listin[temp1]["wall"]["top"]],
                            # right, bottom
                            [listin[temp1]["wall"]["right"], upperThreshold],
                        ]
                    },
                    {
                        "subsc": [
                            # left, top
                            [rightThreshold, lowerThreshold],
                            # right, bottom
                            [listin[temp1]["wall"]["right"], listin[temp1]["wall"]["bottom"]],
                        ]
                    },
                ]
                for region in R:
                    reg = region[list(region.keys())[0]]
                    region_name = list(region.keys())[0]
                    # - ( ) [ ] { } . * = neq +
                    operators = bool(label == 10 or label in range(27, 31) or label == 17)
                    if (
                            (region_name == "super" and not operators)
                            or (region_name == "subsc" and not operators)
                            or (region_name == "contains" and int(listin[temp1]["label"]) == 23)
                    ):
                        temp2 = self.__start(listin, reg)
                        if temp2 != -1:
                            if not listin[temp2]["checked"]:
                                listin[temp2]["checked"] = True
                                listin[temp2]["wall"]["left"] = reg[0][0]
                                listin[temp2]["wall"]["right"] = reg[1][0]
                                listin[temp2]["wall"]["top"] = reg[0][1]
                                listin[temp2]["wall"]["bottom"] = reg[1][1]
                                RelationNode = DS.RegionNode(list(region.keys())[0])
                                T.insert(RelationNode, SymbolNode, "Node")
                                Q.enqueue(temp2)
                                Q.enqueue(RelationNode)
        return T

    def __overlap(self, symbolIndex, top, bottom, listin):
        listIndex = symbolIndex
        stop = False
        n = len(listin)
        if listin[symbolIndex]["label"] == "10":
            maxLength = listin[symbolIndex]["xmax"] - listin[symbolIndex]["xmin"]
        else:
            maxLength = -1
        mainLine = -1
        while listIndex > 0 and stop == False:
            if listin[listIndex - 1]["xmin"] <= listin[symbolIndex]["xmin"]:
                listIndex = listIndex - 1  # stop = True
            else:
                stop = True  # listIndex = listIndex - 1
        line1x = range(listin[symbolIndex]["xmin"], listin[symbolIndex]["xmax"] + 1)
        len_line1x = len(line1x)
        while listIndex < n and listin[listIndex]["xmin"] < listin[symbolIndex]["xmax"]:
            line2x = range(listin[listIndex]["xmin"], listin[listIndex]["xmax"] + 1)
            len_line2x = len(line2x)
            x_set = set(line1x) if len_line1x < len_line2x else set(line2x)
            x_intersection = x_set.intersection(line1x if len_line1x >= len_line2x else line2x)
            min_line = min(len_line1x, len_line2x)
            if (
                    not listin[listIndex]["checked"]
                    and listin[listIndex]["label"] == "10"
                    and listin[listIndex]["centroid"][1] >= top
                    and listin[listIndex]["centroid"][1] <= bottom
                    and listin[listIndex]["xmin"] <= (listin[symbolIndex]["xmin"] + 8)
                    and len(x_intersection) > (min_line / 2)
                    and (listin[listIndex]["xmax"] - listin[listIndex]["xmin"]) > maxLength
            ):
                maxLength = listin[listIndex]["xmax"] - listin[listIndex]["xmin"]
                mainLine = listIndex

            listIndex += 1
        if mainLine == -1:
            return symbolIndex
        else:
            return mainLine

    def __start(self, listin, R):
        left = R[0][0]
        top = R[0][1]
        right = R[1][0]
        bottom = R[1][1]
        leftmostIndex = -1
        listIndex = 0
        n = len(listin)
        while leftmostIndex == -1 and listIndex < n:
            if (
                    not listin[listIndex]["checked"]
                    and listin[listIndex]["centroid"][0] >= left
                    and listin[listIndex]["centroid"][1] >= top
                    and listin[listIndex]["centroid"][0] <= right
                    and listin[listIndex]["centroid"][1] <= bottom
            ):
                leftmostIndex = listIndex
            else:
                listIndex = listIndex + 1
        if leftmostIndex == -1:
            return leftmostIndex
        else:
            return self.__overlap(leftmostIndex, top, bottom, listin)

    def __sp(self, listin, R):
        return self.__start(listin, R)

    def __hor(self, listin, index):
        global stop
        stop = False
        global a
        a = -1
        label = int(listin[index]["label"])
        right = listin[index]["wall"]["right"]
        # to avoid get symbols behind
        left = listin[index]["xmin"]
        # to treat expoent and subscript
        # 1/6
        top = listin[index]["ymin"] + (listin[index]["h"] * (1 / 6.5))
        # 5/6
        bottom = listin[index]["ymin"] + (listin[index]["h"] * (5.5 / 6.5))
        # it doesn't have expoent and subscript
        if label == 10 or label in [27, 28, 29, 30]:
            top = listin[index]["wall"]["top"]
            bottom = listin[index]["wall"]["bottom"]
        # if it is square root, the left wall id xmax
        if label == 23:
            left = listin[index]["xmax"]
        # if it is horizontal line or brackets
        if label in range(10, 17):
            R = [[listin[index]["xmax"], top], [right, bottom]]
            a = self.__start(listin, R)
            stop = True
        else:
            for s in range(0, len(listin)):
                checked = listin[s]["checked"]
                if not checked:
                    symbol = listin[s]
                    if (
                            left <= symbol["centroid"][0] <= right
                            and bottom >= symbol["centroid"][1] >= top
                    ):
                        a = s
                        stop = True
                        break
        if stop and a != -1:
            return self.__overlap(a, listin[a]["wall"]["top"], listin[a]["wall"]["bottom"], listin)
        else:
            return -1

    def __tree_to_list(self, tree, node=None):
        latex = []

        def recur(root_node):
            current = tree.root_node if not root_node else root_node
            if current is None:
                return
            if isinstance(current.data, str):
                latex.append(current.data)
            else:
                try:
                    real_label = labels[current.data["label"]]
                    if real_label == "{":
                        real_label = "\\{"
                    if real_label == "}":
                        real_label = "\\}"
                    current.data["label"] = real_label
                    latex.append(current.data)
                except BaseException as e:
                    print("Exception: ", e)

            if current.node_type == "RegionNode":
                latex.append("{")
            for node in current.children:
                recur(node)
            if current.node_type == "RegionNode":
                latex.append("}")

        recur(node)
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

    def __token_substitution(self, latex, grammar, subst):
        def __list_substitution(i, nomatch, aux, initial_index, label, substitution_list, substitution_index):

            for substitution in substitution_list[substitution_index]:
                try:
                    if latex[i]["label"] == substitution:
                        aux.append({"index": i, "label": substitution_list[substitution_index][substitution]})
                        i += 1
                    else:
                        i -= 1
                        nomatch = True

                except IndexError:
                    nomatch = True
                    break
                if nomatch:
                    i = initial_index
                    break
            return i, nomatch

        def __change_label(i, label, substitution_list):
            for substitution_index in range(0, len(substitution_list)):
                nomatch = False
                aux = []
                initial_index = i
                i, nomatch = __list_substitution(
                    i, nomatch, aux, initial_index, label, substitution_list, substitution_index
                )
                if not nomatch:
                    for matched in aux:
                        latex[matched["index"]]["label"] = matched["label"]
            return i

        for i in range(0, len(latex)):
            if latex[i]["label"] in grammar:
                label = grammar[latex[i]["label"]]
                if label in subst:
                    substitution_list = subst[label]  # list of substitutions
                    i = __change_label(i, label, substitution_list)
        return latex

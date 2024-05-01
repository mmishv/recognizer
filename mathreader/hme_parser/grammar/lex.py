import ply.lex as lex

errors = []

tokens = (
    "VAR",
    "PLUS",
    "MIN",
    "OPENC",
    "CLOSEDC",
    "OPENP",
    "CLOSEDP",
    "OPENCO",
    "CLOSEDCO",
    "EQ",
    "NEQ",
    "CDOT",
    "LFRAC",
    "SQRT",
    "NUMBER",
    "POW",
    "SUB",
)

t_VAR = r"(a|b|c|x|y|z|m|n)"
t_PLUS = r"\+"
t_MIN = r"\-"
t_OPENC = r"(\{|\\{)"
t_CLOSEDC = r"(\}|\\})"
t_OPENP = r"\("
t_CLOSEDP = r"\)"
t_OPENCO = r"\["
t_CLOSEDCO = r"\]"
t_EQ = r"\="
t_NEQ = r"\\neq"
t_CDOT = r"\\cdot"
t_LFRAC = r"\\frac"
t_SQRT = r"\\sqrt"
t_NUMBER = r"[0-9]+(?:\.[0-9]+)?"
t_POW = r"\^"
t_SUB = "_"

t_ignore = " "


def t_error(t):
    errors.append((t.value[0], t.lexpos))
    t.lexer.skip(1)
    print("[lex.py] LEX ERROR: ", t)


# EOF handling rule
def t_eof(t):
    return None


lexer = lex.lex()


def latex_lexer(tstring):
    errors.clear()
    lexer.input(tstring)
    while True:
        tok = lexer.token()
        if not tok:
            return errors


class GrammarError(Exception):
    def __init__(self, data=None, valor="Grammar error found"):
        self.valor = valor
        self.data = data

    def __repr__(self):
        return {"message": self.valor, "data": self.data}

    def __str__(self):
        return self.valor


class LexicalError(Exception):
    def __init__(self, data=None, valor="Lexical error found"):
        self.valor = valor
        self.data = data

    def __repr__(self):
        return {"message": self.valor, "data": self.data}

    def __str__(self):
        return self.valor

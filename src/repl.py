import lex, parse, eval

class REPL:
    def __init__(self):
        self.knowns = {
            "i": parse.ImaginaryExpression(),
        } # str: expression

    def start(self):
        print("arcpy v.1.0.0")
        while True:
            code = input("> ")

            if code == ":q":
                print("Quitting...")
                break

            lexer = lex.Lexer(code)
            tokens = lexer.lex()
            parser = parse.Parser(tokens, self.knowns)
            expression = parser.parse()
            evaluator = eval.Evaluator(expression, self.knowns)
            value = evaluator.evaluate()
            if value is not None: print(value)
            
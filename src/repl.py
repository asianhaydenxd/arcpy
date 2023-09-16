import lex, parse, eval

class REPL:
    def __init__(self):
        self.knowns = {
            # Built-in knowns
            "i": parse.ImaginaryExpression(),
            "pi": parse.NumberExpression(3141592653589793, 1000000000000000),
            "e": parse.NumberExpression(2718281828459045, 1000000000000000),
            "phi": parse.NumberExpression(1618033988749895, 1000000000000000),
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
            
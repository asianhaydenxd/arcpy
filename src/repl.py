import lex, parse, eval

class REPL:
    def __init__(self):
        self.knowns = []

    def start(self):
        print("arcpy v.1.0.0")
        while True:
            code = input("> ")

            if code == ":q":
                print("Quitting...")
                break

            lexer = lex.Lexer(code)
            tokens = lexer.lex()
            parser = parse.Parser(tokens)
            expression = parser.parse()
            evaluator = eval.Evaluator(expression)
            value = evaluator.evaluate()
            print(value)
            
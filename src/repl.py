import lex, parse, eval
from numpy import sin, cos, tan, arcsin, arccos, arctan, real, imag, gcd, lcm

class REPL:
    def __init__(self):
        self.knowns = {
            # Built-in knowns
            "i": parse.ImaginaryExpression(),
            "pi": parse.NumberExpression(3141592653589793, 1000000000000000),
            "e": parse.NumberExpression(2718281828459045, 1000000000000000),
            "phi": parse.NumberExpression(1618033988749895, 1000000000000000),
            "sin": parse.EncodedFunctionExpression("sin", sin, [complex]),
            "cos": parse.EncodedFunctionExpression("cos", cos, [complex]),
            "tan": parse.EncodedFunctionExpression("tan", tan, [complex]),
            "arcsin": parse.EncodedFunctionExpression("arcsin", arcsin, [complex]),
            "arccos": parse.EncodedFunctionExpression("arccos", arccos, [complex]),
            "arctan": parse.EncodedFunctionExpression("arctan", arctan, [complex]),
            "real": parse.EncodedFunctionExpression("real", real, [complex]),
            "imag": parse.EncodedFunctionExpression("imag", imag, [complex]),
            "abs": parse.EncodedFunctionExpression("abs", abs, [complex]),
            "gcd": parse.EncodedFunctionExpression("gcd", gcd, [int, int]),
            "lcm": parse.EncodedFunctionExpression("lcm", lcm, [int, int]),
        } # str: expression
        self.operators = list(self.knowns)

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
            
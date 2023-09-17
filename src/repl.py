import lex, parse, eval
from numpy import sqrt, cbrt, sin, cos, tan, arcsin, arccos, arctan, real, imag, gcd, lcm

SET_C = lambda _: True
SET_I = lambda x: int(x) == x

class REPL:
    def __init__(self):
        self.knowns = {
            # Built-in knowns
            "i": parse.ImaginaryExpression(),
            "pi": parse.NumberExpression(3141592653589793, 1000000000000000),
            "e": parse.NumberExpression(2718281828459045, 1000000000000000),
            "phi": parse.NumberExpression(1618033988749895, 1000000000000000),
            "sqrt": parse.EncodedFunctionExpression("sqrt", sqrt, [SET_C]),
            "cbrt": parse.EncodedFunctionExpression("cbrt", cbrt, [SET_C]),
            "sin": parse.EncodedFunctionExpression("sin", sin, [SET_C]),
            "cos": parse.EncodedFunctionExpression("cos", cos, [SET_C]),
            "tan": parse.EncodedFunctionExpression("tan", tan, [SET_C]),
            "arcsin": parse.EncodedFunctionExpression("arcsin", arcsin, [SET_C]),
            "arccos": parse.EncodedFunctionExpression("arccos", arccos, [SET_C]),
            "arctan": parse.EncodedFunctionExpression("arctan", arctan, [SET_C]),
            "real": parse.EncodedFunctionExpression("real", real, [SET_C]),
            "imag": parse.EncodedFunctionExpression("imag", imag, [SET_C]),
            "abs": parse.EncodedFunctionExpression("abs", abs, [SET_C]),
            "gcd": parse.EncodedFunctionExpression("gcd", gcd, [SET_I, SET_I]),
            "lcm": parse.EncodedFunctionExpression("lcm", lcm, [SET_I, SET_I]),
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
            
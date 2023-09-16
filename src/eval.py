import parse

class NumberValue:
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f"{self.a}"
    
    def __add__(self, other):
        return NumberValue(self.a + other.a)
    
    def __sub__(self, other):
        return NumberValue(self.a - other.a)
    
class Evaluator:
    def __init__(self, expression, knowns):
        self.expression = expression
        self.knowns = knowns

    def evaluate(self):
        return self.eval(self.expression)
    
    def eval(self, expression):
        if type(expression) == parse.AdditionExpression:
            return self.eval(expression.left) + self.eval(expression.right)
        if type(expression) == parse.SubtractionExpression:
            return self.eval(expression.left) - self.eval(expression.right)
        if type(expression) == parse.NumberExpression:
            return NumberValue(int(expression.string))
        if type(expression) == parse.IdentifierExpression:
            if expression.string in list(self.knowns):
                return self.knowns[expression.string]

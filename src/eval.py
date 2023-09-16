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
    
    def __mul__(self, other):
        return NumberValue(self.a * other.a)
    
class Evaluator:
    def __init__(self, expression, knowns):
        self.expression = expression
        self.knowns = knowns

    def evaluate(self):
        return self.eval_expr(self.expression)
    
    def eval_expr(self, expression):
        if type(expression) == parse.DefinitionStatement:
            self.knowns[expression.left.string] = expression.right
        if type(expression) == parse.AdditionExpression:
            return self.eval_expr(expression.left) + self.eval_expr(expression.right)
        if type(expression) == parse.SubtractionExpression:
            return self.eval_expr(expression.left) - self.eval_expr(expression.right)
        if type(expression) == parse.MultiplicationExpression:
            return self.eval_expr(expression.left) * self.eval_expr(expression.right)
        if type(expression) == parse.ImplicitExpression:
            return self.eval_expr(expression.left) * self.eval_expr(expression.right)
        if type(expression) == parse.NumberExpression:
            return NumberValue(int(expression.string))
        if type(expression) == parse.IdentifierExpression:
            if expression.string in list(self.knowns):
                return self.eval_expr(self.knowns[expression.string])

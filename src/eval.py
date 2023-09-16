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

class FunctionValue:
    def __init__(self, params, expression):
        self.params = params
        self.expression = expression

class VectorValue:
    def __init__(self, members):
        self.members = members
    
    def __repr__(self):
        return str(self.members)
    
    def __add__(self, other):
        if len(self.members) != len(other.members):
            raise TypeError(f"vector sizes for {self} and {other} do not match")
        new_list = []
        for i in range(len(self.members)):
            new_list.append(self.members[i] + other.members[i])
        return VectorValue(new_list)
    
class Evaluator:
    def __init__(self, expression, knowns):
        self.expression = expression
        self.knowns = knowns

    def evaluate(self):
        return self.eval_expr(self.expression)
    
    def eval_expr(self, expression):
        if type(expression) == parse.DefinitionStatement:
            # Functions
            if type(expression.left) == parse.ImplicitExpression:
                # Single Variable Functions
                if type(expression.left.right) == parse.IdentifierExpression:
                    self.knowns[expression.left.left.string] = parse.FunctionExpression([expression.left.right], expression.right)
                # Multivariable Functions
                elif type(expression.left.right) == parse.VectorExpression:
                    self.knowns[expression.left.left.string] = parse.FunctionExpression(expression.left.right.members, expression.right)
            # Variables
            elif type(expression.left) == parse.IdentifierExpression:
                self.knowns[expression.left.string] = expression.right
            else:
                raise Exception("Non-identifier lvalue")
        if type(expression) == parse.AdditionExpression:
            return self.eval_expr(expression.left) + self.eval_expr(expression.right)
        if type(expression) == parse.SubtractionExpression:
            return self.eval_expr(expression.left) - self.eval_expr(expression.right)
        if type(expression) == parse.MultiplicationExpression:
            return self.eval_expr(expression.left) * self.eval_expr(expression.right)
        if type(expression) == parse.ImplicitExpression:
            lvalue = self.eval_expr(expression.left)
            if type(lvalue) == NumberValue:
                return lvalue * self.eval_expr(expression.right)
            if type(lvalue) == FunctionValue:
                expr = lvalue.expression
                for i, param in enumerate(lvalue.params):
                    expr = parse.sub(expr, param, expression.right if len(lvalue.params) == 1 else expression.right.members[i])
                return self.eval_expr(expr)
        if type(expression) == parse.FunctionExpression:
            return FunctionValue(expression.params, expression.expression)
        if type(expression) == parse.VectorExpression:
            return VectorValue([self.eval_expr(member) for member in expression.members])
        if type(expression) == parse.NumberExpression:
            return NumberValue(int(expression.string))
        if type(expression) == parse.IdentifierExpression:
            if expression.string in list(self.knowns):
                return self.eval_expr(self.knowns[expression.string])

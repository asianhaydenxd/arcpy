from lex import TokenType

class DefinitionStatement:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} = {self.right}"

class IdentifierExpression:
    def __init__(self, string: str):
        self.string = string

    def __repr__(self):
        return f"Id: {self.string}"

class NumberExpression:
    def __init__(self, dividend: int, divisor: int):
        self.dividend = dividend
        self.divisor = divisor
    
    def __repr__(self):
        return f"[Num: {self.dividend}/{self.divisor}]"

class ImaginaryExpression:
    def __init__(self):
        pass
    
    def __repr__(self):
        return f"[i]"
    
class AbsoluteExpression:
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self):
        return f"|{self.expression}|"

class AdditionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} + {self.right})"
    
class SubtractionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} - {self.right})"
    
class NegationExpression:
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self):
        return f"(-{self.expression})"
    
class FactorialExpression:
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self):
        return f"({self.expression}!)"
    
class MultiplicationExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} * {self.right})"
    
class DivisionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} / {self.right})"
    
class ExponentExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} ^ {self.right})"
    
class ImplicitExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"{self.left}({self.right})"
    
class FunctionExpression:
    def __init__(self, params, expression):
        self.params = params
        self.expression = expression
    
    def __repr__(self):
        return f"{self.params} => {self.expression}"
    
class EncodedFunctionExpression:
    def __init__(self, name, function, param_types):
        self.name = name
        self.function = function
        self.param_types = param_types
    
    def __repr__(self):
        return f"{self.name}"

class VectorExpression:
    def __init__(self, members):
        self.members = members
    
    def __repr__(self):
        return self.members

def sub(expression, old, new):
    if type(expression) == IdentifierExpression and expression.string == old.string:
        return new
    if type(expression) in [IdentifierExpression, NumberExpression]:
        return expression
    if type(expression) == AdditionExpression:
        return AdditionExpression(sub(expression.left, old, new), sub(expression.right, old, new))
    if type(expression) == SubtractionExpression:
        return SubtractionExpression(sub(expression.left, old, new), sub(expression.right, old, new))
    if type(expression) == MultiplicationExpression:
        return MultiplicationExpression(sub(expression.left, old, new), sub(expression.right, old, new))
    if type(expression) == ImplicitExpression:
        return ImplicitExpression(sub(expression.left, old, new), sub(expression.right, old, new))
    if type(expression) == VectorExpression:
        return VectorExpression([sub(member, old, new) for member in expression.members])

class Parser:
    def __init__(self, tokens, knowns) -> None:
        self.tokens = tokens
        self.knowns = knowns
        self.index = -1
        self.iterate()
    
    def iterate(self, index: int = 1):
        self.index += index
        self.token = self.tokens[self.index] if self.index_is_valid() else None

    def index_is_valid(self):
        return self.index < len(self.tokens)
    
    def parse(self):
        return self.parse_definition()
    
    def parse_definition(self):
        left_token = self.parse_vector()
        if self.index_is_valid() and self.token.matches("=", TokenType.OP):
            self.iterate()
            right_token = self.parse_vector()
            return DefinitionStatement(left_token, right_token)
        return left_token
    
    def parse_vector(self):
        token = self.parse_addition_and_subtraction()
        tokens = [token]
        while self.index_is_valid():
            if self.token.matches(",", TokenType.OP):
                self.iterate()
                tokens.append(self.parse_addition_and_subtraction())
            else:
                break
        if len(tokens) > 1: return VectorExpression(tokens)
        return token
    
    def parse_addition_and_subtraction(self):
        left_token = self.parse_division()
        while self.index_is_valid():
            if self.token.matches("+", TokenType.OP):
                self.iterate()
                right_token = self.parse_division()
                left_token = AdditionExpression(left_token, right_token)
            elif self.token.matches("-", TokenType.OP):
                self.iterate()
                right_token = self.parse_division()
                left_token = SubtractionExpression(left_token, right_token)
            else:
                break
        return left_token
    
    def parse_division(self):
        left_token = self.parse_multiplication()
        while self.index_is_valid():
            if self.token.matches("/", TokenType.OP):
                self.iterate()
                right_token = self.parse_multiplication()
                left_token = DivisionExpression(left_token, right_token)
            else:
                break
        return left_token
    
    def parse_multiplication(self):
        left_token = self.parse_negation()
        while self.index_is_valid():
            if self.token.matches("*", TokenType.OP):
                self.iterate()
                right_token = self.parse_negation()
                left_token = MultiplicationExpression(left_token, right_token)
            else:
                break
        return left_token
    
    def parse_negation(self):
        if self.token.matches("-", TokenType.OP):
            self.iterate()
            token = self.parse_factorial()
            return NegationExpression(token)
        return self.parse_factorial()
    
    def parse_factorial(self):
        expression = self.parse_implicit()
        while self.index_is_valid() and self.token.matches("!", TokenType.OP):
            self.iterate()
            expression = FactorialExpression(expression)
        return expression
    
    def parse_implicit(self):
        left_token = self.parse_exponent()
        if self.index_is_valid() and (self.token.tokentype in [TokenType.NUM, TokenType.ID] or self.token.matches("(", TokenType.OP)):
            right_token = self.parse_implicit()
            return ImplicitExpression(left_token, right_token)
        return left_token
    
    def parse_exponent(self):
        left_token = self.parse_factor()
        if self.index_is_valid() and self.token.matches("^", TokenType.OP):
            self.iterate()
            right_token = self.parse_exponent()
            return ExponentExpression(left_token, right_token)
        return left_token
    
    def parse_factor(self):
        token = self.token
        self.iterate()

        if token.tokentype == TokenType.NUM:
            dividend, divisor = make_fraction(token.string)
            return NumberExpression(dividend, divisor)
        
        if token.tokentype == TokenType.ID:
            return IdentifierExpression(token.string)
        
        if token.matches("(", TokenType.OP):
            expr = self.parse_vector()
            if not self.token.matches(")", TokenType.OP):
                raise Exception("Unmatched parenthesis")
            self.iterate()
            return expr
        
        if token.matches("|", TokenType.OP):
            expr = self.parse_vector()
            if not self.token.matches("|", TokenType.OP):
                raise Exception("Unmatched bars")
            self.iterate()
            return AbsoluteExpression(expr)
        
def make_fraction(string):
    dividend = ""
    divisor = 1
    point_met = False
    for char in string:
        if char in "1234567890":
            dividend += char
            if point_met: divisor *= 10
        if char == ".":
            point_met = True
    return (int(dividend), divisor)

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
    def __init__(self, string: str):
        self.string = string
    
    def __repr__(self):
        return f"Num: {self.string}"

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
    
class MultiplicationExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} * {self.right})"

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
        left_token = self.parse_addition_and_subtraction()
        if self.index_is_valid() and self.token.matches("=", TokenType.OP):
            if type(left_token) is not IdentifierExpression:
                raise Exception("Non-identifier lvalue")
            self.iterate()
            right_token = self.parse_addition_and_subtraction()
            return DefinitionStatement(left_token, right_token)
        return left_token
    
    def parse_addition_and_subtraction(self):
        left_token = self.parse_multiplication()
        while self.index_is_valid():
            if self.token.matches("+", TokenType.OP):
                self.iterate()
                right_token = self.parse_multiplication()
                left_token = AdditionExpression(left_token, right_token)
            elif self.token.matches("-", TokenType.OP):
                self.iterate()
                right_token = self.parse_multiplication()
                left_token = SubtractionExpression(left_token, right_token)
            else:
                break
        return left_token
    
    def parse_multiplication(self):
        left_token = self.parse_factor()
        while self.index_is_valid():
            if self.token.tokentype is TokenType.NUM or self.token.tokentype is TokenType.ID:
                right_token = self.parse_factor()
                left_token = MultiplicationExpression(left_token, right_token)
            else:
                break
        return left_token
    
    def parse_factor(self):
        token = self.token
        self.iterate()

        if token.tokentype == TokenType.NUM:
            return NumberExpression(token.string)
        
        if token.tokentype == TokenType.ID:
            return IdentifierExpression(token.string)

from parse.lex import TokenType

class IdentifierNode:
    def __init__(self, string: str):
        self.string = string

    def __repr__(self):
        return f"Id: {self.string}"

class NumberNode:
    def __init__(self, string: str):
        self.string = string
    
    def __repr__(self):
        return f"Num: {self.string}"

class AdditionNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"({self.left} + {self.right})"

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = -1
        self.iterate()
    
    def iterate(self, index: int = 1):
        self.index += index
        self.token = self.tokens[self.index] if self.index < len(self.tokens) else None
    
    def parse(self):
        return self.parse_addition()
    
    def parse_addition(self):
        left_token = self.parse_factor()
        if self.token.matches("+", TokenType.OP):
            self.iterate()
            right_token = self.parse_factor()
            return AdditionNode(left_token, right_token)
        return left_token
    
    def parse_factor(self):
        token = self.token
        self.iterate()

        if token.tokentype == TokenType.NUM:
            return NumberNode(token.string)

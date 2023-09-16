from parse.lex import TokenType

class IdentifierNode:
    def __init__(self, string: str):
        self.string = string

class NumberNode:
    def __init__(self, string: str):
        self.string = string

class AdditionNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = -1
    
    def next_token(self, index: int = 1):
        self.index += index
        self.token = self.tokens[self.index] if self.index < len(self.tokens) else None
        return self.token
    
    def parse(self):
        return self.parse_factor()
    
    def parse_factor(self):
        token = self.next_token()

        if token.tokentype == TokenType.NUM:
            return NumberNode(token.string)

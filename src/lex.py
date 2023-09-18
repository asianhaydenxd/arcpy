# import parse.tokens
from enum import Enum

NUMBERS = "1234567890"
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZŠŒŽšœžŸÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþαβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"

KEYWORDS = [
    "and",
    "or",
    "xor",
    "not",
]

class TokenType(Enum):
    ID = "id"
    NUM = "num"
    OP = "op"
    KW = "kw"
    NONE = "none"

class Token:
    def __init__(self, string: str, tokentype: TokenType, index: int):
        self.string = string
        self.tokentype = tokentype
        self.index = index

    def matches(self, string: str, tokentype: TokenType):
        return self.string == string and self.tokentype is tokentype

class LexerError:
    def __init__(self, msg: str, code: str, index: int):
        self.msg = msg
        self.code = code
        self.index = index

class Lexer:
    def __init__(self, code: str, operators):
        self.code = code
        self.operators = operators
        self.index = 0
        self.tokens = []

    def add_token(self, string: str, tokentype: TokenType):
        self.tokens.append(Token(string, tokentype, self.index))

    def index_is_valid(self):
        return self.index < len(self.code)
    
    def current_character(self, i = 1):
        return self.code[self.index : self.index + i]

    def next(self, i = 1):
        self.index += i

    def lex(self):
        while self.index_is_valid():
            if self.current_character() in " \t":
                self.next()
                continue

            for keyword in sorted(KEYWORDS, reverse=True, key=len):
                if self.current_character(len(keyword)) == keyword:
                    self.add_token(keyword, TokenType.KW)
                    self.next(len(keyword))
                    break
            else:
                for operator in sorted(self.operators, reverse=True, key=len):
                    if self.current_character(len(operator)) == operator:
                        self.add_token(operator, TokenType.ID)
                        self.next(len(operator))
                        break
                else:
                    # Function Operator (implemented early
                    # as an example of a two-char-long op)
                    if self.current_character(2) == "=>":
                        self.add_token("=>", TokenType.OP)
                        self.next(2)

                    # Definition Operator
                    elif self.current_character() == "=":
                        self.add_token("=", TokenType.OP)
                        self.next()

                    # Addition Operator
                    elif self.current_character() == "+":
                        self.add_token("+", TokenType.OP)
                        self.next()
                    
                    # Subtraction Operator
                    elif self.current_character() == "-":
                        self.add_token("-", TokenType.OP)
                        self.next()

                    # Multiplication Operator
                    elif self.current_character() == "*":
                        self.add_token("*", TokenType.OP)
                        self.next()

                    # Division Operator
                    elif self.current_character() == "/":
                        self.add_token("/", TokenType.OP)
                        self.next()

                    # Exponent Operator
                    elif self.current_character() == "^":
                        self.add_token("^", TokenType.OP)
                        self.next()

                    # Factorial Operator
                    elif self.current_character() == "!":
                        self.add_token("!", TokenType.OP)
                        self.next()
                    
                    # Comma Operator
                    elif self.current_character() == ",":
                        self.add_token(",", TokenType.OP)
                        self.next()

                    # Parentheses Operators
                    elif self.current_character() == "(":
                        self.add_token("(", TokenType.OP)
                        self.next()
                    elif self.current_character() == ")":
                        self.add_token(")", TokenType.OP)
                        self.next()
                    
                    # Bar Operator
                    elif self.current_character() == "|":
                        self.add_token("|", TokenType.OP)
                        self.next()

                    elif self.current_character() == "\\":
                        self.next()
                        self.lex_multichar_id()
                    
                    elif self.current_character() in LETTERS:
                        self.add_token(self.current_character(), TokenType.ID)
                        self.next()

                    elif self.current_character() in NUMBERS:
                        self.lex_number()

                    else:
                        raise Exception(f"unrecognized character \"{self.current_character()}\"")
        
        return self.tokens
    
    def lex_multichar_id(self):
        word = ""

        while self.index_is_valid() and self.current_character() in LETTERS + NUMBERS + "_":
            word += self.current_character()
            self.next()

        self.add_token(word, TokenType.ID)
        
    def lex_number(self):
        word = ""

        while self.index_is_valid() and self.current_character() in "1234567890_.":
            if self.current_character() == "_":
                continue
            elif self.current_character() == "." and self.code[self.index+1] in "1234567890_":
                word += self.current_character()
            elif self.current_character() == ".":
                break
            else:
                word += self.current_character()
            self.next()

        self.add_token(word, TokenType.NUM)

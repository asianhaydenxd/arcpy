# import parse.tokens

NUMBERS = "1234567890"
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZŠŒŽšœžŸÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþαβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"

class Token:
    def __init__(self, string: str, index: int):
        self.string = string
        self.index = index

class LexerError:
    def __init__(self, msg: str, code: str, index: int):
        self.msg = msg
        self.code = code
        self.index = index

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.index = 0
        self.tokens = []

    def add_token(self, string: str):
        self.tokens.append(Token(string, self.index))

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

            elif self.current_character(2) == "=>":
                self.add_token("=>")
                self.next(2)

            elif self.current_character() == "+":
                self.add_token("+")
                self.next()
            
            elif self.current_character() in LETTERS:
                self.add_token(self.current_character())
                self.next()

            elif self.current_character() in NUMBERS:
                self.lex_number()

            else:
                raise Exception(f"Unhandled character \"{self.current_character()}\"")
        
    def lex_number(self):
        word = ""

        while self.index_is_valid() and self.current_character() in "1234567890":
            word += self.current_character()
            self.next()

        self.add_token(word)

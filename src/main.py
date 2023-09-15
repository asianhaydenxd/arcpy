import repl as repl
import parse.lex as lex

def main():
    # new_repl = repl.REPL()
    # new_repl.start()
    lexer = lex.Lexer("123+ 2")
    lexer.lex()
    
    # Print Tokens
    for token in lexer.tokens:
        print(token.string)

if __name__ == "__main__":
    main()
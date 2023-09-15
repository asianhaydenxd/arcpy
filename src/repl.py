class REPL:
    def __init__(self):
        self.knowns = []

    def start(self):
        print("arcpy v.1.0.0")
        while True:
            cmd = input("> ")
            if cmd == ":q":
                print("Quitting...")
                break
            
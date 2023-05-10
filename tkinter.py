import tkinter
from browser import request
WIDTH , HEIGHT = 800 ,600

def lex(body):
    text = ""
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            text += c
    return text

class Browser:
    def __init__(self):
        #tk creates a window
        self.window = tkinter.Tk()
        #creates the canvas and puts the window inside it
        self.canvas = tkinter.Canvas(
            self.window, 
            width=WIDTH,
            height=HEIGHT
        )
        #pack the canvas to fir tk
        self.canvas.pack()

    def load(self, url):
        # load data
        headers, body = request(url)
        text = lex(body)
        for c in text:
            self.canvas.create_text(100, 100, text=c)

if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()

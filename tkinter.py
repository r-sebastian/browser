import tkinter
from browser import request #use HTTP connection if certificate error is shown
WIDTH , HEIGHT = 800 ,600   #resolution of the canvas
HSTEP, VSTEP = 13, 18   #poniters to dispaly where the next charater is printed

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
    return text #returns the content of the page without tags


class Browser:
    def __init__(self):
        #tk creates a window
        self.window = tkinter.Tk()
        #creates the canvas and puts the window inside it
        self.canvas = tkinter.Canvas(
            self.window, #to tell the canvas where to dispaly the canvas
            width=WIDTH,
            height=HEIGHT
        )
        #pack the canvas to fit tk
        self.canvas.pack()

    def load(self, url):
        # load data
        headers, body = request(url)
        text = lex(body)
        cursor_x, cursor_y = HSTEP, VSTEP
        #draw the text char by char
        for c in text:
            self.canvas.create_text(cursor_x, cursor_y, text=c)
            #prinitng earch line
            cursor_x += HSTEP
            #if cursor reaches the end wrap to next line
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP   #increases the vertical step
                cursor_x = HSTEP    #resets the hori step
            #thus priting each line

if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()

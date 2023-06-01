import tkinter
import tkinter.font
from browser import request #use HTTP connection if certificate error is shown
WIDTH , HEIGHT = 800 ,600   #resolution of the canvas
HSTEP, VSTEP = 13, 18   #poniters to dispaly where the next charater is printed
SCROLL_STEP = 100

class Text:
    def __init__(self, text):
        self.text = text

class Tag:
    def __init__(self, tag):
        self.tag = tag

def lex(body):
    out = []
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if text: out.append(Text(text))
            text = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(text))
            text = ""
        else:
            text += c
    if not in_tag and text:
        out.append(Text(text))
    return out

class Layout:
    def __init__(self, tokens):
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        for tok in tokens:
            self.token(tok)

        def token(self, tok):
            if isinstance(tok, Text):
                self.text(tok)
            elif tok.tag == "i":
                style = "italic"
            elif tok.tag == "/i":
                style = "roman"
            elif tok.tag == "b":
                weight = "bold"
            elif tok.tag == "/b":
                weight = "normal"
            elif tok.tag == "small":
                self.size -= 2
            elif tok.tag == "/small":
                self.size += 2
            elif tok.tag == "big":
                self.size += 4
            elif tok.tag == "/big":
                self.size -= 4
                
        def text(self, tok):
            font = tkinter.font.Font(
                size=self.size,
                weight=self.weight,
                slant=self.style,
            )
            for word in tok.text.split():
                w = font.measure(word)
                if self.cursor_x + w > WIDTH - HSTEP:
                    self.flush()
                self.line.append((self.cursor_x, word, font))
                self.cursor_x += w + font.measure(" ")


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
        #var to store how far user have scrolled
        self.scroll = 0
        
        #SCROLL
        #option to scroll down using the down arrow key
        self.window.bind("<Down>", self.scrolldown) #scrolldown is a event handler tk() calles when down is pressed

        #setting up font
        bi_times = tkinter.font.Font(
            family="Times",
            size=16,
            weight="bold",
            slant="italic",
        )

    def load(self, url):
        headers, body = request(url)
        tokens = lex(body)
        self.display_list = layout(text)
        self.display_list = Layout(tokens).display_list
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")   #delets all the text everytime we call dra()-->for scrolling
        #loops thorugh diaply list
        for x, y, c in self.display_list:
            #bewlo 2 if are used to make scrolling faster
            #we only render stuff in our view
            if y > self.scroll + HEIGHT: 
                continue
            if y + VSTEP < self.scroll: #computes the bottom edge of the character, so that characters that are halfway inside the viewing window are still drawn
                continue
            #dispalying each char in list with correct positions
            #scroll value can now scroll the page as;y  is page coordinate therefore y-scroll is the screen coord
            self.canvas.create_text(x, y - self.scroll , text=c, font = bi_times, anchor = 'nw')
            '''
            loading information about the shape of a character, inside create_text, takes a while
            therefore slow scrolling
            '''

    #incremetns y and redraws the canvas
    def scrolldown(self, e):
        self.scroll += SCROLL_STEP  #increase y
        self.draw()                 #update canvas

if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()

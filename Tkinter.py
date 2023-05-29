import tkinter
from browser import request #use HTTP connection if certificate error is shown
WIDTH , HEIGHT = 800 ,600   #resolution of the canvas
HSTEP, VSTEP = 13, 18   #poniters to dispaly where the next charater is printed
SCROLL_STEP = 100

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

def layout(text):
        #list for each char dispaly
        display_list = []   #list of things to display
        cursor_x, cursor_y = HSTEP, VSTEP
        for word in text.split():
            w = font.measure(word)  //measure width
            if cursor_x + w > WIDTH - HSTEP:
                cursor_y += font.metrics("linespace") * 1.25
                cursor_x = HSTEP
            self.display_list.append((cursor_x, cursor_y, word))
            cursor_x += w + font.measure(" ")
        '''
        display_list.sort()
        '''
        return display_list

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
        text = lex(body)
        self.display_list = layout(text)
        self.display_list.sort()    #NOT NEEDED;used here for smoother scrolling
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")   #delets all the text everytime we call dra()-->for scrolling
        #loops thorugh diaply list
        for x, y, c in self.display_list:\
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

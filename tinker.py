import tkinter

WIDTH , HEIGHT = 800 ,600

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
        self.canvas.create_rectangle(10, 20, 400, 300) #left,top,right,bottom
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text="Hi!")

if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()



class Renderer:

    def __init__(self):
        self.linewidth=0
        self.maxlines=0
        self.charwidth=0
        self.lineheigth=0

    def renderline(self,line,color,x,y):
        pass #STUB, to be replaced in subclass

    def refresh(self):
        pass #STUB, to be replaced in subclass

    def quit(self):
        pass #STUB, to be replaced in subclass
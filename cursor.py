class Cursor():

    def __init__(self):
        self.position = [0, 0] #char, line
        self.cyclesymbols = ["░", "▓"]  # █░▒▓
        self.symbol = self.cyclesymbols[0]
        self.cycleframes = 10
        self.cyclecounter = self.cycleframes

    def line(self):
        return self.position[1]

    def char(self):
        return self.position[0]

    def setline(self,y):
        self.position[1]=y
    
    def setchar(self,x):
        self.position[0]=x

    def cyclecursor(self):
        self.cyclecounter-=1
        if self.cyclecounter < 0:
            self.cyclecounter = self.cycleframes
            i = self.cyclesymbols.index(self.symbol)
            nexti = (i+1) % len(self.cyclesymbols)
            self.symbol = self.cyclesymbols[nexti]


class Cursor():

    def __init__(self):
        # TODO handle an x,y position ?
        self.position = 0  # position of the cursor in the text string
        self.cyclesymbols = ["░", "▓"]  # █░▒▓
        self.symbol = self.cyclesymbols[0]
        self.cycleframes = 10
        self.cyclecounter = self.cycleframes

    def cyclecursor(self):
        self.cyclecounter-=1
        if self.cyclecounter < 0:
            self.cyclecounter = self.cycleframes
            i = self.cyclesymbols.index(self.symbol)
            nexti = (i+1) % len(self.cyclesymbols)
            self.symbol = self.cyclesymbols[nexti]


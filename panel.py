
#kyrlian, 2023

class Panel:

    def __init__(self, title="", initargs="", status="normal"):
        self.controls = "□_|x"
        self.title = title
        self.status = status
        self.zone = None
        self.sizes = [.1, .5, .9]
        self.content = []
        self.initcontent(initargs)
        self.update()

    def attachtozone(self, zone):
        self.zone = zone

    def preferedsizes(self):
        pass  # stub, to be customized for each panel type

    def initcontent(self, initargs):
        pass  # stub, to be customized for each panel type

    def updatecontent(self):
        pass  # stub, to be customized for each panel type

    def update(self):
        self.updatecontent()
        self.preferedsizes()  # is after init content, so it can use len(self.content)

    def toggleminimised(self):
        if self.status == "minimized":
            self.status = "normal"
            self.zone.resizeme(self.sizes[1])
        elif self.status == "normal":
            self.status = "maximized"
            self.zone.resizeme(self.sizes[2])
        else:
            self.status = "minimized"
            self.zone.resizeme(self.sizes[0])

    def getcolor(self, context):
        if context.focusedpanel == self:
            return (200, 200, 200)
        else:
            return (100, 100, 100)

    def isclicked(self, charx, chary):
        return charx >= self.zone.x and charx < self.zone.x + self.zone.w and chary >= self.zone.y and chary < self.zone.y + self.zone.h

    def handlecontrolclick(self, event, charx, chary):
        controlsminimize = -5  # "□_|x"
        controlssplith = -4
        controlssplitv = -3
        controlsclose = -2
        if chary == self.zone.y:
            if charx == self.zone.x + self.zone.w + controlsminimize:
                print("clicked minimize")
                self.toggleminimised()
            elif charx == self.zone.x + self.zone.w + controlssplith:
                print("clicked split h")
                self.zone.split("h", .5)
            elif charx == self.zone.x + self.zone.w + controlssplitv:
                print("clicked split v")
                self.zone.split("v", .5)
            elif charx == self.zone.x + self.zone.w + controlsclose:
                print("clicked close")
                self.zone.remove()

    def handlepanelclick(self, event, charx, chary):
        self.handlecontrolclick(event, charx, chary)

    def handlepanelkeydown(self, event, keymods):
        pass  # stub, to be customized for each panel type

    def draw(self):
        txtarray = []
        # top border with windows controls
        for i in range(self.zone.y):
            txtarray.append("")
        txtarray.append(" "*self.zone.x+"╔"+self.title+"═"*(self.zone.w-2-len(self.title) -
                        len(self.controls))+self.controls+"╗")  # top border
        # side borders plus content
        try:
            for txtline in self.content:
                txtarray.append(" "*self.zone.x+"║"+txtline +
                                " "*(self.zone.w-2-len(txtline))+"║")
        except:
            #for debuging draw errors
            raise
        # side borders after content
        for i in range(self.zone.h-2-len(self.content)):
            txtarray.append(" "*self.zone.x+"║"+" "*(self.zone.w-2)+"║")
        # bottom border
        txtarray.append(" "*self.zone.x+"╚"+"═" *
                        (self.zone.w-2)+"╝")  # bottom border
        cutarray = []  # generate copy array staying in the zone
        for y in range(self.zone.y+self.zone.h):
            cutarray.append(txtarray[y][0:self.zone.x+self.zone.w])
        return cutarray

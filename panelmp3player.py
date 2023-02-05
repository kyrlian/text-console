from panel import Panel

class Panelmp3player(Panel):

    def initcontent(self, content):
        self.content = "▣ > || << >>"
        self.contentheigth = 1

    def handleplayerclick(self, charx, chary):
        controlsstop = [1]  # "▣ > || << >>"
        controlssplay = [3]
        controlsspause = [5,6]
        controlscbwd = [8,9]
        controlscfwd = [11,12]
        if chary == self.zone.y+1:
            if charx -self.zone.x in controlsstop:
                print("clicked stop")
            elif charx -self.zone.x in controlssplay:
                print("clicked play")
            elif charx -self.zone.x in controlsspause:
                print("clicked pause")
            elif charx- self.zone.x in controlscbwd:
                print("clicked bwd")
            elif charx - self.zone.x in controlscfwd:
                print("clicked fwd")

    def handlepanelclick(self, charx, chary):
        self.handleplayerclick(charx, chary)
        self.handlecontrolclick(charx, chary)
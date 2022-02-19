from inkkeys import *
from modules.IMode import IMode
# title: Media
# 1.             | 5.
# 2.             | 6.
# 3.             | 7.
# 4.             | 8.
# Jag Press      :
# -> switch to ModeMedia
# ->
# Jag Jag Rotate
#   left         :
#   right        :
class ModeManagement(IMode):
    Title = "Modes"

    mode_position: int = 0
    modes: IMode = []

    def set_modes(self, modes):
        self.modes = modes

    def activate(self, device):
        self.device = device
        self.device.sendTextFor("title", self.Title, inverted=True)
        self.SetupButtons()
        self.device.updateDisplay(True)

    def __IterateMode(self, direction: int):
        self.mode_position = self.mode_position + direction

        if self.mode_position < 0:
            self.mode_position = 0

        if self.mode_position >= self.modes.__len__():
            self.mode_position = 0

        self.mode = self.modes[self.mode_position]
        self.device.sendTextFor(1, "< " + self.mode.Title + " >", inverted=False)
        self.device.updateDisplay(fullRefresh=True)

    def SelectMode(self):
        return lambda: self.__SelectMode()

    def __SelectMode(self):
        self.mediator.notify(self, self.mode.Title)

    def IterateModeFW(self):
        return lambda: self.__IterateMode(1)

    def IterateModeBW(self):
        return lambda: self.__IterateMode(-1)

    ## Jog

    def SetupJogRotation(self):
        # Jog dial rotation - Pressing + (CW) or - (CCW) to zoom in and out
        self.device.registerCallback(self.IterateModeFW(), KeyCode.JOG_CW)
        self.device.registerCallback(self.IterateModeBW(), KeyCode.JOG_CCW)

    def SetupJogButton(self):
        # Button1 (Jog dial press) - Pressing F to home camera
        self.device.sendTextFor(1, "<   Select mode   >")
        self.device.registerCallback(self.SelectMode(), KeyCode.JOG_PRESS)

    ## first row
    def SetupButton1(self):
        # Button1 (top left)
        self.device.sendIconFor(2, "icons/dot.png")
        self.device.registerCallback(self.StartAppInUsrBin("chromium-browser"), KeyCode.SW2_PRESS)

    def SetupButton5(self):
        # Button5 (top right)
        self.device.sendIconFor(6, "icons/dot.png")

    ## second row
    def SetupButton2(self):
        # Button3 (left, second from top)
        self.device.sendIconFor(3, "icons/dot.png")

    def SetupButton6(self):
        # Button6(right, second from top)
        self.device.sendIconFor(7, "icons/dot.png")

    ## third row
    def SetupButton3(self):
        # Button4 (left, third from top)
        self.device.sendIconFor(4, "icons/dot.png")

    def SetupButton7(self):
        # Button8 (right, third from top)
        self.device.sendIconFor(8, "icons/dot.png")

    ## fourth row
    def SetupButton4(self):
        # Button5 (bottom left)
        self.device.sendIconFor(5, "icons/dot.png")

    def SetupButton8(self):
        # Button9 (bottom right)
        self.device.sendIconFor(9, "icons/dot.png")

    ## other methods
    def poll(self, device):
        return False  # No polling in this example

    def animate(self, device):
        device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        pass  # Nothing to clean up in this example

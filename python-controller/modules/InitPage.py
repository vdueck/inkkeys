# title: Init
# 1.    Code          |   Media
# 2.    Starter       |   Status
# 3.    Teams         |     -
# 4.      -           |     -
# Jog Rotate - switch to next page
# -> need a list of pages
# -> Page contains 8 mode entries
# -> need of one default mode entry which has a dot as icon and no action

from inkkeys import *
from modules.IMode import *


class InitPage(IMode):
    Title = "Init"

    def activate(self, device):
        super().activate(device)
        self.mediator.notify_display(self, DisplayUpdateCommand(CommandType.Text, "title", self.Title, False, True))
        self.SetupButtons()

    ## first row
    def SetupButton1(self):
        # code button -> should activate the code modus
        # Button1 (top left)
        # KeyCode.SW2_PRESS
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 2, "icons/keyboard.png", False, False))
        self.device.registerCallback(self.ActivateMode("Code"), KeyCode.SW2_PRESS)

    def SetupButton5(self):
        # media button -> should activate the media modus
        # Button5 (top right)
        # KeyCode.SW6_PRESS
        self.mediator.notify_display(self, DisplayUpdateCommand(CommandType.Icon, 6, "icons/play.png", False, False))
        self.device.registerCallback(self.ActivateMode("Media"), KeyCode.SW6_PRESS)

    ## second row
    def SetupButton2(self):
        # Button3 (left, second from top)
        # KeyCode.SW3_PRESS
        # self.device.sendIconFor(3, "icons/dot.png")
        # self.device.registerCallback(self.StartAppInUsrBin("kontact"), KeyCode.SW3_PRESS)
        pass

    def SetupButton6(self):
        # Button6(right, second from top)
        # KeyCode.SW7_RELEASE
        # self.device.sendIconFor(7, "icons/dot.png")
        # self.device.registerCallback(self.StartAppInUsrBin("dolphin"), KeyCode.SW7_PRESS)
        pass

    ## third row
    def SetupButton3(self):
        # Button4 (left, third from top)
        pass  # self.device.sendIconFor(4, "icons/dot.png")

    def SetupButton7(self):
        # Button8 (right, third from top)
        # KeyCode.SW8_RELEASE
        pass  # self.device.sendIconFor(8, "icons/dot.png")

    ## fourth row
    def SetupButton4(self):
        # Button5 (bottom left)
        # KeyCode.SW5_PRESS
        pass  # self.device.sendIconFor(5, "icons/dot.png")

    def SetupButton8(self):
        # Button9 (bottom right)
        # KeyCode.SW9_PRESS
        pass  # self.device.sendIconFor(9, "icons/dot.png")

    ## Jog
    def SetupJogRotation(self):
        # rotation should show next page
        # Jog dial rotation - Pressing + (CW) or - (CCW) to zoom in and out
        self.device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, -1)])
        self.device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, 1)])

    def SetupJogButton(self):
        # Button1 (Jog dial press) - Pressing F to home camera
        # self.device.registerCallback(self.ReturnToModeManagement(), KeyCode.JOG_PRESS)
        pass

    ## other methods
    def poll(self):
        return False  # No polling in this example

    def animate(self):
        self.device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self):
        self.device.clearCallback()
        pass  # Nothing to clean up in this example

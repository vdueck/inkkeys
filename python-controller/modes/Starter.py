# title: Starter
# 1.    Chromium      |   Firefox
# 2.    Rider         |   Webstorm
# 3.    Pycharm       |   Kontact
# 4.                  |
from inkkeys import *
from interfaces.IMode import *


class Starter(IMode):
    Title = "Starter"

    def activate(self):
        self.notify_display(DisplayUpdateCommand(CommandType.Text, "title", self.Title, False, True))
        # self.mediator.notify_display(self, DisplayUpdateCommand(CommandType.Text, "title", self.Title, False, True))
        self.SetupButtons()

    ## first row
    def SetupButton1(self):
        # Button1 (top left)
        # KeyCode.SW2_PRESS
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 2, "app-icons/app-chrome.png", False, False))
        self.set_key(SetKeyCommand(SetKeyCommandType.Callback, KeyCode.SW2_PRESS,
                                   self.StartAppAbsolutePath("/snap/bin/chromium")))

    def SetupButton5(self):
        # Button5 (top right)
        # KeyCode.SW6_PRESS
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 6, "app-icons/app-email.png", False, False))
        self.set_key(SetKeyCommand(SetKeyCommandType.Callback, KeyCode.SW6_PRESS, self.StartAppInUsrBin("thunderbird")))
        # self.device.sendIconFor(6, "icons/dot.png")
        pass  # self.device.registerCallback(self.StartAppInUsrBin("firefox"), KeyCode.SW6_PRESS)

    ## second row
    def SetupButton2(self):
        # Button3 (left, second from top)
        # KeyCode.SW3_PRESS
        # self.device.sendIconFor(3, "icons/dot.png")
        pass  # self.device.registerCallback(self.StartAppInUsrBin("kontact"), KeyCode.SW3_PRESS)

    def SetupButton6(self):
        # Button6(right, second from top)
        # KeyCode.SW7_RELEASE
        # self.device.sendIconFor(7, "icons/dot.png")
        pass  # self.device.registerCallback(self.StartAppInUsrBin("dolphin"), KeyCode.SW7_PRESS)

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
        # Jog dial rotation - Pressing + (CW) or - (CCW) to zoom in and out
        # self.device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, -1)])
        # self.device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, 1)])
        pass

    def SetupJogButton(self):
        self.set_key(SetKeyCommand(SetKeyCommandType.Callback, KeyCode.JOG_PRESS, self.ActivateMode("Init")))
        # Button1 (Jog dial press) - Pressing F to home camera
        pass  # self.device.registerCallback(self.ReturnToModeManagement(), KeyCode.JOG_PRESS)

    ## other methods
    def poll(self):
        return False  # No polling in this example

    def animate(self):
        pass  # self.device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self):
        # self.device.clearCallback()
        pass  # Nothing to clean up in this example

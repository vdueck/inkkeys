import os

from inkkeys import Device, KeyCode
from modules.Display import DisplayUpdateCommand
from modules.Mediator import Mediator


class IMode:
    Title = ""
    device: Device = None

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator

    def activate(self, device):
        self.device = device

    def SetupButtons(self):
        self.ClearButtons()
        self.device.clearCallbacks()
        self.SetupJogButton()
        self.SetupJogRotation()
        self.SetupButton1()
        self.SetupButton2()
        self.SetupButton3()
        self.SetupButton4()
        self.SetupButton5()
        self.SetupButton6()
        self.SetupButton7()
        self.SetupButton8()

    def ClearButtons(self):
        for keyCode in KeyCode:
            self.device.assignKey(keyCode, [])

    def StartAppInUsrBin(self, app_name):
        return lambda: self.__StartAppInUsrBin(app_name)

    def StartAppAbsolutePath(self, path_to_app):
        return lambda: self.__StartAppAbsolutePath(path_to_app)

    @staticmethod
    def __StartAppInUsrBin(app_name):
        path = "/usr/bin/" + app_name + " &"
        os.system(path)

    @staticmethod
    def __StartAppAbsolutePath(path):
        os.system(path + " &")

    def ReturnToModeManagement(self):
        return lambda: self.__ReturnToModeManagment()

    def __ReturnToModeManagement(self):
        self.device.clearCallbacks()
        self.mediator.notify(self, "Reset")

    def UpdateDisplay(self, command: DisplayUpdateCommand):
        self.mediator.notify()
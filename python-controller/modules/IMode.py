import os

from inkkeys import Device, KeyCode
from modules.Mediator import Mediator
from modules.DisplayManager import CommandType, DisplayUpdateCommand


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
        self.mediator.notify_display(self, DisplayUpdateCommand(update_display=True))

    def ClearButtons(self):
        for keyCode in KeyCode:
            self.device.assignKey(keyCode, [])

    def StartAppInUsrBin(self, app_name):
        return lambda: self.__StartAppInUsrBin(app_name)

    def StartAppAbsolutePath(self, path_to_app):
        return lambda: self.__StartAppAbsolutePath(path_to_app)

    def ActivateMode(self, mode_name):
        return lambda: self.__ActivateMode(mode_name)

    @staticmethod
    def __StartAppInUsrBin(app_name):
        path = "/usr/bin/" + app_name + " &"
        os.system(path)

    @staticmethod
    def __StartAppAbsolutePath(path):
        os.system(path + " &")

    def __ActivateMode(self, mode_name):
        self.mediator.notify(self, mode_name)
        pass

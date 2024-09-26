import os

from inkkeys import Device, KeyCode
from modules.Mediator import Mediator
from modules.DisplayManager import CommandType, DisplayUpdateCommand
from modules.KeyManager import SetKeyCommand, SetKeyCommandType
from modules.LedManager import LedCommand


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

    def notify_display(self, command: DisplayUpdateCommand):
        self.mediator.notify_display(self, command)

    def set_key(self, command):
        self.mediator.set_key(self, command)

    def notify_led(self, command):
        self.mediator.notify_led(self, command)

    def deactivate(self):
        self.mediator.set_key(self, SetKeyCommand(command_type=SetKeyCommandType.Reset))
        self.mediator.set_key(self, SetKeyCommand(command_type=SetKeyCommandType.ClearCallback))
        pass

    def SetupButtons(self):
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
        self.mediator.notify_mode_change(self, mode_name)
        pass

from enum import Enum

from inkkeys import Device, KeyCode


class SetKeyCommandType(Enum):
    Default = 0
    Callback = 1
    AssignKey = 2
    Reset = 3
    ClearCallback = 4


class SetKeyCommand:
    commandType: SetKeyCommandType = 0
    key = ""
    value = ""

    def __init__(self, command_type, key="", value=""):
        self.commandType = command_type
        self.key = key
        self.value = value


class KeyManager:
    device: Device = None

    def __init__(self, device):
        self.device = device

    def handle_command(self, command: SetKeyCommand):
        if command.commandType is SetKeyCommandType.Callback:
            self.device.registerCallback(command.value, command.key)
            pass

        if command.commandType is SetKeyCommandType.AssignKey:
            self.device.assignKey(command.key, command.value)
            pass

        if command.commandType is SetKeyCommandType.Reset:
            for keyCode in KeyCode:
                self.device.assignKey(keyCode, [])
            pass
        if command.commandType is SetKeyCommandType.ClearCallback:
            self.device.clearCallbacks()
            pass

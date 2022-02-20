from inkkeys import Device


class LedCommand:
    led = ""
    key = ""


class LedManager:
    device: Device = None

    def __init__(self, device):
        self.device = device

    def set_device(self, device):
        self.device = device

    def handle_command(self, command: LedCommand):
        self.device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

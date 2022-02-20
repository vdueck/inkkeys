# to clear the screen

from interfaces.IMode import *


class ClearPage(IMode):
    Title = "ClearPage"

    def activate(self):
        self.notify_display(DisplayUpdateCommand(CommandType.Text, "title", "", False, True))
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 2, "icons/white.png", False, False))
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 6, "icons/white.png", False, False))
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 3, "icons/white.png", False, False))
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 7, "icons/white.png", False, False))
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 4, "icons/white.png", False, False))
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 8, "icons/white.png", False, False))
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 5, "icons/white.png", False, False))
        self.notify_display(DisplayUpdateCommand(CommandType.Icon, 9, "icons/white.png", False, False))
        self.notify_display(DisplayUpdateCommand(update_display=True, full_refresh=True))

    def SetupJogRotation(self):
        pass

    def SetupJogButton(self):
        pass

    def poll(self):
        return False

    def animate(self):
        self.notify_led(LedCommand())

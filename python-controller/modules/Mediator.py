from __future__ import annotations
from abc import ABC

from modules.DisplayManager import DisplayUpdateCommand, DisplayManager
from modules.KeyManager import KeyManager, SetKeyCommand
from modules.LedManager import LedManager, LedCommand


class Mediator(ABC):
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """

    def notify_mode_change(self, sender: object, event: str) -> None:
        pass

    def notify_display(self, sender: object, command: DisplayUpdateCommand) -> None:
        pass

    def notify_led(self, sender: object, command: LedCommand) -> None:
        pass

    def set_key(self, sender: object, command: SetKeyCommand) -> None:
        pass


class ConcreteMediator(Mediator):
    active_mode = None

    def __init__(self, modes: object,
                 display_manager: DisplayManager,
                 key_manager: KeyManager,
                 led_manager: LedManager) -> None:

        self._key_manager = key_manager
        self._key_manager.mediator = self

        self._led_manager = led_manager
        self._led_manager.mediator = self

        self._display_manager = display_manager
        self._display_manager.mediator = self

        self._modes = modes
        for x in self._modes:
            self._modes[x].mediator = self

        pass

    def notify_mode_change(self, sender: object, event: str) -> None:
        if event == "Reset":
            self._init.activate()
        else:
            mode = self._modes[event]
            if mode is None:
                return

            if self.active_mode is not None and self.active_mode.Title != mode.Title:
                self.clear()
                self.active_mode.deactivate()

            mode.activate()
            self.active_mode = mode

    def set_key(self, sender: object, command: SetKeyCommand) -> None:
        self._key_manager.handle_command(command)

    def notify_led(self, sender: object, command: LedCommand) -> None:
        self._led_manager.handle_command(command)

    def notify_display(self, sender: object, command: DisplayUpdateCommand) -> None:
        self._display_manager.handle_command(command)

    def init(self):
        self.notify_mode_change(self, "Init")

    def clear(self):
        clear_page = self._modes["ClearPage"]
        if clear_page is not None:
            clear_page.activate()

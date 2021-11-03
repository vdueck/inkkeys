from __future__ import annotations
from abc import ABC

from modules.Display import DisplayUpdateCommand


class Mediator(ABC):
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """

    def notify(self, sender: object, event: str) -> None:
        pass

    def notify_display(self, sender: object, command: DisplayUpdateCommand) -> None:
        pass


class ConcreteMediator(Mediator):
    def __init__(self, manager: object, modes: object, display_manager: object) -> None:
        self._manager = manager
        self._manager.mediator = self
        self._display = display_manager
        self._display.mediator = self
        self._modes = modes
        for x in self._modes:
            x.mediator = self

    def notify(self, sender: object, event: str) -> None:
        if event == "Reset":
            self._manager.activate()
        else:
            mode = next((e for e in self._modes if e.Title == event), None)
            if mode is None:
                return
            mode.activate(self._manager.device)

    def notify_display(self, sender: object, command: DisplayUpdateCommand) -> None:
        self._display.update(command)

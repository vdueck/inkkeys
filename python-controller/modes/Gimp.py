from inkkeys import *


##########
## Gimp ## The Gimp example is similar to Blender, but we add a callback to pressing the jog dial to switch functions
##########


class ModeGimp:
    jogFunction = ""  # Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Gimp", inverted=True)  # Title

        # Button2 (top left)
        device.sendIconFor(2, "icons/fullscreen.png")
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS),
                                             event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B),
                                             event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT,
                                                   ActionCode.RELEASE), event(DeviceCode.KEYBOARD,
                                                                              KeyboardKeycode.KEY_Z)])  # Cut to selection (this shortcut appears to be language dependent, so you will probably need to change it)
        device.assignKey(KeyCode.SW2_RELEASE, [])

        # Button3 (left, second from top)
        device.sendIconFor(3, "icons/upc-scan.png")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS),
                                             event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B),
                                             event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT,
                                                   ActionCode.RELEASE), event(DeviceCode.KEYBOARD,
                                                                              KeyboardKeycode.KEY_I)])  # Cut to content (this shortcut appears to be language dependent, so you will probably need to change it)
        device.assignKey(KeyCode.SW3_RELEASE, [])

        # Button4 (left, third from top)
        device.sendIconFor(4, "icons/crop.png")
        device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS),
                                             event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B),
                                             event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT,
                                                   ActionCode.RELEASE), event(DeviceCode.KEYBOARD,
                                                                              KeyboardKeycode.KEY_L)])  # Canvas size (this shortcut appears to be language
        device.assignKey(KeyCode.SW4_RELEASE, [])

        # Button5 (bottom left)
        device.sendIconFor(5, "icons/arrows-angle-expand.png")
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS),
                                             event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B),
                                             event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT,
                                                   ActionCode.RELEASE), event(DeviceCode.KEYBOARD,
                                                                              KeyboardKeycode.KEY_S)])  # Resize (this shortcut appears to be language
        device.assignKey(KeyCode.SW5_RELEASE, [])

        # Button6 (top right)
        device.sendIconFor(6, "icons/clipboard-plus.png")
        device.assignKey(KeyCode.SW6_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT,
                                ActionCode.RELEASE)])  # Paste as new image
        device.assignKey(KeyCode.SW6_RELEASE, [])

        # Button7 (right, second from top)
        device.sendIconFor(7, "icons/layers-half.png")
        device.assignKey(KeyCode.SW7_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])  # New layer
        device.assignKey(KeyCode.SW7_RELEASE, [])

        # Button8 (right, third from top)
        device.sendIconFor(8, "icons/arrows-fullscreen.png")
        device.assignKey(KeyCode.SW8_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT,
                                ActionCode.RELEASE)])  # Zom to fill screen
        device.assignKey(KeyCode.SW8_RELEASE, [])

        # Button9 (bottom right)
        device.sendIconFor(9, "icons/dot.png")
        device.assignKey(KeyCode.SW9_PRESS, [])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW9_RELEASE, [])

        self.jogFunction = ""

        # This toggles the jog function and sets up key assignments and the label for the jog dial. It calls "updateDiplay()" if update is not explicitly set to False (for example if you need to update more parts of the display before updating it.)
        def toggleJogFunction(update=True):
            if self.jogFunction == "size":  # Tool opacity in GIMP
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Tool opacity")
                device.assignKey(KeyCode.JOG_CW,
                                 [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS),
                                  event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_COMMA),
                                  event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
                device.assignKey(KeyCode.JOG_CCW,
                                 [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS),
                                  event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PERIOD),
                                  event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
                self.jogFunction = "opacity"
                if update:
                    device.updateDisplay()
            else:  # Tool size in GIMP
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Tool size")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_BRACE)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT_BRACE)])
                self.jogFunction = "size"
                if update:
                    device.updateDisplay()

        # Button 1 / jog dial press
        device.registerCallback(toggleJogFunction, KeyCode.JOG_PRESS)  # Call "toggleJogFunction" if the dial is pressed
        device.assignKey(KeyCode.SW1_PRESS,
                         [])  # We do not send a key stroke when the dial is pressed, instead we use the callback.
        device.assignKey(KeyCode.SW1_RELEASE,
                         [])  # We still need to overwrite the assignment to clear previously set assignments.
        toggleJogFunction(False)  # We call toggleJogFunction to initially set the label and assignment
        device.updateDisplay()  # Everything has been sent to the display. Time to refresh it.

    def poll(self, device):
        return False  # Nothing to poll

    def animate(self, device):
        device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        device.clearCallbacks()  # Remove our callbacks if we switch to a different mode

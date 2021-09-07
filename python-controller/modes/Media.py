from inkkeys import *


# title: Media
# 1.    Play/Pause      |   Stop
# 2.    Vol++           |   Vol--
# 3.    Mute            |   Mic
# 4.    Cam             |    

class ModeMedia:

    def activate(self, device):
        device.sendTextFor("title", "Media", inverted=True)  # Title

        # Button1 (Jog dial press) - Pressing F to home camera
        device.sendTextFor(1, "<   Play/Pause   >")
        device.assignKey(KeyCode.SW1_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.PRESS)])  # Play/pause
        device.assignKey(KeyCode.SW1_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.RELEASE)])

        # Jog dial rotation - Pressing + (CW) or - (CCW) to zoom in and out
        device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, 1)])
        device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, -1)])

        # Button2 (top left) - supports (pressing C)
        device.sendIconFor(2, "icons/camera-reels.png")
        device.assignKey(KeyCode.SW2_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_C, ActionCode.PRESS)])  # Set view to camera
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_C, ActionCode.RELEASE)])

        # Button3 (left, second from top) - orientation (pressing O)
        device.sendIconFor(3, "icons/person-bounding-box.png")
        device.assignKey(KeyCode.SW3_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_O, ActionCode.PRESS)])  # Isolation view
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_O, ActionCode.RELEASE)])

        # Button4 (left, third from top) Print - ctrl + p
        device.sendIconFor(4, "icons/dot.png")
        device.assignKey(KeyCode.SW4_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.PRESS)])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW4_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.PRESS)])

        # Button5 (bottom left) - Go up one slice
        device.sendIconFor(5, "icons/dot.png")
        device.assignKey(KeyCode.SW5_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PAGE_UP, ActionCode.PRESS)])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW5_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PAGE_UP, ActionCode.PRESS)])

        # Button6 (top right) - edit supports (Pressing Ctrl + E)
        device.sendIconFor(6, "icons/aspect-ratio.png")
        device.assignKey(KeyCode.SW6_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.PRESS)])  # Center on selection
        device.assignKey(KeyCode.SW6_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.RELEASE)])

        # Button7 (right, second from top) - Turn knobs (ctrl + K)
        device.sendIconFor(7, "icons/collection.png")
        device.assignKey(KeyCode.SW7_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F12),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL,
                                ActionCode.RELEASE)])  # Render sequence
        device.assignKey(KeyCode.SW7_RELEASE, [])

        # Button8 (right, third from top) (printer list ctrl + shift + p)
        device.sendIconFor(8, "icons/dot.png")
        device.assignKey(KeyCode.SW8_PRESS, [])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW8_RELEASE, [])

        # Button9 (bottom right) - go down one layer
        device.sendIconFor(9, "icons/dot.png")
        device.assignKey(KeyCode.SW9_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PAGE_DOWN, ActionCode.PRESS)])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW9_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PAGE_DOWN, ActionCode.PRESS)])

        device.updateDisplay()

    def poll(self, device):
        return False  # No polling in this example

    def animate(self, device):
        device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        pass  # Nothing to clean up in this example

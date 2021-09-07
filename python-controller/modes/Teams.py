from inkkeys import *


######### One of the most complex examples. This controls OBS scenes and gives feedback about the current state. For this we
## OBS ## use the websocket plugin and address scenes and sources by their names (so, you need to adapt these to your setup).
######### We subscribe to OBS events and show the status on the key and LEDs.


class ModeTeams:

    def activate(self, device):
        device.sendTextFor("title", "Blender", inverted=True)  # Title

        # Button1 (Jog dial press)
        device.sendTextFor(1, "<   Play/Pause   >")
        device.assignKey(KeyCode.SW1_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.PRESS)])  # Play/pause
        device.assignKey(KeyCode.SW1_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.RELEASE)])

        # Jog dial rotation
        device.assignKey(KeyCode.JOG_CW,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT)])  # CW = Clock-wise, one frame forward
        device.assignKey(KeyCode.JOG_CCW, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT)])  # CCW = Counter clock-wise, one frame back

        # Button2 (top left)
        device.sendIconFor(2, "icons/camera-reels.png")
        device.assignKey(KeyCode.SW2_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_0, ActionCode.PRESS)])  # Set view to camera
        device.assignKey(KeyCode.SW2_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_0, ActionCode.RELEASE)])

        # Button3 (left, second from top)
        device.sendIconFor(3, "icons/person-bounding-box.png")
        device.assignKey(KeyCode.SW3_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.PRESS)])  # Isolation view
        device.assignKey(KeyCode.SW3_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.RELEASE)])

        # Button4 (left, third from top)
        device.sendIconFor(4, "icons/dot.png")
        device.assignKey(KeyCode.SW4_PRESS, [])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW4_RELEASE, [])

        # Button5 (bottom left)
        device.sendIconFor(5, "icons/dot.png")
        device.assignKey(KeyCode.SW5_PRESS, [])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW5_RELEASE, [])

        # Button6 (top right)
        device.sendIconFor(6, "icons/aspect-ratio.png")
        device.assignKey(KeyCode.SW6_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.PRESS)])  # Center on selection
        device.assignKey(KeyCode.SW6_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.RELEASE)])

        # Button7 (right, second from top)
        # Button4 (left, third from top)
        device.sendIconFor(7, "icons/collection.png")
        device.assignKey(KeyCode.SW7_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F12),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL,
                                ActionCode.RELEASE)])  # Render sequence
        device.assignKey(KeyCode.SW7_RELEASE, [])

        # Button8 (right, third from top)
        device.sendIconFor(8, "icons/dot.png")
        device.assignKey(KeyCode.SW8_PRESS, [])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW8_RELEASE, [])

        # Button9 (bottom right)
        device.sendIconFor(9, "icons/dot.png")
        device.assignKey(KeyCode.SW9_PRESS, [])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW9_RELEASE, [])

        device.updateDisplay()

    def poll(self, device):
        return False  # No polling in this example

    def animate(self, device):
        device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        pass  # Nothing to clean up in this example

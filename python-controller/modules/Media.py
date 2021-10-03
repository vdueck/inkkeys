from inkkeys import *


# title: Media
# 1.    Play/Pause      | 5.  Stop
# 2.    Vol++           | 6.  Vol--
# 3.    Mute            | 7.  Mic
# 4.    Cam             | 8.
# Jag Press      :
# Jag Jag Rotate
#   left         :
#   right        :

class ModeMedia:

    def activate(self, device):
        device.sendTextFor("title", "Media", inverted=True)  # Title

        self.SetupJogButton(device)
        self.SetupJogRotation(device)

        self.SetupButton1(device)
        self.SetupButton2(device)
        self.SetupButton3(device)
        self.SetupButton4(device)
        self.SetupButton5(device)
        self.SetupButton6(device)
        self.SetupButton7(device)
        self.SetupButton8(device)

        device.updateDisplay()

    def SetupButton1(self, device):
        # Button1 (top left)
        device.sendIconFor(2, "icons/play.png")
        key = ConsumerKeycode.MEDIA_PLAY_PAUSE
        device.assignKey(KeyCode.SW2_PRESS,
                         [event(DeviceCode.KEYBOARD, key, ActionCode.PRESS)])  # Set view to camera
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, key, ActionCode.RELEASE)])

    def SetupButton2(self, device):
        # Button3 (left, second from top)
        device.sendIconFor(3, "icons/volume-up.png")
        device.assignKey(KeyCode.SW3_PRESS,
                         [event(DeviceCode.KEYBOARD, ConsumerKeycode.MEDIA_VOLUME_UP,
                                ActionCode.PRESS)])  # Isolation view
        device.assignKey(KeyCode.SW3_RELEASE,
                         [event(DeviceCode.KEYBOARD, ConsumerKeycode.MEDIA_VOLUME_UP, ActionCode.RELEASE)])

    def SetupButton3(self, device):
        # Button4 (left, third from top)
        device.sendIconFor(4, "icons/dot.png")
        device.assignKey(KeyCode.SW4_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.PRESS)])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW4_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.PRESS)])

    def SetupButton4(self, device):
        # Button5 (bottom left)
        device.sendIconFor(5, "icons/dot.png")
        device.assignKey(KeyCode.SW5_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PAGE_UP, ActionCode.PRESS)])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW5_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PAGE_UP, ActionCode.PRESS)])

    def SetupButton5(self, device):
        # Button6 (top right)
        device.sendIconFor(6, "icons/aspect-ratio.png")
        device.assignKey(KeyCode.SW6_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.PRESS)])  # Center on selection
        device.assignKey(KeyCode.SW6_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.RELEASE)])

    def SetupButton6(self, device):
        # Button7 (right, second from top)
        device.sendIconFor(7, "icons/collection.png")
        device.assignKey(KeyCode.SW7_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F12),
                          event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL,
                                ActionCode.RELEASE)])  # Render sequence
        device.assignKey(KeyCode.SW7_RELEASE, [])

    def SetupButton7(self, device):
        # Button8 (right, third from top)
        device.sendIconFor(8, "icons/dot.png")
        device.assignKey(KeyCode.SW8_PRESS, [])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW8_RELEASE, [])

    def SetupButton8(self, device):
        # Button9 (bottom right)
        device.sendIconFor(9, "icons/dot.png")
        device.assignKey(KeyCode.SW9_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PAGE_DOWN, ActionCode.PRESS)])  # Not used, set to nothing.
        device.assignKey(KeyCode.SW9_RELEASE,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PAGE_DOWN, ActionCode.PRESS)])

    def SetupJogRotation(self, device):
        # Jog dial rotation - Pressing + (CW) or - (CCW) to zoom in and out
        device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, -1)])
        device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, 1)])

    def SetupJogButton(self, device):
        # Button1 (Jog dial press) - Pressing F to home camera
        device.sendTextFor(1, "<   Play/Pause   >")
        device.assignKey(KeyCode.SW1_PRESS,
                         [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.PRESS)])  # Play/pause
        device.assignKey(KeyCode.SW1_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.RELEASE)])

    def poll(self, device):
        return False  # No polling in this example

    def animate(self, device):
        device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        pass  # Nothing to clean up in this example

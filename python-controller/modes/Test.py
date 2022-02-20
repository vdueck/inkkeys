from inkkeys import *
from interfaces.IMode import *


def Function():
    print("Button 1 pressed")


class Test(IMode):
    Title = "Test"

    def activate(self, device):
        device.sendTextFor("title", IMode.Title, inverted=True)
        self.SetupButtons(device)
        device.updateDisplay()

    ## first row
    def SetupButton1(self, device):
        # Button1 (top left)
        # Register Callback
        device.registerCallback(Function(), KeyCode.SW1_PRESS)

    def SetupButton5(self, device):
        # Button5 (top right)
        device.registerCallback(Function(), KeyCode.SW5_PRESS)

    ## second row
    def SetupButton2(self, device):
        # Button3 (left, second from top)
        device.sendIconFor(3, "icons/volume-down.png")
        key = ConsumerKeycode.MEDIA_VOLUME_DOWN
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    def SetupButton6(self, device):
        # Button6(right, second from top)
        device.sendIconFor(7, "icons/volume-up.png")
        key = ConsumerKeycode.MEDIA_VOLUME_UP
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    ## third row
    def SetupButton3(self, device):
        # Button4 (left, third from top)
        device.sendIconFor(4, "icons/volume-mute.png")
        key = ConsumerKeycode.MEDIA_VOLUME_MUTE
        device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW4_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    def SetupButton7(self, device):
        # Button8 (right, third from top)
        device.sendIconFor(8, "icons/mic-mute.png")
        key = ConsumerKeycode.MEDIA_VOL_MUTE
        device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW8_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    ## fourth row
    def SetupButton4(self, device):
        # Button5 (bottom left)
        device.sendIconFor(5, "icons/chevron-double-left.png")
        key = ConsumerKeycode.MEDIA_REWIND
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW5_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    def SetupButton8(self, device):
        # Button9 (bottom right)
        device.sendIconFor(9, "icons/chevron-double-right.png")
        key = ConsumerKeycode.MEDIA_FAST_FORWARD
        device.assignKey(KeyCode.SW9_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW9_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    ## Jog
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

    ## other methods
    def poll(self, device):
        return False  # No polling in this example

    def animate(self, device):
        device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        pass  # Nothing to clean up in this example

####
#### Templates
####
# device.assignKey(KeyCode.SW7_PRESS,
#                  [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS),
#                   event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F12),
#                   event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL,
#                         ActionCode.RELEASE)])  # Render sequence
# device.assignKey(KeyCode.SW7_RELEASE, [])

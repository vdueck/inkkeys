from inkkeys import *
from modules.IMode import *


# title: Media
# 1.    Play/Pause      | 5.
# 2.    Vol++           | 6.  Vol--
# 3.    Mute            | 7.
# 4.    Rewind          | 8. Fastfoward
# Jag Press      :
# Jag Jag Rotate
#   left         :
#   right        :


class Media(IMode):
    Title = "Media"

    def activate(self, device):
        super().activate(device)
        self.mediator.notify_display(self, DisplayUpdateCommand(CommandType.Text, "title", self.Title, False, True))
        self.SetupButtons()

    ## first row
    def SetupButton1(self):
        # Button1 (top left)
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 2, "icons/play.png", False, False))
        key = ConsumerKeycode.MEDIA_PLAY_PAUSE
        # app = "/home/vd/.local/share/JetBrains/Toolbox/apps/Rider/ch-0/212.5284.64/bin/rider.sh"
        # device.registerCallback(self.StartAppInUsrBin(app), KeyCode.SW2_PRESS)
        self.device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, key, ActionCode.PRESS)])
        self.device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, key, ActionCode.RELEASE)])

    def SetupButton5(self):
        # Button5 (top right)
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 6, "icons/dot.png", False, False))
        self.device.assignKey(KeyCode.SW6_PRESS, [
            event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.PRESS)])
        self.device.assignKey(KeyCode.SW6_RELEASE,
                              [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.RELEASE)])

    ## second row
    def SetupButton2(self):
        # Button3 (left, second from top)
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 3, "icons/volume-down.png", False, False))
        key = ConsumerKeycode.MEDIA_VOLUME_DOWN
        self.device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        self.device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    def SetupButton6(self):
        # Button6(right, second from top)
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 7, "icons/volume-up.png", False, False))
        key = ConsumerKeycode.MEDIA_VOLUME_UP
        self.device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        self.device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    ## third row
    def SetupButton3(self):
        # Button4 (left, third from top)
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 7, "icons/volume-mute.png", False, False))
        key = ConsumerKeycode.MEDIA_VOLUME_MUTE
        self.device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        self.device.assignKey(KeyCode.SW4_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    def SetupButton7(self):
        # Button8 (right, third from top)
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 8, "icons/mic-mute.png", False, False))
        key = ConsumerKeycode.MEDIA_VOL_MUTE
        self.device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        self.device.assignKey(KeyCode.SW8_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    ## fourth row
    def SetupButton4(self):
        # Button5 (bottom left)
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 5, "icons/chevron-double-left.png", False,
                                                          False))
        key = ConsumerKeycode.MEDIA_REWIND
        self.device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        self.device.assignKey(KeyCode.SW5_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    def SetupButton8(self):
        # Button9 (bottom right)
        self.mediator.notify_display(self,
                                     DisplayUpdateCommand(CommandType.Icon, 9, "icons/chevron-double-right.png", False,
                                                          False))
        key = ConsumerKeycode.MEDIA_FAST_FORWARD
        self.device.assignKey(KeyCode.SW9_PRESS, [event(DeviceCode.CONSUMER, key, ActionCode.PRESS)])
        self.device.assignKey(KeyCode.SW9_RELEASE, [event(DeviceCode.CONSUMER, key, ActionCode.RELEASE)])

    ## Jog
    def SetupJogRotation(self):
        # Jog dial rotation - Pressing + (CW) or - (CCW) to zoom in and out
        self.device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, -1)])
        self.device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, 1)])

    def SetupJogButton(self):
        # Button1 (Jog dial press)
        self.device.registerCallback(self.ActivateMode("Init"), KeyCode.JOG_PRESS)
        # self.device.registerCallback(self.ReturnToModeManagement(), KeyCode.JOG_PRESS)
        # device.sendTextFor(1, "<   Play/Pause   >")
        # device.assignKey(KeyCode.SW1_PRESS,
        #                 [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.PRESS)])  # Play/pause
        # device.assignKey(KeyCode.SW1_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F, ActionCode.RELEASE)])

    ## other methods
    def poll(self):
        return False  # No polling in this example

    def animate(self):
        self.device.fadeLeds()  # No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self):
        self.device.clearCallback()
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

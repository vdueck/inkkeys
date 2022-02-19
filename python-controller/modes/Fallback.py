############## This mode is used as a fallback and a much more complex example than Gimp. It also uses a switchable Jog dial,
## Fallback ## but most of its functions give a feedback via LED. Also, we use MQTT (via a separately defined class) to get
############## data from a CO2 sensor and control a light (both including feedback)
from colorsys import hsv_to_rgb
from math import floor, ceil

from pulsectl import pulsectl

from inkkeys import *


class ModeFallback:
    jogFunction = ""  # Keeps track of the currently selected function of the jog dial
    mqtt = None  # The MQTT object defined in mqtt.py. It will be passed when this class is contructed and kept in this variable
    lightState = None  # Current state of the lights in my office. (Keeping track to know when to update the screen)
    demoActive = False  # We have a demo button and this keeps track whether the demo mode is active, so we know when to update the screen

    def __init__(self, mqtt):
        self.mqtt = mqtt

    def activate(self, device):
        device.sendTextFor("title", "Default", inverted=True)  # Title

        ### Buttons 2, 3, 6 and 7 are media controls ###

        device.sendIconFor(2, "icons/play.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW2_PRESS,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_PLAY_PAUSE, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW2_RELEASE,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_PLAY_PAUSE, ActionCode.RELEASE)])
        device.sendIconFor(3, "icons/skip-start.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_PREV, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW3_RELEASE,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_PREV, ActionCode.RELEASE)])

        device.sendIconFor(6, "icons/stop.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_STOP, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW6_RELEASE,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_STOP, ActionCode.RELEASE)])
        device.sendIconFor(7, "icons/skip-end.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_NEXT, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW7_RELEASE,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_NEXT, ActionCode.RELEASE)])

        ### Buttons 5 and 9 are shortcuts to applications ###

        device.sendIconFor(5, "icons/envelope.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW5_PRESS,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_EMAIL_READER, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW5_RELEASE,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_EMAIL_READER, ActionCode.RELEASE)])
        device.sendIconFor(9, "icons/calculator.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW9_PRESS,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_CALCULATOR, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW9_RELEASE,
                         [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_CALCULATOR, ActionCode.RELEASE)])

        ### Button 4 controls the light in my office and displays its state ###

        def toggleLight():
            target = not self.lightState
            self.mqtt.setLight(target)
            self.lightState = target
            self.showLightState(device)

        self.lightState = self.mqtt.getLight
        self.showLightState(device, False)

        device.assignKey(KeyCode.SW4_PRESS, [])
        device.assignKey(KeyCode.SW4_RELEASE, [])
        device.registerCallback(toggleLight, KeyCode.SW4_PRESS)

        ### Button 8 set display and LEDs to a demo state (only used for videos and pictures of the thing)
        def toggleDemo():
            if self.demoActive:
                self.demoActive = False
                img = Image.new("1", (device.dispW, device.dispH), color=1)
                device.sendImage(0, 0, img)
                self.activate(device)  # Recreate the screen content after the demo
            else:
                self.demoActive = True
                self.activate(
                    device)  # Recreate the screen because with demo active, the buttons will align differently to give room for "there.oughta.be"
                text = "there.oughta.be/a/macro-keyboard"
                font = ImageFont.truetype("arial.ttf", 17)
                w, h = font.getsize(text);
                x = (device.dispW - h) // 2
                x8 = floor(x / 8) * 8  # needs to be a multiple of 8
                h8 = ceil((h + x - x8) / 8) * 8  # needs to be a multiple of 8
                img = Image.new("1", (w, h8), color=1)
                d = ImageDraw.Draw(img)
                d.text((0, x - x8), text, font=font, fill=0)
                device.sendImage(x8, (device.dispH - w) // 2, img.transpose(Image.ROTATE_90))
                device.updateDisplay(True)

        device.registerCallback(toggleDemo, KeyCode.SW8_PRESS)
        device.sendIconFor(8, "icons/emoji-sunglasses.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW8_PRESS, [])
        device.assignKey(KeyCode.SW8_RELEASE, [])

        ### The jog wheel can be pressed to switch between three functions: Volume control, mouse wheel, arrow keys left/right ###

        def showVolume(n):
            with pulsectl.Pulse('inkkeys') as pulse:
                sinkList = pulse.sink_list()
                name = pulse.server_info().default_sink_name
                for sink in sinkList:
                    if sink.name == name:
                        vol = sink.volume.value_flat
                off = 0x00ff00
                on = 0xff0000
                leds = [on if vol > i / (device.nLeds - 1) else off for i in range(device.nLeds)]
                device.setLeds(leds)

        self.jogFunction = ""

        def toggleJogFunction(update=True):
            if self.jogFunction == "wheel":
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Arrow Keys")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT)])
                self.jogFunction = "arrow"
                if update:
                    device.updateDisplay()
            elif self.jogFunction == "arrow":
                device.sendTextFor(1, "Volume")
                device.registerCallback(showVolume, KeyCode.JOG)
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_VOL_UP)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_VOL_DOWN)])
                self.jogFunction = "volume"
                if update:
                    device.updateDisplay()
            else:
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Mouse Wheel")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, 1)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, -1)])
                self.jogFunction = "wheel"
                if update:
                    device.updateDisplay()

        device.registerCallback(toggleJogFunction, KeyCode.JOG_PRESS)
        device.assignKey(KeyCode.SW1_PRESS, [])
        device.assignKey(KeyCode.SW1_RELEASE, [])
        toggleJogFunction(False)

        ### All set, let's update the display ###

        device.updateDisplay()

    def poll(self, device):
        if not self.demoActive:
            co2 = self.mqtt.getCO2()
            if co2 != None and co2 > 1000:
                leds = [0x0000ff for i in range(device.nLeds)]
                device.setLeds(leds)
            light = self.mqtt.getLight()
            if light != self.lightState:
                self.lightState = light
                self.showLightState(device)
        return 10  # Since we only retrieve the current state from the Mqtt class, the 10 seconds do not really control how often the value is querries but how often we react to it. For the CO2 warning, this is a not too intrusive blue flash every 10 seconds and a 10 second delay to update the light state if it has been switched from somewhere else (rare) seems reasonable, too.

    # Called to update the icon of button 4, showing the state of the office light (as if I couldn't see it in the real room, but it is a nice touch to update the display accordingly)
    def showLightState(self, device, update=True):
        if self.lightState:
            device.sendIconFor(4, "icons/lightbulb.png", centered=(not self.demoActive))
        else:
            device.sendIconFor(4, "icons/lightbulb-off.png", centered=(not self.demoActive))
        if update:
            device.updateDisplay()

    def animate(self, device):
        if self.demoActive:  # In demo mode, we animate the LEDs here

            def rgbTupleToInt(rgb):
                return (int(rgb[0] * 255) << 16) | (int(rgb[1] * 255) << 8) | int(rgb[2] * 255)

            t = time.time()
            leds = [rgbTupleToInt(hsv_to_rgb(t + i / device.nLeds, 1, 1)) for i in range(device.nLeds)]
            device.setLeds(leds)
        else:  # If not in demo mode, we call "fadeLeds" to create a fade animation for any color set anywhere in this mode
            device.fadeLeds()

    def deactivate(self, device):
        device.clearCallbacks()  # Clear our callbacks if we switch to a different mode

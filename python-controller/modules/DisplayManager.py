import time
from PIL import Image, ImageDraw, ImageOps, ImageFont
from enum import Enum
from inkkeys import Device, CommandCode, RefreshTypeCode


class CommandType(Enum):
    Default = 0
    Text = 1
    Icon = 2


class DisplayUpdateCommand:
    command_type = CommandType.Default
    position = ""
    value = ""
    full_refresh = False
    inverted = False
    update_display = False

    def __init__(self, command_type=CommandType.Default,
                 position="",
                 value="",
                 full_refresh=False,
                 inverted=False,
                 update_display=False):
        self.command_type = command_type
        self.position = position
        self.value = value
        self.full_refresh = full_refresh
        self.inverted = inverted
        self.update_display = update_display


class DisplayManager:
    device: Device = None

    def set_device(self, device):
        self.device = device

    imageBuffer = []
    bannerHeight = 12  # Defines the height of top and bottom banner

    def sendImage(self, x, y, image):
        self.imageBuffer.append({"x": x, "y": y, "image": image.copy()})
        w, h = image.size
        data = image.convert("1").rotate(180).tobytes()
        self.device.sendToDevice(CommandCode.DISPLAY.value + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h))
        self.device.sendBinaryToDevice(data)
        return True

    def resendImageData(self):
        for part in self.imageBuffer:
            image = part["image"]
            x = part["x"]
            y = part["y"]
            w, h = image.size
            data = image.convert("1").rotate(180).tobytes()
            self.device.sendToDevice(
                CommandCode.DISPLAY.value + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h))
            self.device.sendBinaryToDevice(data)
        self.device.imageBuffer = []

    def updateDisplay(self, fullRefresh=False, timeout=5):
        with self.device.awaitingResponseLock:
            start = time.time()
            self.device.sendToDevice(CommandCode.REFRESH.value + " " + (
                RefreshTypeCode.FULL.value if fullRefresh else RefreshTypeCode.PARTIAL.value))
            line = self.device.readFromDevice()
            while line != "ok":
                if time.time() - start > timeout:
                    return False
                if line == None:
                    time.sleep(0.1)
                    line = self.device.readFromDevice()
                    continue
                line = self.device.readFromDevice()
            self.resendImageData()
            self.device.sendToDevice(CommandCode.REFRESH.value + " " + RefreshTypeCode.OFF.value)
            line = self.device.readFromDevice()
            while line != "ok":
                if time.time() - start > timeout:
                    return False
                if line == None:
                    time.sleep(0.1)
                    line = self.device.readFromDevice()
                    continue
                line = self.device.readFromDevice()

    def getAreaFor(self, function):
        if function == "title":
            return (0, self.device.dispH - self.bannerHeight, self.device.dispW, self.bannerHeight)
        elif function == 1:
            return (0, 0, self.device.dispW, self.bannerHeight)
        elif function <= 5:
            return (
                self.device.dispW // 2, (5 - function) * self.device.dispH // 4 + self.bannerHeight,
                self.device.dispW // 2,
                self.device.dispH // 4 - 2 * self.bannerHeight)
        else:
            return (0, (9 - function) * self.device.dispH // 4 + self.bannerHeight, self.device.dispW // 2,
                    self.device.dispH // 4 - 2 * self.bannerHeight)

    def sendImageFor(self, function, image):
        x, y, w, h = self.getAreaFor(function)
        if (w, h) != image.size:
            if self.debug:
                print("Rescaling image from " + str(image.size) + " to " + str((w, h)) + ".")
            image = image.resize((w, h))
        self.sendImage(x, y, image)

    def sendTextFor(self, function, text, subtext="", inverted=False):
        x, y, w, h = self.getAreaFor(function)
        img = Image.new("1", (w, h), color=(0 if inverted else 1))
        d = ImageDraw.Draw(img)
        font1 = ImageFont.truetype("font/Munro.ttf", 10)
        wt1, ht1 = font1.getsize(text);
        font2 = ImageFont.truetype("font/MunroSmall.ttf", 10)
        wt2, ht2 = font2.getsize_multiline(subtext);
        if function == 1 or function == "title":
            position1 = ((w - wt1) / 2, (h - ht1 - (
                0.5 if function == "title" else 0)) / 2)  # Center jog wheel and title label (the title get's small -0.5 nudge for rounding to prefer a top alignment)
            position2 = None
        elif function < 6:
            d.line([(0, h / 2), (wt1, h / 2)], fill=(1 if inverted else 0))
            position1 = (0, h / 2 - ht1 - 2)  # Align left
            position2 = (0, h / 2 - 1)
            align = "left"
        else:
            d.line([(w, h / 2), (w - wt1, h / 2)], fill=(1 if inverted else 0))
            position1 = (w - wt1, h / 2 - ht1 - 2)  # Align right
            position2 = (w - wt2, h / 2 - 1)
            align = "right"
        d.text(position1, text, font=font1, fill=(1 if inverted else 0))
        if position2 != None and subtext != None:
            d.multiline_text(position2, subtext, font=font2, align=align, spacing=-2, fill=(1 if inverted else 0))
        self.sendImageFor(function, img)

    def sendIconFor(self, function, icon, inverted=False, centered=True, marked=False, crossed=False):
        x, y, w, h = self.getAreaFor(function)
        img = Image.new("1", (w, h), color=(0 if inverted else 1))
        imgIcon = Image.open(icon).convert("RGB")
        if inverted:
            imgIcon = ImageOps.invert(imgIcon)
        wi, hi = imgIcon.size
        if function < 6:
            pos = ((w - wi) // 2 if centered else 0, (h - hi) // 2)
        else:
            pos = ((w - wi) // 2 if centered else (w - wi), (h - hi) // 2)
        img.paste(imgIcon, pos)

        if marked:
            imgMarker = Image.open(
                "icons/chevron-compact-right.png" if function < 6 else "icons/chevron-compact-left.png")
            wm, hm = imgMarker.size
            img.paste(imgMarker, (-16, (h - hm) // 2) if function < 6 else (w - wm + 16, (h - hm) // 2),
                      mask=ImageOps.invert(imgMarker.convert("RGB")).convert("1"))

        if crossed:
            d = ImageDraw.Draw(img)
            d.line([pos[0] + 5, pos[1] + 5, pos[0] + wi - 5, pos[1] + hi - 5], width=3)
            d.line([pos[0] + 5, pos[1] + hi - 5, pos[0] + wi - 5, pos[1] + 5], width=3)

        self.sendImage(x, y, img)

    def handle_update_command(self, command: DisplayUpdateCommand):
        if command.command_type is CommandType.Icon:
            self.sendIconFor(command.position, command.value, inverted=command.inverted)

        if command.command_type is CommandType.Text:
            self.sendTextFor(command.position, command.value, inverted=command.inverted)

        if command.update_display:
            self.updateDisplay()

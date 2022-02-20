from .protocol import *
import serial
import time
from threading import Lock
from serial import SerialException  # Serial functions

CHUNK_SIZE = 100


class Device:
    ser = None
    inbuffer = ""

    awaitingResponseLock = Lock()

    testmode = False
    nLeds = 0
    dispW = 0
    dispH = 0
    rotFactor = 0
    rotCircleSteps = 0

    # bannerHeight = 12  # Defines the height of top and bottom banner

    # imageBuffer = []

    callbacks = {}  # This object stores callback functions that react directly to a keypress reported via serial

    ledState = None  # Current LED status, so we can animate them over time
    ledTime = None  # Last time LEDs were set

    debug = False;

    def connect(self, dev):
        print("Connecting to ", dev, ".")
        self.ser = serial.Serial(dev, 115200, timeout=1, write_timeout=1)
        if not self.requestInfo(3):
            self.disconnect()
            return False
        if self.testmode:
            print("Connection to ", self.ser.name,
                  " was successfull, but the device is running the hardware test firmware, which cannot be used for anything but testing. Please flash the proper inkkeys firmware to use it.")
            return False
        print("Connected to ", self.ser.name, ".")
        return True

    def disconnect(self):
        if self.ser != None:
            self.ser.close()
            self.ser = None

    def sendToDevice(self, command):
        if self.debug:
            print("Sending: " + command)
        self.ser.write((command + "\n").encode())

    def sendBinaryToDevice(self, data):
        if self.debug:
            print("Sending " + str(len(data)) + " bytes of binary data.")
        try:
            # Send binary data in chunks to prevent killing the serial connection
            start = time.time()
            endIx = CHUNK_SIZE
            startIx = 0
            while (startIx < len(data)):
                self.ser.write(data[startIx:endIx])
                # if self.debug:
                #    print(data[startIx:endIx].hex())
                startIx = startIx + CHUNK_SIZE
                endIx = endIx + CHUNK_SIZE
            if self.debug:
                print("Data sent.")
        except SerialException as e:
            print("Serial error: ", e)

    def readFromDevice(self):
        if self.ser.in_waiting > 0:
            # self.inbuffer += self.ser.read(self.ser.in_waiting).decode().replace("\r", "")
            self.inbuffer += self.ser.read(self.ser.in_waiting).decode("ISO-8859-16").replace("\r", "")
        chunks = self.inbuffer.split("\n", 1)
        if len(chunks) > 1:
            cmd = chunks[0]
            self.inbuffer = chunks[1]
            if self.debug:
                print("Received: " + cmd)
            return cmd
        return None

    def poll(self):
        with self.awaitingResponseLock:
            input = self.readFromDevice()
        if input != None:
            if input[0] == KeyCode.JOG.value and (input[1:].isdecimal() or (input[1] == '-' and input[2:].isdecimal())):
                if input == "R1" and "R+" in self.callbacks:
                    self.callbacks["R+"]()
                if input == "R-1" and "R-" in self.callbacks:
                    self.callbacks["R-"]()
                if KeyCode.JOG.value in self.callbacks:
                    self.callbacks[KeyCode.JOG.value](int(input[1:]))
            elif input in self.callbacks:
                self.callbacks[input]()

    def registerCallback(self, cb, key):
        self.callbacks[key.value] = cb

    def clearCallback(self, key):
        if key.value in self.callbacks:
            del self.callbacks[key.value]

    def clearCallbacks(self):
        self.callbacks = {}

    def assignKey(self, key, sequence):
        self.sendToDevice(
            CommandCode.ASSIGN.value + " " + key.value + (" " + " ".join(sequence) if len(sequence) > 0 else ""))

    # Blanks out the display
    def resetDisplay(self):
        self.sendToDevice(CommandCode.REFRESH.value + " " + RefreshTypeCode.RESET.value)

    def sendLed(self, colors):
        self.sendToDevice(CommandCode.LED.value + " " + " ".join(colors))

    def setLeds(self, leds):
        ledStr = ['{:06x}'.format(i) for i in leds]
        self.ledTime = time.time()
        self.ledState = leds
        self.sendLed(ledStr)

    def fadeLeds(self):
        if self.ledState == None:
            return
        p = (3.5 - (time.time() - self.ledTime)) / 0.5  # Stay on for 3 seconds and then fade out over 0.5 seconds
        if p >= 1:
            return
        if p <= 0:
            self.ledState = None
            self.sendLed(["000000" for i in range(self.nLeds)])
            return
        dimmedLeds = [
            (int((i & 0xff0000) * p) & 0xff0000) | (int((i & 0xff00) * p) & 0xff00) | (int((i & 0xff) * p) & 0xff) for i
            in self.ledState]
        ledStr = ['{:06x}'.format(i) for i in dimmedLeds]
        self.sendLed(ledStr)

    def requestInfo(self, timeout):
        with self.awaitingResponseLock:
            print("Requesting device info...")
            start = time.time()
            self.sendToDevice(CommandCode.INFO.value)
            line = self.readFromDevice()
            while line != "Inkkeys":
                if time.time() - start > timeout:
                    return False
                if line == None:
                    time.sleep(0.1)
                    line = self.readFromDevice()
                    continue
                print("Skipping: ", line)
                line = self.readFromDevice()
            print("Header found. Waiting for infos...")
            line = self.readFromDevice()
            while line != "Done":
                if time.time() - start > timeout:
                    return False
                if line == None:
                    time.sleep(0.1)
                    line = self.readFromDevice()
                    continue
                if line.startswith("TEST "):
                    self.testmode = line[5] != "0"
                elif line.startswith("N_LED "):
                    self.nLeds = int(line[6:])
                elif line.startswith("DISP_W "):
                    self.dispW = int(line[7:])
                elif line.startswith("DISP_H "):
                    self.dispH = int(line[7:])
                elif line.startswith("ROT_CIRCLE_STEPS "):
                    self.rotCircleSteps = int(line[17:])
                else:
                    print("Skipping: ", line)
                line = self.readFromDevice()
            print("End of info received.")
            #            print("Testmode: ", self.testmode)
            #            print("Number of LEDs: ", self.nLeds)
            #            print("Display width: ", self.dispW)
            #            print("Display height: ", self.dispH)
            #            print("Rotation circle steps: ", self.rotCircleSteps)
            return True

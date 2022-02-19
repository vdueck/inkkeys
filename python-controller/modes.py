# In here, the logic of the different modes are defined.
# Each mode has to implement four functions (use "pass" if not needed):
#
# - activate
# Called when the mode becomes active. Usually used to set up static key assignment and icons
# - poll
# Called periodically and typically used to poll a state which you need to monitor. At the end you have to return an interval in seconds before the function is to be called again - otherwise it is not called a second time
# - animate
# Called up to 30 times per second, used for LED animation
# - deactivate
# Called when the mode becomes inactive. Used to clean up callback functions and images on the screen that are outside commonly overwritten areas.

# To avoid multiple screen refreshs, the modules usually do not clean-up the display when being deactivvated. Instead, each module is supposed to set at least the area corresponding to each button (even if it needs to be set to white if unused).

from inkkeys import *
import time
from threading import Timer
from math import ceil, floor
from PIL import Image, ImageDraw, ImageFont
from colorsys import hsv_to_rgb

# Optional libraries you might want to remove if you do not require them.
import pulsectl  # Get volume level in Linux, pip3 install pulsectl
from obswebsocket import obsws, requests, \
    events  # Control OBS. This requires the websocket plugin in OBS (https://github.com/Palakis/obs-websocket) and the Python library obs-websocket-py (pip3 install obs-websocket-py, https://github.com/Elektordi/obs-websocket-py)







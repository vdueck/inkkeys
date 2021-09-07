from obswebsocket import requests

from inkkeys import *


class ModeOBS:
    ws = None  # Websocket instance
    currentScene = None  # Keep track of current scene

    # Scenes assigned to buttons with respective icons.
    scenes = [ \
        {"name": "Moderation", "icon": "icons/card-image.png", "button": 2}, \
        {"name": "Closeup", "icon": "icons/person-square.png", "button": 3}, \
        {"name": "Slides", "icon": "icons/easel.png", "button": 4}, \
        {"name": "Video-Mute", "icon": "icons/camera-video-off.png", "button": 5}, \
        ]

    # State of sources within scenes. "items" is an array of scene/item combinations to keep track of items that need to be switched on multiple scenes simultaneously, so you can mute all mics in all scenes and switch scenes without an unpleasant surprise. The current state is tracked in this object ("current")
    states = [ \
        {"items": [("Moderation", "Phone"), ("Closeup", "Phone"), ("Slides", "Phone")], "icon": "icons/phone.png",
         "button": 7, "current": True}, \
        {"items": [("Slides", "Cam: Closeup")], "icon": "icons/pip.png", "button": 8, "current": True}, \
        {"items": [("Moderation", "Mic: Moderation"), ("Closeup", "Mic: Closeup"), ("Slides", "Mic: Closeup")],
         "icon": "icons/mic.png", "button": 9, "current": True}, \
        ]

    # Switch to scene with name "name"
    def setScene(self, name):
        self.ws.call(requests.SetCurrentScene(name))

    # Toggle source visibility as defined in a state (see states above)
    def toggleState(self, state):
        visible = not state["current"]
        for item in state["items"]:
            self.ws.call(requests.SetSceneItemProperties(item[1], scene_name=item[0], visible=visible))

    # Generates a callback function which in turn calls "setScene" with the fixed scene "name" without requiring a parameter
    def getSetSceneCallback(self, name):
        return lambda: self.setScene(name)

    # Generates a callback function which in turn calls "toggleState" with a fixed "state" object without requiting a parameter
    def getToggleStateCallback(self, state):
        return lambda: self.toggleState(state)

    # Updates the buttons associated with scenes. Unless "init" is set to true, it only updates changed parts of the display and returns True if anything has changed so that the calling function should call updateDisplay()
    def updateSceneButtons(self, device, newScene, init=False):
        if self.currentScene == newScene:
            return False
        for scene in self.scenes:
            if (init and newScene != scene["name"]) or self.currentScene == scene["name"]:
                device.sendIconFor(scene["button"], scene["icon"], centered=True)
            elif newScene == scene["name"]:
                device.sendIconFor(scene["button"], scene["icon"], centered=True, marked=True)
        self.currentScene = newScene
        return True

    # Updates the buttons associated with states. Unless "init" is set to true, it only updates changed parts of the display and returns True if anything has changed so that the calling function should call updateDisplay()
    def updateStateButtons(self, device, scene, item, visible, init=False):
        anyUpdate = False
        for state in self.states:
            if init or ((scene, item) in state["items"] and visible != state["current"]):
                device.sendIconFor(state["button"], state["icon"], centered=True,
                                   crossed=(not (state["current"] if init else visible)))
                anyUpdate = True
                if not init:
                    state["current"] = visible
        return anyUpdate

    # Change LED colors if the microphones are muted
    def updateLED(self, device):
        if self.currentScene == "Video-Mute" or self.states[2]["current"] == False:
            leds = [0xff0000 for i in
                    range(device.nLeds)]  # Either this is the empty "Video-Mute" scene or the mics are muted -> red
        else:
            leds = [0x00ff00 for i in range(device.nLeds)]  # In any other case the mics are live -> green
        device.setLeds(leds)

    def activate(self, device):
        self.ws = obsws("localhost", 4444)  # Connect to websockets plugin in OBS

        # Callback if OBS is shutting down
        def on_exit(message):
            self.ws.disconnect()

        # Callback if the scene changes
        def on_scene(message):
            if self.updateSceneButtons(device, message.getSceneName()):
                device.updateDisplay()  # Only update if parts of the display actually changed
            self.updateLED(device)

        # Callback if the visibility of a source changes
        def on_visibility_changed(message):
            if self.updateStateButtons(device, message.getSceneName(), message.getItemName(), message.getItemVisible()):
                device.updateDisplay()  # Only update if parts of the display actually changed
            self.updateLED(device)

        # Register callbacks to OBS
        self.ws.register(on_exit, events.Exiting)
        self.ws.register(on_scene, events.SwitchScenes)
        self.ws.register(on_visibility_changed, events.SceneItemVisibilityChanged)

        self.ws.connect()

        device.sendTextFor("title", "OBS", inverted=True)  # Title

        ### Buttons 2 to 5 set different scenes (Moderation, Closeup, Slides and Video Mute) ###

        for scene in self.scenes:
            device.assignKey(KeyCode["SW" + str(scene["button"]) + "_PRESS"], [])
            device.assignKey(KeyCode["SW" + str(scene["button"]) + "_RELEASE"], [])
            device.registerCallback(self.getSetSceneCallback(scene["name"]),
                                    KeyCode["SW" + str(scene["button"]) + "_PRESS"])

        ### Button 6: Order!

        def stopOrder():
            self.ws.call(requests.SetSceneItemProperties("Order", visible=False))

        def playOrder():
            self.ws.call(requests.SetSceneItemProperties("Order", visible=True))
            Timer(3, stopOrder).start()

        device.assignKey(KeyCode["SW6_PRESS"], [])
        device.assignKey(KeyCode["SW6_RELEASE"], [])
        device.registerCallback(playOrder, KeyCode["SW6_PRESS"])
        device.sendIconFor(6, "icons/megaphone.png", centered=True)

        ### Buttons 7 to 9 toogle the visibility of items, some of which are present in multiple scenes (Mics, Picture-In-Picture cam, Video stream from phone) ###

        for state in self.states:
            device.assignKey(KeyCode["SW" + str(state["button"]) + "_PRESS"], [])
            device.assignKey(KeyCode["SW" + str(state["button"]) + "_RELEASE"], [])
            device.registerCallback(self.getToggleStateCallback(state), KeyCode["SW" + str(state["button"]) + "_PRESS"])

        ### Get current state and initialize buttons accordingly ###
        current = self.ws.call(requests.GetSceneList())
        for scene in current.getScenes():
            for item in scene["sources"]:
                for state in self.states:
                    if (scene["name"], item["name"]) in state["items"]:
                        state["current"] = item["render"]

        # Call updateSceneButtons and updateStateButtons to initialize their images
        self.currentScene = None
        self.updateSceneButtons(device, current.getCurrentScene(), init=True)
        self.updateStateButtons(device, None, None, True, init=True)
        device.updateDisplay()
        self.updateLED(device)

    def poll(self, device):
        return False  # No polling required

    def animate(self, device):
        pass  # In this mode we want permanent LED illumination. Do not fade or animate otherwise.

    def deactivate(self, device):
        device.clearCallbacks()  # Clear our callbacks if we switch to a different mode

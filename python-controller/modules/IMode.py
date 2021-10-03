class IMode:
    Title = ""

    def SetupButtons(self, device):
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

import wx
from main import *
from MainPanel import *


class SettingsPanel(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None, size=(350, 250), title='Settings')
        self.parent = parent
        self.panel = wx.Panel(self, -1, style=(wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX),
                              size=(350, 250))

        icon(self)

        self.Centre()
        self.panel.SetBackgroundColour("white")

        # SettingsPanel objects
        self.backcolour = wx.StaticText(self.panel, label="Set background colour:", pos=(10, 13))
        self.BackgroundColourPick = wx.ColourPickerCtrl(self.panel, col=self.parent.MainPanel.GraphColor, pos=(140, 10), size=(99, 25))

        self.axcolour = wx.StaticText(self.panel, label="Set axis colour:", pos=(10, 40))
        self.AxisColourPick = wx.ColourPickerCtrl(self.panel, col=self.parent.MainPanel.AxisColor, pos=(140, 40), size=(99, 25))

        self.backgroundButton = wx.Button(self.panel, label="Apply settings", pos=(70, 100), size=(120, 50))

        self.Bind(wx.EVT_BUTTON, self.onbutton, self.backgroundButton)

    def onbutton(self, evt):
        self.parent.MainPanel.GraphPanel.SetBackgroundColour(self.BackgroundColourPick.GetColour())
        self.parent.MainPanel.GraphColor = self.BackgroundColourPick.GetColour()
        self.parent.MainPanel.clearGraphPanel(self.AxisColourPick.GetColour())

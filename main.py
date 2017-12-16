import wx
import time
from SettingsPanel import *
from MainPanel import *

'''
    CONFIG
'''
SPLASH = True
'''
    TODO: Make it possible to change window x_max, y_max, x_min, y_min
'''


def icon(self):
    '''
        Define custom icon.
        ----------------------------------------------------
        License message for GraphCalc.ico:
        Toy Icons Set
        IconsMaster

        The images and icons from this Set are free for use.
        Please refer to our site http://www.iconsmaster.com
    '''
    GraphCalcIconFile = "GraphCalc.ico"
    GraphCalcIcon = wx.Icon(GraphCalcIconFile, wx.BITMAP_TYPE_ICO)
    self.SetIcon(GraphCalcIcon)


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="GraphCalc",
                          size=(1108, 631),
                          style=(wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN))

        self.MainPanel = MainPanel(self)
        self.Centre()

        if SPLASH:
            # -------------------SPLASH-SCREEN-------------------------------------------
            convertedToBitmap = wx.Image(name="splash.png").ConvertToBitmap()
            splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
            splashDuration = 4000  # milliseconds
            terryTheBear = wx.SplashScreen(convertedToBitmap, splashStyle, splashDuration, None)
            # We have to also tell python to wait or else it will load MainPanel before
            # splash has finished displaying
            time.sleep(splashDuration / 1000)
            # --------------------END-----------------------------------------------------
        # self.Show() must be after splash screen
        self.Show()

        # --------STATUS-BAR-------------------------
        self.CreateStatusBar()
        self.SetStatusText("")

        # -------------MENU--------------------------------------------------------
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        file_settings = fileMenu.Append(wx.ID_ANY, 'Settings', 'Settings, have it your way!')
        file_quit = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')

        helpMenu = wx.Menu()
        hitem = helpMenu.Append(wx.ID_HELP, 'About', 'About this program')
        menubar.Append(helpMenu, '&Help')

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.onQuit, file_quit)
        self.Bind(wx.EVT_MENU, self.onSettings, file_settings)
        self.Bind(wx.EVT_MENU, self.onAbout, hitem)
        icon(self)

    def onQuit(self, event):
        self.Close()

    def onSettings(self, event):
        self.SettingsPanel = SettingsPanel(self)
        self.SettingsPanel.Show()

    def onAbout(self, event):
        GraphCalcIconFile = "GraphCalc.ico"
        GraphCalcIcon = wx.Icon(GraphCalcIconFile, wx.BITMAP_TYPE_ICO)
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "GraphCalc"
        info.Version = "1.0.0"
        info.Icon = GraphCalcIcon
        info.Copyright = "2015 (C)"
        info.Description = "A superb program, that you can use to graph ANYTHING!\n\nDevelopers:\nMagnus Gustafsson\nJonas Norlinder\nTerry the Bear, our mascot!"

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)


# ----------------------------MAIN--------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

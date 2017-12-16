import wx
from sympy import *
import math


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Declare panels
        self.GraphPanel = wx.Panel(self, -1, style=wx.BORDER_SIMPLE, size=(800, 600))
        self.UserPanel = wx.Panel(self, -1, style=wx.BORDER_SIMPLE, size=(300, 600))

        # ----------------------Set-panel-properties--------------------
        self.GraphPanel.SetPosition((0, 0))
        self.UserPanel.SetPosition((800, 0))

        self.GraphColor = (255, 255, 255)
        self.AxisColor = (255, 0, 0)
        self.GraphPanel.SetBackgroundColour(self.GraphColor)
        self.UserPanel.SetBackgroundColour("white")

        # This will position defined panels' accordingly
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.GraphPanel, 2, wx.EXPAND)
        box.Add(self.UserPanel, 1, wx.EXPAND)

        # UserPanel objects
        # ----------------COMMAND-INPUT----1-----------------------------
        self.cmd = wx.StaticText(self.UserPanel, label="Graph 1:", pos=(10, 13))
        cmd = self.cmd_variable1 = wx.TextCtrl(self.UserPanel, size=(160, -1), pos=(61, 10))
        cmd.SetValue("x^2")
        GraphColor1 = self.GraphColor1 = wx.ColourPickerCtrl(self.UserPanel, col=(0, 0, 160), pos=(226, 13), size=(80, 25))
        # FULHACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        GraphColor1.SetSize((15,15))
        # ----------------COMMAND-INPUT----2-----------------------------
        self.cmd = wx.StaticText(self.UserPanel, label="Graph 2:", pos=(10, 53))
        cmd = self.cmd_variable2 = wx.TextCtrl(self.UserPanel, size=(160, -1), pos=(61, 50))
        cmd.SetValue("x+100")
        GraphColor2 = self.GraphColor2 = wx.ColourPickerCtrl(self.UserPanel, col=(0, 160, 0), pos=(226, 53), size=(80, 25))
        # FULHACK!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        GraphColor2.SetSize((15,15))

        # --------------------EXECUTE-COMMAND----------------------------
        self.cmd = wx.Button(self.UserPanel, label="Graph it!\n(your way)", pos=(70, 100), size=(120, 50))

        self.Bind(wx.EVT_BUTTON, self.onCmd, self.cmd)
        self.Bind(wx.EVT_PAINT, self.onPaint)

        # -------------------TIMER-FOR-GET-MOUSE-POS--------------------
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        self.Bind(wx.EVT_TIMER, self.printMouseOnGraph, self.timer)

        # -------------------FIND-INTERSECTION-BUTTON--------------------

        self.findIntersect = wx.Button(self.UserPanel, label="Find Intersection", pos=(70, 160), size=(120, 50))
        self.Bind(wx.EVT_BUTTON, self.findInter, self.findIntersect)

        # ----CONSOLE-OUTPUT-----
        self.output = self.output = wx.TextCtrl(self.UserPanel, size=(302, 320), pos=(-2, 240),
                                                style=wx.TE_MULTILINE | wx.TE_READONLY)

        # clearOutput() also adds some start text => run at start to get some starting text
        self.clearOutput()

    def onPaint(self, event):
        self.axis(self.AxisColor)

    def onCmd(self, event):
        self.draw()

    def insertMultiSign(self, string):
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        # Add space att the end of the string
        string += " "
        for i in range(len(string) - 1):
            char1 = string[i]
            char2 = string[i + 1]
            for j in numbers:
                if char1 == j and char2 == "x":
                    string = string[:i + 1] + "*" + string[i + 1:]
                if char2 == j and char1 == "x":
                    string = string[:i + 1] + "*" + string[i + 1:]
        return string

    def verifyCmd(self, string):
        for char in string:
            if self.verifyChar(char) == False:
                return False
        return True

    def verifyChar(self, char):
        OkChar = ["+", "-", "*", "/", ".", "^", "x"]
        try:
            type(int(char)) == int
            return True
        except ValueError:
            for i in OkChar:
                if char == i:
                    return True
        return False

    def draw(self):
        self.clearGraphPanel(self.AxisColor)
        if self.verifyCmd(self.cmd_variable1.GetValue()):
            string_cmd1 = self.cmd_variable1.GetValue()
            self.genericGraph(string_cmd1, self.GraphColor1.GetColour())
        else:
            # --------------------------NOT-READABLE-FUNCTION------------
            self.output.AppendText(">> Graph 1 function is not readable\n")
        if self.verifyCmd(self.cmd_variable2.GetValue()):
            string_cmd2 = self.cmd_variable2.GetValue()
            self.genericGraph(string_cmd2, self.GraphColor2.GetColour())
        else:
            # --------------------------NOT-READABLE-FUNCTION------------
            self.output.AppendText(">> Graph 2 function is not readable\n")

    def clearOutput(self):
        self.output.SetValue(" ---GraphCalc Kernel v 1.0---\n")

    def findInter(self, event):
        # ---------------IF-STRINGS-VERIEFIED----------------------------
        if self.verifyCmd(self.cmd_variable1.GetValue()) and self.verifyCmd(self.cmd_variable2.GetValue()):
            self.draw()
            dc = wx.ClientDC(self.GraphPanel)
            dc.SetPen(wx.Pen(self.AxisColor, 2))
            dc.SetDeviceOrigin(400, 300)
            string_cmd1 = self.cmd_variable1.GetValue()
            string_cmd2 = self.cmd_variable2.GetValue()
            string_cmd1 = self.insertMultiSign(string_cmd1)
            string_cmd2 = self.insertMultiSign(string_cmd2)
            # Begin console output
            self.output.AppendText(">> Calculating...\n")

            # Make sympy recognize x:s in user function
            x = symbols("x")

            graph_cmd1 = sympify(string_cmd1)
            graph_cmd2 = sympify(string_cmd2)

            xRootsList = solve(graph_cmd1 - graph_cmd2, x)
            numberOfComplexRoots = 0
            if len(xRootsList) == 0:
                self.output.AppendText("No solutions exist")
            else:
                for i in xRootsList:
                    if abs(i.as_real_imag()[1]) < (10 ** (-20)):
                        xRoot = float(i.as_real_imag()[0])
                        # Subs. = substitute
                        Intersect = (xRoot, graph_cmd1.subs(x, xRoot))
                        self.output.AppendText(">> Intersection at x: ")
                        self.output.AppendText(str(round(Intersect[0], 2)))
                        self.output.AppendText(" y: ")
                        self.output.AppendText(str(round(Intersect[1], 2)))
                        if (abs(Intersect[0]) > 400) or (abs(Intersect[1]) > 300):
                            self.output.AppendText(" (out of window) ")
                        self.output.AppendText("\n")
                        self.drawCircleOnGraph(Intersect[0], -Intersect[1], 7)
                    else:
                        numberOfComplexRoots += 1
        else:
            # --------------------------NOT-READABLE-FUNCTION------------
            self.output.AppendText(">> One of the functions is not readable\n")

    def printMouseOnGraph(self, event):
        # -----------------GET-MOUSE-POS-ON-GRAPH------------------------
        # THIS FUNCTIONS RUNS FROM TIMER EVENT ------OBS: CHANGE EVENT TO SOMETHING ELSE
        MouseOnGraphCornerOrigin = self.GraphPanel.ScreenToClient(wx.GetMousePosition())
        MouseOnGraph = (MouseOnGraphCornerOrigin[0] - 400, MouseOnGraphCornerOrigin[1] - 300)
        # print MouseOnGraph

    def axis(self, colour):
        '''
            Draw x and y axis
        '''
        dc = wx.ClientDC(self.GraphPanel)
        self.AxisColor = colour
        dc.SetPen(wx.Pen(colour, 1))
        dc.SetDeviceOrigin(400, 300)

        # x-axis
        dc.DrawLine(400, 0, -400, 0)

        # y-axis
        dc.DrawLine(0, 300, 0, -300)

    def clearGraphPanel(self, colour):
        dc = wx.ClientDC(self.GraphPanel)
        dc.Clear()
        self.axis(colour)

    def drawCircleOnGraph(self, x, y, r, color=(255, 0, 0)):
        # dev devides circle into parts
        dc = wx.ClientDC(self.GraphPanel)
        dc.SetPen(wx.Pen((color), 2))
        dc.SetDeviceOrigin(400, 300)
        # div is for dividing circle into segments
        div = 8
        for i in range(0, (2 * div)):
            from_x = x + r * math.cos(i * (math.pi / div))
            from_y = y + r * math.sin(i * (math.pi / div))
            to_x = x + r * math.cos((i + 1) * (math.pi / div))
            to_y = y + r * math.sin((i + 1) * (math.pi / div))
            try:
                dc.DrawLine(from_x, from_y, to_x, to_y)
            except OverflowError:
                break

    def genericGraph(self, string_cmd, color):
        string_cmd = self.insertMultiSign(string_cmd)
        dc = wx.ClientDC(self.GraphPanel)
        dc.SetPen(wx.Pen(color))
        dc.SetDeviceOrigin(400, 300)

        # Make "x" a symbol for sympy
        x = symbols("x")  # datastruktur
        # Convert string to equation with sympy ----NB: sympify uses eval!
        graph_cmd = sympify(string_cmd)

        # Initiate first position we will draw from.
        i = -400
        from_x = -401
        # @Jonas: You have to also set the second argument to negative, ergo: -401
        from_y = -graph_cmd.subs(x, -401)
        # Loop though and draw function.
        while i < 401:
            to_x = i
            # Adjust for up-side-down coordinate system
            to_y = -graph_cmd.subs(x, i)
            if abs(from_y) < 301 or abs(to_y) < 301:
                try:
                    dc.DrawLine(from_x, from_y, to_x, to_y)
                except OverflowError:
                    self.output.AppendText(">> ERROR: OverflowError\n")
                    self.output.AppendText(">> Function ")
                    self.output.AppendText(string_cmd)
                    self.output.AppendText(" produces too big numbers for python to handle\n")
                    break

            from_x = to_x
            from_y = to_y

            i += 1

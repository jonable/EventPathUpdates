import wx
from wx.webkit import WebKitCtrl


ID_OPEN_NEW_WINDOW = wx.NewId()
#----------------------------------------------------------------------
class MozillaBrowser(wx.Frame):
    def __init__(self, start_page):
        wx.Frame.__init__(self, None, -1, "Mozilla Browser Demo")
        self.current = start_page
        self.selLink = ""

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mozilla = WebKitCtrl(self)
        self.CreateStatusBar()
        self.openBtn = wx.Button(self, wx.NewId(), "Open")
        wx.EVT_BUTTON(self, self.openBtn.GetId(), self.OnOpenButton)
        btnSizer.Add(self.openBtn, 0, wx.EXPAND|wx.ALL, 2)

        self.backBtn = wx.Button(self, wx.NewId(), "<--")
        wx.EVT_BUTTON(self, self.backBtn.GetId(), self.OnPrevPageButton)
        btnSizer.Add(self.backBtn, 0, wx.EXPAND|wx.ALL, 2)

        self.nextBtn = wx.Button(self, wx.NewId(), "-->")
        wx.EVT_BUTTON(self, self.nextBtn.GetId(), self.OnNextPageButton)
        btnSizer.Add(self.nextBtn, 0, wx.EXPAND|wx.ALL, 2)

        self.stopBtn = wx.Button(self, wx.NewId(), "Stop")
        wx.EVT_BUTTON(self, self.stopBtn.GetId(), self.OnStopButton)
        btnSizer.Add(self.stopBtn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, wx.NewId(), "Refresh")
        wx.EVT_BUTTON(self, btn.GetId(), self.OnRefreshPageButton)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        txt = wx.StaticText(self, -1, "Location:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

        self.location = wx.ComboBox(self, wx.NewId(), "", style=wx.CB_DROPDOWN|wx.PROCESS_ENTER)
        wx.EVT_COMBOBOX(self, self.location.GetId(), self.OnLocationSelect)
        wx.EVT_KEY_UP(self.location, self.OnLocationKey)
        wx.EVT_CHAR(self.location, self.IgnoreReturn)
        
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)
        btnSizer.Add((1, 1), 1, wx.EXPAND)

        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.mozilla, 1, wx.EXPAND)

        self.mozilla.LoadURL(self.current)
        # self.location.Append(self.current)
        # self.mozilla.SetPageSource("<html><head></head><body><p>Hello world!</p></body></html>")

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        #wx.EVT_SIZE(self, self.OnSize)

    def Derp(self, e):
        print 'hi'

    def OpenInNewWindow(self, evt):
        newwindow = MozillaBrowser()
        newwindow.Show()
        newwindow.mozilla.LoadURL(self.selLink)

    def UpdateStatus(self, evt):
        self.SetStatusText(evt.GetStatusText())

    def UpdateState(self, evt):
         if (evt.GetState() & wx.MOZILLA_STATE_START) or (evt.GetState() & wx.MOZILLA_STATE_TRANSFERRING):
             self.SetStatusText("Loading " + evt.GetURL() + "...")
         elif evt.GetState() & wx.MOZILLA_STATE_NEGOTIATING:
             self.SetStatusText("Contacting server...")
         elif evt.GetState() & wx.MOZILLA_STATE_REDIRECTING:
             self.SetStatusText("Redirecting from " + evt.GetURL())

    def OnLoadComplete(self, evt):
        self.SetStatusText("")
        self.SetTitle("wx.Mozilla - " + self.mozilla.GetTitle())

    def OnRightClick(self, evt):
        contextMenu = wx.Menu()
        if evt.GetLinks() != "":
            self.selLink = evt.GetLink()
            contextMenu.Append(ID_OPEN_NEW_WINDOW, "Open in New Window")

        self.PopupMenu(contextMenu, evt.GetPosition())

    def OnSize(self, evt):
        self.Layout()
        self.panel.Layout()

    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        self.mozilla.LoadURL(url)

    def OnLocationKey(self, evt):
        if evt.KeyCode() == wx.K_RETURN:
            URL = self.location.GetValue()
            self.location.Append(URL)
            self.mozilla.LoadURL(URL)
        else:
            evt.Skip()


    def IgnoreReturn(self, evt):
        if evt.GetKeyCode() != wx.K_RETURN:
            evt.Skip()

    def OnOpenButton(self, event):
        dlg = wx.TextEntryDialog(self, "Open Location",
                                "Enter a full URL or local path",
                                self.current, wx.OK|wx.CANCEL)
        dlg.CentreOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.current = dlg.GetValue()
            self.mozilla.LoadURL(self.current)
        dlg.Destroy()

    def OnPrevPageButton(self, event):
        self.mozilla.GoBack()

    def OnNextPageButton(self, event):
        self.mozilla.GoForward()

    def OnStopButton(self, evt):
        self.mozilla.Stop()

    def OnRefreshPageButton(self, evt):
        self.mozilla.Reload()


overview = """\
<html><body>
<h2>wx.Mozilla</h2>

The wx.Mozilla example shows how to use the wx.MozillaBrowser to embed Mozilla into
a wx.Python application. 
</body></html>
"""

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MozillaBrowser(start_page='http://localhost:8111/revision/')
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    from wx.lib.inspection import InspectionTool
    # import SimpleHTTPServer, sys
    # sys.argv.append(9999)
    # t = threading.Thread(target=SimpleHTTPServer.test, args=())
    # t.setDaemon(False)
    # t.start()
    app = MyApp()

    InspectionTool().Show()    
    app.MainLoop()


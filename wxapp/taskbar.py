import os
import wx
import threading
import subprocess

import runserver

from wxapp.ballontaskbaricon import BalloonTaskBarIcon

DEFAULT_BALLON_MESSAGE = 'Right Click To View Menu'
DEFAULT_BALLON_TITLE   = 'Revisions'

class RevisionsTaskBarIcon(BalloonTaskBarIcon):

	def __init__(self, init_message=None, revision_html_file=None, link_to_update=None, *args, **kwargs):
		"""
		Create a Task Bar Icon to notify user about revisions
		:init_message (Balloon Title, Balloon Init Message)
		:revision_html_file path to the revision file
		:link_to_update url params to launch browser to specific page
		"""
		wx.TaskBarIcon.__init__(self)
		self.server_thread = None
		self.revision_html_file = revision_html_file
		self.link_to_update = link_to_update       
		
		testicon = wx.IconFromBitmap(wx.Bitmap(os.path.abspath('../assets/ser_icon.ico')))

		if init_message:                    
			self.SetIcon(testicon, tooltip=init_message[1])
			self.ShowBalloon(*init_message)
		else: 
			self.SetIcon(testicon, tooltip=DEFAULT_BALLON_MESSAGE)
			self.ShowBalloon(DEFAULT_BALLON_TITLE, DEFAULT_BALLON_MESSAGE)
		

	def OnIconLeftClick(self, event):
		self.fetch_latest(self)

	def CreatePopupMenu(self):
		self.menu = wx.Menu()		
		m_view = self.menu.Append(wx.ID_ANY, "View Latest", "View Revision")
		self.Bind(wx.EVT_MENU, self.OnIconLeftClick, m_view)
		m_view_archive = self.menu.Append(wx.ID_ANY, "View Archive", "View Entire Revision Collection")
		self.Bind(wx.EVT_MENU, self.OnViewArchive, m_view_archive)
		m_exit = self.menu.Append(wx.ID_ANY, "E&xit", "Close Program")        
		self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
		return self.menu

	def launch_browser(self, exit=True):           
	
		import webbrowser
		print self.revision_html_file
		if os.path.exists(self.revision_html_file):            
			# t=FuncThread(webbrowser.open, self.revision_html_file)
			# t.start()            
			webbrowser.open_new(self.revision_html_file)        
		
		# if exit:
		# 	self.close_icon()


	def OnViewArchive(self, event):
		if not self.server_thread:
			self.server_thread = threading.Thread(target=runserver.startWebServer)
			self.server_thread.setDaemon(True)
			self.server_thread.start()
		import webbrowser
		webbrowser.open("http://{}:{}/revision/".format(runserver.DEFAULT_ADDR, runserver.DEFAULT_PORT))  		

	def OnClose(self, event):
		self.close_icon()

	def close_icon(self):		
		self.RemoveIcon()
		try:
			self.Destroy()
			# sys.exit()
		except Exception, e:
			print e
			# silently close program
			pass

class RevisionsAdminTaskBarIcon(BalloonTaskBarIcon):

	def __init__(self, *args, **kwargs):
		wx.TaskBarIcon.__init__(self)
		self.server_thread = None
		# bmp = wx.EmptyBitmap(16, 16)
		# dc = wx.MemoryDC(bmp)
		# dc.SetBrush(wx.RED_BRUSH)
		# dc.Clear()
		# dc.SelectObject(wx.NullBitmap)

		# testicon = wx.EmptyIcon()
		# testicon.CopyFromBitmap(bmp) 
		testicon = wx.IconFromBitmap(wx.Bitmap(os.path.abspath('../assets/ser_icon.ico')))
		
		self.SetIcon(testicon, tooltip="Revisions Update Admin")
		# self.ShowBalloon("Revisions Update Admin", DEFAULT_BALLON_MESSAGE)

	def CreatePopupMenu(self):
		menu      = wx.Menu()
		m_run     = menu.Append(wx.ID_ANY, "Run", "Perform Update Now")
		m_options = menu.Append(wx.ID_ANY, "Options", "Set Options")
		m_exit    = menu.Append(wx.ID_ANY, "E&xit", "Close Program")        
		
		self.Bind(wx.EVT_MENU, self.OnMenuRun, m_run)
		self.Bind(wx.EVT_MENU, self.OnMenuSetOptions, m_options)
		self.Bind(wx.EVT_MENU, self.OnClose, m_exit)

		return menu							

	def OnClose(self, event):
		self.close_icon()

	def OnMenuRun(self, event):
		""" check for revisions """
		subprocess.call([
			"python",
			"manage.py",
			"check_for_revisions",
			"--email_report=True",
			]
		)

	def OnMenuSetOptions(self, event):
		""" launch web interface to configure options """
		# run server in thread
		# launch the browser
		# thread.start_new_thread(runserver.startWebServer, ())
		if not self.server_thread:
			self.server_thread = threading.Thread(target=runserver.startWebServer)
			self.server_thread.setDaemon(True)
			self.server_thread.start()
		import webbrowser
		webbrowser.open("http://{}:{}/admin/revisions/".format(runserver.DEFAULT_ADDR, runserver.DEFAULT_PORT))  

	def close_icon(self):		
		self.RemoveIcon()
		try:
			self.Destroy()
			# sys.exit()
		except Exception, e:
			print e
			# silently close program
			pass

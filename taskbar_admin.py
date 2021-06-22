import wx, os
from wxapp.taskbar import RevisionsAdminTaskBarIcon


def run_admin(*args, **kwargs):
	app = wx.App()
	icon = RevisionsAdminTaskBarIcon(*args, **kwargs)
	app.MainLoop()	


if __name__ == '__main__':
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventupdates.settings")
	run_admin()


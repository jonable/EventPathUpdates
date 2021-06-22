import threading, os



DEFAULT_PORT = 8111
DEFAULT_ADDR = '127.0.0.1'

class FuncThread(threading.Thread):
	def __init__(self, target, *args, **kwargs):
		self._target = target
		self._args = args
		self._kwargs
		threading.Thread.__init__(self)
 
	def run(self):
		self._target(*self._args, **self._kwargs)


def startWebServer(addr=DEFAULT_ADDR, port=DEFAULT_PORT):
	
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventupdates.settings")
	print addr, port
	try:
		print("Starting web server on port %d"%port)
		from django.core.servers.basehttp import run
		from django.core.handlers.wsgi import WSGIHandler
		
		handler = WSGIHandler()

		run( addr, port, handler)
	except Exception, e:
		raise e

# def launch_custom_browser():
# 	from wx.lib.inspection import InspectionTool
# 	# from dbisam import settings
# 	app = WebKit.MyApp(0)
# 	InspectionTool().Show()    
# 	app.MainLoop() 

if __name__ == '__main__':
	# try:
	# 	print "RUNNING SERVER"
	# 	thread.start_new_thread( startWebServer, () )    
	# except Exception, e:
	# 	raise e 
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)
	import webbrowser
	webbrowser.open("http://{}:{}/revision/".format(DEFAULT_ADDR, DEFAULT_PORT))  
	startWebServer()


#!/usr/bin/python
import cgi
import cgitb
import videohub
import render
import re
import time
cgitb.enable()


def change_route(field_strage):
	#get hubinfo
	vh = videohub.Videohub()
	vh.openHub('172.28.127.58', 9990)
	
	#scan main output
	out_route = {}
	for i in range(vh.device.video_inputs):
		optname = 'mainout%d' % i
		opt = field_strage.getvalue(optname, '')
		m = re.match(r'([0-9]+):', opt)
		if(m):
			out_route[ str(i) ] = int(m.group(1)) - 1
	vh.tmp_out_route.routes = out_route
	vh.out_route.routes = out_route
		
	#scan monitor out
	monitor_route={}
	for i in range(vh.device.video_inputs):
		optname = 'monitorout%d' % i
		opt = field_strage.getvalue(optname, '')
		m = re.match(r'([0-9]+):', opt)
		if(m):
			monitor_route[ str(i) ] = int(m.group(1)) - 1
	vh.tmp_monitor_route.routes = monitor_route
	vh.monitor_route.routes = monitor_route	
	vh.tmp_serial_route = vh.serial_route
	vh.serial_route = vh.serial_route
	
	vh.set_route()

	vh.closeHub()
	return vh


# pre render
print "Content-type: text/html"
print

vh=None
f = cgi.FieldStorage()
cmd = f.getvalue('submit_btn', '')
if cmd == 'CHANGE_ROUTE_OK':
	vh = change_route(f)
	



#get hubinfo
if vh == None:
	vh = videohub.Videohub()
	vh.openHub('172.28.127.58', 9990)
	vh.closeHub()
#render
#print vh.device.video_inputs
#print vh.in_label.labels
print render.render('view_control.html', vh)










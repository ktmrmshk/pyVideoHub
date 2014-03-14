#!/usr/bin/python
import cgi
import cgitb
import videohub
import render
import re
cgitb.enable()

# pre render
print "Content-type: text/html"
print

#get hubinfo
vh = videohub.Videohub()
vh.openHub('172.28.127.58', 9990)
vh.closeHub()


f = cgi.FieldStorage()

cmd = f.getvalue('submit_btn', '')

if cmd == 'CHANGE_ROUTE_OK':
	#scan main output
	out_route = {}
	for i in range(72):
		optname = 'mainout%d' % i
		opt = f.getvalue(optname, '')
		m = re.match(r'([0-9]+):', opt)
		if(m):
			out_route[ str(i) ] = int(m.group(1)) - 1
	print out_route
	
	#scan monitor out
	monitor_route={}
	for i in range(72):
		optname = 'monitorout%d' % i
		opt = f.getvalue(optname, '')
		m = re.match(r'([0-9]+):', opt)
		if(m):
			monitor_route[ str(i) ] = int(m.group(1)) - 1
	print monitor_route


#render

print render.render('view_control.html', vh)










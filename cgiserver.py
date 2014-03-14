import CGIHTTPServer

h = CGIHTTPServer.CGIHTTPRequestHandler
h.cgi_directories.append('/')
CGIHTTPServer.test()



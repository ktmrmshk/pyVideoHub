import socket
import re
from collections import OrderedDict
HOST='172.28.127.50'
PORT=9990
RECVMAX=9000

class ProtocolPreamble(object):
    def __init__(self):
        self.version = 0
    def parse(self, msg):
        for l in msg.splitlines():
            m = re.match(r'Version:\s([0-9.]+)', l)
            if(m):
                print m.group(1)
                self.version = m.group(1)

class VideohubDevice(object):
    def __init__(self):
        self.device_present = True
        self.model_name = ''
        self.video_inputs = 0
        self.video_processing_units = 0
        self.video_outputs = 0
        self.video_monitoring_outputs = 0
        self.serial_ports = 0
    def parse(self, msg):
        for l in msg.splitlines():
            m = re.match(r'Device present:\s(\w+)', l)
            if m:
                if m.group(1) == 'true':
                    self.device_present = True
                elif m.group(1) == 'false':
                    self.device_present = False
                continue
            m = re.match(r'Model name:\s(.+)', l)
            if m:
                self.model_name = m.group(1)
                continue
            m = re.match(r'Video inputs:\s(\d+)', l)
            if m:
                self.video_inputs = int( m.group(1) )
                continue
            m = re.match(r'Video processing units:\s(\d+)', l)
            if m:
                self.video_processing_units = int( m.group(1) )
                continue
            m = re.match(r'Video outputs:\s(\d+)', l)
            if m:
                self.video_outputs = int( m.group(1) )
                continue
            m = re.match(r'Video monitoring outputs:\s(\d+)', l)
            if m:
                self.video_monitoring_outputs = int( m.group(1) )
                continue
            m = re.match(r'Serial ports:\s(\d+)', l)
            if m:
                self.serial_ports = int( m.group(1) )
                continue
    def show(self):
        print self.device_present
        print self.model_name
        print self.video_inputs
        print self.video_processing_units
        print self.video_outputs
        print self.video_monitoring_outputs
        print self.serial_ports

class InputLabels(object):
    def __init__(self):
        self.labels=OrderedDict()
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.labels[m.group(1)] = m.group(2)
                idx+=1

    def show(self):
        for k,v in self.labels.items():
            print '%s, %s' % (k, v)
    




class Videohub(object):
    def __init__(self):
        self.proto = ProtocolPreamble()
        self.device = VideohubDevice()

    def parse_initmsg(self, initmsg):
        tmpmsg = initmsg
        for line in tmpmsg.splitlines():
            print line

def openHub(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (host, port) )
    sock.settimeout(0.01)
    initmsg=''
    while True:
        try:
            ret = sock.recv(RECVMAX)
            initmsg+=ret
        except socket.timeout:
            break
    return (sock, initmsg)

def closeHub(sock):
    sock.close()

def divMsgBlock(msg):
    msgblk =[]
    blk=''
    for line in msg.splitlines():
        print line
        if line == '':
            msgblk.append(blk)
            blk=''
        else:
            blk+=line
            blk+='\n'
    return msgblk

s, msg = openHub(HOST, PORT)
closeHub(s)
v = Videohub()
#v.parse_initmsg(msg)
msgblocks = divMsgBlock(msg)

pp = ProtocolPreamble()
pp.parse(msgblocks[0])
vd = VideohubDevice()
vd.parse(msgblocks[1])
vd.show()
il = InputLabels()
il.parse(msgblocks[2])
il.show()

exit()
print msgblocks
for msg in msgblocks:
    print msg[:10]
exit()

for line in ret.splitlines():
    pass
    #
    #if (re.match(r'VIDEOHUB DEVICE:', line)):

#s.close()
#exit()

print '[Recv %d bytes]%s' %  (len(ret), ret)

print '>>try recv1'
ret = s.recv(RECVMAX)
print '[Recv %d bytes]%s' %  (len(ret), ret)

s.close()

import socket
import re
from collections import OrderedDict
import json

HOST='172.28.127.58'
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

class Labels(object):
    def __init__(self):
        self.labels=OrderedDict()
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.labels[ int(m.group(1)) ] = m.group(2)
                idx+=1
    def show(self):
        for k,v in self.labels.items():
            print '%d, %s' % (k, v)
    def save(self, filename):
        with open(filename, 'w') as  f:
            f.write( json.dumps(self.labels) )

class SerialPortDirectons(object):
    def __init__(self):
        self.directions=OrderedDict()
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.directions[ int(m.group(1)) ] = m.group(2)
                idx+=1
    def show(self):
        for k,v in self.directions.items():
            print '%d, %s' % (k, v)
    def save(self, filename):
        with open(filename, 'w') as  f:
            f.write( json.dumps(self.directions) )

class VideoRouting(object):
    def __init__(self):
        self.routes=OrderedDict()
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.routes[ int(m.group(1)) ] = int( m.group(2) )
                idx+=1
    def show(self):
        for k,v in self.directions.items():
            print '%d, %d' % (k, v)
    def save(self, filename):
        with open(filename, 'w') as  f:
            f.write( json.dumps(self.routes) )

class OutputLocks(object):
    def __init__(self):
        self.locks=OrderedDict()    
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.locks[ int(m.group(1)) ] = m.group(2)
                idx+=1
    def show(self):
        for k,v in self.locks.items():
            print '%d, %d' % (k, v)
    def save(self, filename):
        with open(filename, 'w') as  f:
            f.write( json.dumps(self.locks) )
        
class Videohub(object):
    def __init__(self):
        self.sec = {
              'proto' : 'PROTOCOL PREAMBLE:',
              'device' : 'VIDEOHUB DEVICE:',
              'in_label' : 'INPUT LABELS:',
              'out_label' : 'OUTPUT LABELS:',
              'monitor_label' : 'MONITORING OUTPUT LABELS:',
              'serial_label' : 'SERIAL PORT LABELS:',
              'serial_dir' : 'SERIAL PORT DIRECTIONS:',
              'out_route' : 'VIDEO OUTPUT ROUTING:',
              'monitor_route' : 'VIDEO MONITORING OUTPUT ROUTING:',
              'serial_route' : 'SERIAL PORT ROUTING:',
              'out_lock' : 'VIDEO OUTPUT LOCKS:',
              'monitor_lock' : 'MONITORING OUTPUT LOCKS:',
              'serial_lock' : 'SERIAL PORT LOCKS:',
              }
        self.proto = ProtocolPreamble()
        self.device = VideohubDevice()
        self.in_label = Labels()
        self.out_label = Labels()
        self.monitor_label = Labels()
        self.serial_label = Labels()
        self.serial_dir = SerialPortDirectons()
        self.out_route = VideoRouting()
        self.monitor_route = VideoRouting()
        self.serial_route = VideoRouting()
        self.out_lock = OutputLocks()
        self.monitor_lock = OutputLocks()
        self.serial_lock = OutputLocks()


    def divMsgBlock(self, msg):
        msgblk =[]
        blk=''
        for line in msg.splitlines():
            if line == '':
                msgblk.append(blk)
                blk=''
            else:
                blk+=line
                blk+='\n'
        return msgblk

    def parse_initmsg(self):
        msgblks = self.divMsgBlock(self.initmsg)
        for blk in msgblks:
            m = re.match(self.sec['proto'], blk)
            if m:
                self.proto.parse(blk)
                continue
            m = re.match(self.sec['device'], blk)
            if m:
                self.device.parse(blk)
                continue
            m = re.match(self.sec['in_label'], blk)
            if m:
                self.in_label.parse(blk)
                continue
            m = re.match(self.sec['out_label'], blk)
            if m:
                self.out_label.parse(blk)
                continue            
            m = re.match(self.sec['monitor_label'], blk)
            if m:
                self.monitor_label.parse(blk)
                continue         
            m = re.match(self.sec['serial_label'], blk)
            if m:
                self.serial_label.parse(blk)
                continue
            m = re.match(self.sec['serial_dir'], blk)
            if m:
                self.serial_dir.parse(blk)
                continue
            m = re.match(self.sec['out_route'], blk)
            if m:
                self.out_route.parse(blk)
                continue
            m = re.match(self.sec['monitor_route'], blk)
            if m:
                self.monitor_route.parse(blk)
                continue
            m = re.match(self.sec['serial_route'], blk)
            if m:
                self.serial_route.parse(blk)
                continue
            m = re.match(self.sec['out_lock'], blk)
            if m:
                self.out_lock.parse(blk)
                continue
            m = re.match(self.sec['monitor_lock'], blk)
            if m:
                self.monitor_lock.parse(blk)
                continue
            m = re.match(self.sec['serial_lock'], blk)
            if m:
                self.serial_lock.parse(blk)
                continue

    def openHub(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect( (host, port) )
        self.sock.settimeout(0.01)
        self.initmsg=''
        while True:
            try:
                ret = self.sock.recv(RECVMAX)
                self.initmsg+=ret
            except socket.timeout:
                break
        self.parse_initmsg()

    def closeHub(self):
        self.sock.close()




vh = Videohub()
vh.openHub(HOST, PORT)
vh.closeHub()

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

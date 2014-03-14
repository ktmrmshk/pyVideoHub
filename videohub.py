import socket
import re
from collections import OrderedDict
import json

HOST='172.28.127.58'
PORT=9990
RECVMAX=9000

g_section = {
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

class ProtocolPreamble(object):
    def __init__(self, secname='proto'):
        self.version = 0
        self.sec = g_section[secname]
    def parse(self, msg):
        for l in msg.splitlines():
            m = re.match(r'Version:\s([0-9.]+)', l)
            if(m):
                self.version = m.group(1)

class VideohubDevice(object):
    def __init__(self, secname='device'):
        self.sec = g_section[ secname ]
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
    def __init__(self, secname):
        self.labels=OrderedDict()
        self.sec = g_section[ secname ]
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.labels[ m.group(1) ] = m.group(2)
                idx+=1
    def show(self):
        for k,v in self.labels.items():
            print '%d, %s' % (k, v)
    def save(self, filename):
        with open(filename, 'w') as  f:
            f.write( json.dumps(self.labels) )
    def setdevice(self, sock):
        cmd = '%s\n' % self.sec
        for k,v in self.labels.items():
            cmd+= '%s %s\n' % (k, v)
        else:
            cmd+='\n'

        sock.sendall(cmd)
        #ret = sock.recv(RECVMAX)
        msg=''
        while True:
            try:
                ret = sock.recv(RECVMAX)
                msg+=ret
            except socket.timeout:
                break
        #print msg
    def make_default(self, num_ch, prefix='label', is_overwrite=False):
        labels=OrderedDict()
        for i in range(num_ch):
            labels[ str(i) ] = '%s %d' % (prefix, i+1)
        if is_overwrite:
            self.labels=labels
        return labels
    
        

class SerialPortDirectons(object):
    def __init__(self, secname='serial_dir'):
        self.directions=OrderedDict()
        self.sec = g_section[ secname ]
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.directions[ m.group(1) ] = m.group(2)
                idx+=1
    def show(self):
        for k,v in self.directions.items():
            print '%d, %s' % (k, v)
    def save(self, filename):
        with open(filename, 'w') as  f:
            f.write( json.dumps(self.directions) )

class VideoRouting(object):
    def __init__(self, secname):
        self.routes=OrderedDict()
        self.sec = g_section[ secname ]
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.routes[ m.group(1) ] = int( m.group(2) )
                idx+=1
    def show(self):
        for k,v in self.directions.items():
            print '%d, %d' % (k, v)
    def save(self, filename):
        with open(filename, 'w') as  f:
            f.write( json.dumps(self.routes) )
    def setdevice(self, sock):
        cmd = '%s\n' % self.sec
        for k,v in self.routes.items():
            cmd+= '%s %d\n' % (k, v)
        else:
            cmd+='\n'
        #print cmd
        sock.sendall(cmd)
        msg=''
        while True:
            try:
                ret = sock.recv(RECVMAX)
                msg+=ret
            except socket.timeout:
                break
        #print msg
        
    def make_default(self, num_ch, is_overwrite=False):
        routes=OrderedDict()
        for i in range(num_ch):
            routes[ str(i) ] = i
        if is_overwrite:
            self.routes = routes
        return routes

class OutputLocks(object):
    def __init__(self, secname):
        self.locks=OrderedDict()
        self.sec = g_section[ secname ]
    def parse(self, msg):
        idx=0
        for l in msg.splitlines():
            m = re.match(r'(\d+)\s(.+)', l)
            if m:
                if int(m.group(1)) != idx:
                    raise 'index number is not good'
                self.locks[ m.group(1) ] = m.group(2)
                idx+=1
    def show(self):
        for k,v in self.locks.items():
            print '%d, %d' % (k, v)
    def save(self, filename):
        with open(filename, 'w') as  f:
            f.write( json.dumps(self.locks) )
        
class Videohub(object):
    def __init__(self):
        self.sec=g_section
        self.proto = ProtocolPreamble()
        self.device = VideohubDevice()
        self.in_label = Labels('in_label')
        self.out_label = Labels('out_label')
        self.monitor_label = Labels('monitor_label')
        self.serial_label = Labels('serial_label')
        self.serial_dir = SerialPortDirectons()
        self.out_route = VideoRouting('out_route')
        self.monitor_route = VideoRouting('monitor_route')
        self.serial_route = VideoRouting('serial_route')
        self.out_lock = OutputLocks('out_lock')
        self.monitor_lock = OutputLocks('monitor_lock')
        self.serial_lock = OutputLocks('serial_lock')

#         self.tmp_in_label = Labels('in_label')
#         self.tmp_out_label = Labels('out_label')
#         self.tmp_monitor_label = Labels('monitor_label')
#         self.tmp_serial_label = Labels('serial_label')
        
        #self.tmp_serial_dir = SerialPortDirectons()
        
        self.tmp_out_route = VideoRouting('out_route')
        self.tmp_monitor_route = VideoRouting('monitor_route')
        self.tmp_serial_route = VideoRouting('serial_route')
        
        #self.tmp_out_lock = OutputLocks('out_lock')
#         self.tmp_monitor_lock = OutputLocks('monitor_lock')
#         self.tmp_serial_lock = OutputLocks('serial_lock')

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

    def save_label(self, filename, in_label_=None, out_label_=None, monitor_label_=None, serial_label_=None):
        out={}
        if in_label_ is None:
            in_label_ = self.in_label.labels
        if out_label_ is None:
            out_label_ = self.out_label.labels
        if monitor_label_ is None:
            monitor_label_ = self.monitor_label.labels
        if serial_label_ is None:
            serial_label_ = self.serial_label.labels
        out[ self.sec['in_label'] ] = in_label_
        out[ self.sec['out_label'] ] = out_label_
        out[ self.sec['monitor_label'] ] = monitor_label_
        out[ self.sec['serial_label'] ] = serial_label_
            
        with open(filename, 'w') as f:
            f.write( json.dumps(out, indent=2) )
            
    def load_label(self, filename):
        tmpbuf=''
        with open(filename, 'r') as f:
            tmpbuf = f.read()
        tmp = json.loads(tmpbuf)
        self.in_label.labels = tmp[ self.sec['in_label'] ]
        self.out_label.labels = tmp[ self.sec['out_label'] ]
        self.monitor_label.labels = tmp[ self.sec['monitor_label'] ]    
        self.serial_label.labels = tmp[ self.sec['serial_label'] ]    
 
    def set_label(self):
        self.in_label.setdevice(self.sock)
        self.out_label.setdevice(self.sock)
        self.monitor_label.setdevice(self.sock)
        self.serial_label.setdevice(self.sock)

    def save_route(self, filename, out_route_=None, monitor_route_=None, serial_route_=None):
        out={}
        if out_route_ is None:
            out_route_ = self.out_route.routes
        if monitor_route_ is None:
            monitor_route_ = self.monitor_route.routes
        if serial_route_ is None:
            serial_route_ = self.serial_route.routes
        out[ self.sec['out_route'] ] = out_route_
        out[ self.sec['monitor_route'] ] = monitor_route_
        out[ self.sec['serial_route'] ] = serial_route_
        with open(filename, 'w') as f:
            f.write( json.dumps(out, indent=2) )
        
    def load_route(self, filename):
        tmpbuf=''
        with open(filename, 'r') as f:
            tmpbuf = f.read()
        tmp = json.loads(tmpbuf)
        self.tmp_out_route.routes = tmp[ self.sec['out_route'] ]
        self.tmp_monitor_route.routes = tmp[ self.sec['monitor_route'] ]
        self.tmp_serial_route.routes = tmp[ self.sec['serial_route'] ]
   
    def set_route(self):
        self.tmp_out_route.setdevice(self.sock)
        self.tmp_monitor_route.setdevice(self.sock)
        self.tmp_serial_route.setdevice(self.sock)

    def set_default_label(self):
        self.in_label.make_default(self.device.video_inputs, 'input', True)
        self.out_label.make_default(self.device.video_outputs, 'output', True)
        self.monitor_label.make_default(self.device.video_monitoring_outputs, 'monitor', True)
        self.serial_label.make_default(self.device.serial_ports, 'serial', True)
        self.set_label()
   
    def set_default_route(self):
        self.tmp_out_route.make_default(self.device.video_outputs, True)
        self.tmp_monitor_route.make_default(self.device.video_monitoring_outputs, True)
        #self.tmp_serial_route.setdevice(self.sock)
        self.set_route()

if __name__ == '__main__':
    
    vh = Videohub()
    vh.openHub(HOST, PORT)
    vh.save_label('label.json')
    vh.save_route('route.json')
    #vh.save_route('test2.json')
    #vh.load_label('test.json')
    #vh.load_route('test2.json')
    
    #vh.set_label()
    #vh.set_route()
    #vh.set_default_route()
    
    vh.closeHub()
    
    exit()

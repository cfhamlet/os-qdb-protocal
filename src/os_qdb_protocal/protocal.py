#!/usr/bin/python 

import socket
import struct
from x import docid

def qdb_net_get(s, key, keylen):
	t = struct.pack('>bi16si', 1, keylen, key, 0)
	s.send(t)
	t = s.recv(4)
	ret = struct.unpack('>i', t)
	if ret[0] == 0:
		t = s.recv(4)
		data_length = struct.unpack('>i', t)[0]
		return s.recv(data_length)
		#return struct.unpack('%ds'%data_length, t)
	else:
		return None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.141.108.44', 8012))

url = 'http://www.qq.com/'
id = docid(url).bytes
id = id[16:]
print qdb_net_get(s, id, len(id))

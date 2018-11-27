import struct


class Protocal(object):
    def __init__(self, cmd, key):
        self._cmd = cmd
        self._key = key
        self._value = None

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def upstream(self):
        raise NotImplementedError

    def downstream(self, data):
        raise NotImplementedError


class Get(Protocal):
    def upstream(self):
        key_length = len(self._key)
        return struct.pack('>bi%dsi' % key_length, 1, key_length, self._key, 0)

    def downstream(self):
        exist = yield 4
        exist = struct.unpack('>i', exist)[0]

        if exist == 0:
            data_length = yield 4
            data_length = struct.unpack('>i', data_length)[0]
            self._value = yield data_length

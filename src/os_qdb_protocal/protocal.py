import struct

INT_SIZE = 4


class Protocal(object):
    __slots__ = ('_cmd', '_key', '_value')

    def __init__(self, cmd, key):
        self._cmd = cmd
        self._key = key
        self._value = None

    @property
    def cmd(self):
        return self._cmd

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def upstream(self):
        key_length = len(self._key)
        yield struct.pack('>bi%dsi' % key_length, self._cmd, key_length, self._key, 0)

    def downstream(self, data):
        raise NotImplementedError


class Get(Protocal):

    def __init__(self, key):
        super(Get, self).__init__(1, key)

    def downstream(self):
        exist = yield INT_SIZE
        exist = struct.unpack('>i', exist)[0]

        if exist == 0:
            data_length = yield INT_SIZE
            data_length = struct.unpack('>i', data_length)[0]
            data = yield data_length
            assert data_length == len(data)
            self._value = data

        yield -1


class Test(Protocal):

    def __init__(self, key):
        super(Test, self).__init__(12, key)

    def downstream(self):
        exist = yield INT_SIZE
        exist = struct.unpack('>i', exist)[0]

        if exist == 0:
            self._value = True
        elif exist == 1:
            self._value = False
        elif exist < 0:
            errno = yield INT_SIZE
            errno = struct.unpack('>i', errno)[0]
            self._value = errno
        elif exist > 1:
            self._value = None

        yield -1

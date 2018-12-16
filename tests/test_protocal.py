import pytest
import struct
from io import BytesIO

from os_qdb_protocal import create_protocal
from os_qdb_protocal.protocal import Cmd


def test_create_protocal():
    key = '123'
    proto = create_protocal('get', key)
    assert proto.cmd == Cmd.GET
    with pytest.raises(KeyError):
        create_protocal('put', key)


def test_get_protocal():
    key = b'123'
    proto = create_protocal('get', key)
    up = proto.upstream()
    stream = next(up)
    u_cmd, u_key_length, u_key, u_flag = struct.unpack(
        '>bi%dsi' % len(key), stream)
    assert u_cmd == Cmd.GET.value
    assert u_key_length == len(key)
    assert u_key == key
    assert u_flag == 0

    data_length = 1024
    data = b'1' * 1024
    s = BytesIO()
    s.write(struct.pack('>i', 0))
    s.write(struct.pack('>i', data_length))
    s.write(data)
    s.seek(0)
    down = proto.downstream()
    read_size = next(down)
    while read_size >= 0:
        d = s.read(read_size)
        read_size = down.send(d)
    assert proto.value == data

    proto = create_protocal('get', key)
    s = BytesIO()
    s.write(struct.pack('>i', 1))
    s.seek(0)
    down = proto.downstream()
    read_size = next(down)
    while read_size >= 0:
        d = s.read(read_size)
        read_size = down.send(d)
    assert proto.value == None


def test_test_protocal():

    key = b'123'
    proto = create_protocal('test', key)
    up = proto.upstream()
    stream = next(up)
    u_cmd, u_key_length, u_key, u_flag = struct.unpack(
        '>bi%dsi' % len(key), stream)
    assert u_cmd == Cmd.TEST.value
    assert u_key_length == len(key)
    assert u_key == key
    assert u_flag == 0

    test_cases = [
        ((0, None), True),
        ((1, None), False),
        ((-1, 1), 1),
        ((2, None), None),
    ]

    for data, expected in test_cases:
        s = BytesIO()
        for c in data:
            if isinstance(c, int):
                s.write(struct.pack('>i', c))
        s.seek(0)

        down = proto.downstream()
        read_size = next(down)
        while read_size >= 0:
            d = s.read(read_size)
            read_size = down.send(d)
        assert proto.value == expected

# os-qdb-protocal

[![Build Status](https://www.travis-ci.org/cfhamlet/os-qdb-protocal.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-qdb-protocal)
[![codecov](https://codecov.io/gh/cfhamlet/os-qdb-protocal/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-qdb-protocal)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-qdb-protocal.svg)](https://pypi.python.org/pypi/os-qdb-protocal)
[![PyPI](https://img.shields.io/pypi/v/os-qdb-protocal.svg)](https://pypi.python.org/pypi/os-qdb-protocal)


qdb protocal.
 

# Install

`pip install os-qdb-protocal`

# Usage

* create a protocal object from cmd and key

    ```
    from os_qdb_protocal import create_protocal
    proto = create_protocal('get', b'test-key')
    ```

* use upstream method to generate data to be send

  
    ```
    # s is something which used to write data to, like socket, file, etc.
    for data in proto.upstream(): 
        s.send(data)
    ```

* use downstream method to parse data and get size will be recived

    ```
    downstream = proto.downstream()
    read_size = next(downstream)
    while read_size >= 0:
        # s is something which used to recieve data from, like socket, file, etc.
        data = s.read(read_size)
        read_size = downstream.send(data)
    ```

* access key and value

    ```
    proto.key
    proto.value
    ```


# Unit Tests

`$ tox`

# License

MIT licensed.

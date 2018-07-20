import sys
import numpy as np
from ctypes import *
import ctypes

libc_so = {"darwin": "libc.dylib", "linux2": "libc.so.6"}[sys.platform]
# libc_so = {"darwin": "libc.dylib", "linux2": ""}[sys.platform]    #both right
libc = CDLL(libc_so, use_errno=True, use_last_error=True)
print(libc)

# try:
#     rt = CDLL('librt.so')
# except:
#     rt = CDLL('librt.so.1')

MY_MSG_TYPE = 0x02
MSG_KEY = 0x1001
MSG_TEXT_SIZE = 64

class ipc_msg(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('type', ctypes.c_long),('buf', ctypes.c_byte * MSG_TEXT_SIZE)]

msgget = libc.msgget
msgget.restype = c_int
msgget.argtypes = (c_int, c_int)

msgrcv = libc.msgrcv
msgrcv.restype = c_int
msgrcv.argtypes = (c_int, POINTER(c_byte), c_size_t, c_long, c_int)

msgid = msgget(MSG_KEY, 0o666)
if msgid < 0:
    print ("System not infected")
else:
    some_msg = ipc_msg()
    # byref(obj, offset) corresponds to this C code:
    # (((char *)&obj) + offset)
    ret = msgrcv(msgid, cast(byref(some_msg), POINTER(c_byte)), MSG_TEXT_SIZE, MY_MSG_TYPE, 0)
    print(ret)
    print(some_msg.type)
    print(some_msg.buf[:])

    # another method
    # buf = create_string_buffer(MSG_TEXT_SIZE+4)		
    # lbuf = ctypes.cast(buf, POINTER(c_long)) # for type
    # ret = msgrcv(msgid, buf, MSG_TEXT_SIZE, MY_MSG_TYPE, 0)
    # print(lbuf.contents.value)
    # print(buf.raw[4:])


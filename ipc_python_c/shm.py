#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script dumps the content of a shared memory block
# used by Linux/Cdorked.A into a file named httpd_cdorked_config.bin
# when the machine is infected.
#
# Some of the data is encrypted. If your server is infected and you
# would like to help, please send the httpd_cdorked_config.bin
# to our lab for analysis. Thanks!
#
# Marc-Etienne M.Léveillé <leve...@eset.com>
# 

import sys
import numpy as np
from ctypes import *

IPC_RMID = 0
IPC_PRIVATE = 0

libc_so = {"darwin": "libc.dylib", "linux2": ""}[sys.platform]
libc = CDLL(libc_so, use_errno=True, use_last_error=True)

try:
    rt = CDLL('librt.so')
except:
    rt = CDLL('librt.so.1')

# void* memcpy( void *dest, const void *src, size_t count );
memcpy = libc.memcpy
memcpy.restype = c_void_p
memcpy.argtypes = (c_void_p, c_void_p, c_size_t)

shmget = rt.shmget
shmget.restype = c_int
shmget.argtypes = (c_int, c_size_t, c_int)

shmat = rt.shmat
shmat.restype = c_void_p
shmat.argtypes = (c_int, POINTER(c_void_p), c_int)

SHM_SIZE = (512 * 1024)
SHM_KEY = 0x123456
OUTFILE="dump.bin"

shmid = shmget(SHM_KEY, SHM_SIZE, 0o666)
if shmid < 0:
    print ("System not infected")
else:
    addr = shmat(shmid, None, 0)
    pyarray = np.zeros(SHM_SIZE / 4, dtype="float32")
    memcpy (pyarray.ctypes.data, addr, pyarray.nbytes)

    # f=open(OUTFILE, 'wb')    #f = file(OUTFILE, 'wb')
    # f.write(string_at(addr,SHM_SIZE))
    # f.close()
    # print(addr, type(addr))
    # print ("Dumped %d bytes in %s" % (SHM_SIZE, OUTFILE))


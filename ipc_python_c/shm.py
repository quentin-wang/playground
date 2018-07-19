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

from ctypes import *
import ctypes
import sys
import numpy

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
memcpy.restype = ctypes.c_void_p
memcpy.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)

shmget = rt.shmget
shmget.restype = c_int
shmget.argtypes = (c_int, c_size_t, c_int)

shmat = rt.shmat
shmat.restype = c_void_p
shmat.argtypes = (c_int, POINTER(c_void_p), c_int)

SHM_SIZE = (512 * 1024)
SHM_KEY = 0x123456
OUTFILE="dump.bin"
#define MEM_SIZE (512 * 1024)



shmid = shmget(SHM_KEY, SHM_SIZE, 0o666)
if shmid < 0:
    print ("System not infected")
else:
    addr = shmat(shmid, None, 0)
    # pyarray = numpy.arange(100, dtype="float32").reshape(10, 10)
    pyarray = numpy.zeros(SHM_SIZE / 4, dtype="float32")
    # print(pyarray.nbytes)
    memcpy (pyarray.ctypes.data, addr, pyarray.nbytes)
    # print(pyarray)

    # f=open(OUTFILE, 'wb')    #f = file(OUTFILE, 'wb')
    # f.write(string_at(addr,SHM_SIZE))
    # f.close()
    # print(addr, type(addr))
    # print ("Dumped %d bytes in %s" % (SHM_SIZE, OUTFILE))


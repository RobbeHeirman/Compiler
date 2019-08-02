"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
import struct
from array import array

x = 4.44
print(hex(struct.unpack('f', struct.pack('f', x))[0]))

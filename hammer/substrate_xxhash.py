'''
Created on 20 Nov 2019

@author: andreas
'''

"""
for 128bit xxhash install experimental dev version of xxhash, see
https://github.com/ifduyue/python-xxhash/issues/34#issuecomment-555917458
"""

import xxhash 

def xxh6464(x):
    o1 = bytearray(xxhash.xxh64(x, seed=0).digest())
    o1.reverse()
    o2 = bytearray(xxhash.xxh64(x, seed=1).digest())
    o2.reverse()
    return "0x{}{}".format(o1.hex(), o2.hex())

U8a = bytes("Sudo Key", encoding='utf8')
print (xxhash.xxh32_hexdigest(U8a)) 
print (xxhash.xxh64_hexdigest(U8a))
print (xxhash.xxh3_128_hexdigest(U8a))
print (xxh6464(U8a))


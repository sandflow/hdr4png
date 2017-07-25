# Copyright (c) 2016, Pierre-Anthony Lemieux <pal@palemieux.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#  
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import struct
import zlib
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("icc_profile", help = "Path of the ICC profile")

parser.add_argument("in_png", help = "Path of the input PNG file")

parser.add_argument("out_png", help = "Path of the output PNG file")

parser.add_argument("-p", "--profilename", help = "Name of the profile")

args = parser.parse_args()

# if no profile name is provided, use the name of the ICC profile file

if args.profilename is None:
    import os.path

    pname = os.path.splitext(os.path.split(args.icc_profile)[1])[0].encode()
else:
    pname = args.profilename.encode()

fin = open(args.in_png, "rb")
fout = open(args.out_png, "wb")
icc_profile = open(args.icc_profile, "rb").read()

PNGMAGIC = bytes([137, 80, 78, 71, 13, 10, 26, 10])

IDAT_NAME = b'IDAT'
PLTE_NAME = b'PLTE'
iCCP_NAME = b'iCCP'
sRGB_NAME = b'sRGB'

# read the PNG magic number

header = fin.read(len(PNGMAGIC))

if header != PNGMAGIC:
    raise Exception("Invalid PNG header")

# write the PNG magic to the output file

fout.write(PNGMAGIC)

# remember if we wrote an iCCP chunk

has_written_iCCP = False

# copy chunks from input to output file

while True:

    # read the chunk length

    rawlen = fin.read(4)

    if len(rawlen) == 0:
        break

    clen = struct.unpack('!I', rawlen)[0]

    # read the chunk name
    
    cname = fin.read(4)

    # read the chunk data

    cdata = fin.read(clen)

    # read the chunk CRC

    ccrc = struct.unpack('!I', fin.read(4))[0]

    # overwrite an existing iCCP chunk or insert a new one if
    # one is not found

    if cname == sRGB_NAME:
        continue
    
    elif cname == iCCP_NAME or \
         (not has_written_iCCP and (cname == PLTE_NAME or cname == IDAT_NAME)):

        iccpdata = pname
        iccpdata += b'\x00'
        iccpdata += b'\x00'
        iccpdata += zlib.compress(icc_profile)

        iccplen = len(iccpdata)

        fout.write(struct.pack('!I', iccplen))
        
        iccpchunk = iCCP_NAME
        iccpchunk += iccpdata

        fout.write(iccpchunk)

        iccpcrc = zlib.crc32(iccpchunk) 

        fout.write(struct.pack('!I', iccpcrc))

        has_written_iCCP = True

        if cname == iCCP_NAME:
            continue
        
    fout.write(struct.pack('!I', clen))
    fout.write(cname)
    fout.write(cdata)
    fout.write(struct.pack('!I', ccrc))
        

    


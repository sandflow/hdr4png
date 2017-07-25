     _          _          ___                      
    | |        | |        /   |                     
    | |__    __| | _ __  / /| | _ __   _ __    __ _ 
    | '_ \  / _` || '__|/ /_| || '_ \ | '_ \  / _` |
    | | | || (_| || |   \___  || |_) || | | || (_| |
    |_| |_| \__,_||_|       |_/| .__/ |_| |_| \__, |
                               | |             __/ |
                               |_|            |___/ 

                               
INTRODUCTION
============

`hdr4png` is a Python script that adds an specially-crafted `iCCP` chunk to PNG images according to (Using the ITU BT.2100 PQ EOTF with the PNG Format WG Note)[https://www.w3.org/TR/png-hdr-pq/]. The latter specification uses the `iCCP` chunk to unambiguously signal the color system of an image that uses the Reference PQ EOTF specified in ITU BT.2100-1. It also allows graceful processing by decoders that do not conform to this specification by recommending fallback values for the `gAMA` chunk, `cHRM` chunk, and embedded ICC profile.

_NOTE: `hdr4png` does not convert SDR images to HDR images, but merely adds an `iCCP` chunk. The input image must contain pixels that already conform to the ITU BT.2100 PQ color system_


DEPENDENCIES
============

(required) Python 3.4 or higher


EXAMPLE USAGE
=============

    python hdr4png.py -p ITUR_2100_PQ_FULL ITUR_2100_PQ_FULL.icc in.png out.png
    
where `ITUR_2100_PQ_FULL.icc` can be retrieved from (Using the ITU BT.2100 PQ EOTF with the PNG Format WG Note)[https://www.w3.org/TR/png-hdr-pq/].


NOTABLE DIRECTORIES AND FILES
=============================

    src/hdr4png.py                      Main script
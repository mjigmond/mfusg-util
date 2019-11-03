#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 09:06:58 2019

@author: marius
"""

import numpy as np
import os

def parseCBBu(fn=None):
    fSize = os.path.getsize(fn)
    print(fSize)
    ofst = 0
    BUD = {}
    while ofst < fSize:
        dtmeta = np.dtype([
                ('kstp', 'i4'),
                ('kper', 'i4'),
                ('text', 'S16'),
                ('nval', 'i4'),
                ('one', 'i4'),
                ('icode', 'i4')
        ])
        meta = np.memmap(fn, mode='r', dtype=dtmeta, offset=ofst, shape=1)[0]
        arrSize = meta['nval']
        print('debug message', meta)
        dtu = np.dtype([
                ('kstp', 'i4'),
                ('kper', 'i4'), 
                ('text', 'S16'),
                ('nval', 'i4'), 
                ('one', 'i4'),
                ('icode', 'i4'), 
                ('data', 'f4', arrSize)
        ])
        data = np.memmap(fn, mode='r', dtype=dtu, offset=ofst, shape=1)[0]
        ofst += dtu.itemsize
        print('debug message', ofst, fSize, fSize - ofst)
        kper = data['kper']
        kstp = data['kstp']
        text = data['text'].decode().strip()
        BUD[(text, arrSize), kper, kstp] = data['data']
    return BUD

fName = '/home/marius/software/mfusg1_5/test/02_quadtree/output/biscayne.cbc'
cbb = parseCBBu(fName)
print(cbb.keys())

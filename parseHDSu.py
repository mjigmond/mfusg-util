#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:28:01 2019

@author: marius
"""

import numpy as np
import os

def parseHDSu(fn: str=None) -> np.array:
    fSize = os.path.getsize(fn)
    print(fSize)
    ofst = 0
    HDS = {}
    while ofst < fSize:
        dtmeta = np.dtype([
                ('kstp', 'i4'), 
                ('kper', 'i4'),
                ('pertim', 'f4'),
                ('totim', 'f4'),
                ('text', 'S16'),
                ('nstrt', 'i4'),
                ('nndlay', 'i4'),
                ('ilay', 'i4')
        ])
        meta = np.memmap(fn, mode='r', dtype=dtmeta, offset=ofst, shape=1)[0]
        print('debug message', meta)
        nstrt = meta['nstrt']
        nndlay = meta['nndlay']
        kper = meta['kper']
        kstp = meta['kstp']
        ilay = meta['ilay']
        if ilay == 1:
            h = np.empty(0)
        n = nndlay - nstrt + 1
        dt = np.dtype([
                ('kstp', 'i4'), 
                ('kper', 'i4'), 
                ('pertim', 'f4'),
                ('totim', 'f4'), 
                ('text', 'S16'),
                ('nstrt', 'i4'), 
                ('nndlay', 'i4'),
                ('ilay', 'i4'),
                ('data', 'f4', n)
        ])
        arr = np.memmap(fn, mode='r', dtype=dt, offset=ofst, shape=1)[0]
        h = np.concatenate((h, arr['data']))
        ofst += dt.itemsize
        HDS[kper, kstp] = h
    return HDS

fName = 'data/biscayne.hds'
hds = parseHDSu(fName)

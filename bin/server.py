#! /usr/bin/env python
import os
import sys

thisdir = os.path.dirname(__file__)
libdir = os.path.abspath(os.path.join(thisdir, '..'))
if libdir not in sys.path:
    sys.path.insert(0, libdir)

libdir = os.path.abspath(os.path.join(thisdir, '../app'))
if libdir not in sys.path:
    sys.path.insert(0, libdir)

from app.main import Main

bn = None
if len(sys.argv) > 1:
    bn = sys.argv[1]
Main().load_images(bn)

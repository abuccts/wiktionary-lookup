# -*- coding: utf-8 -*-

import os.path
try:
	import unittest2 as unittest
except:
	import unittest

if __name__ == "__main__":
	rootdir = os.path.split(os.path.dirname(__file__))[0]
	unittest.defaultTestLoader.discover(rootdir)
# -*- coding: utf-8 -*-

import os.path

try:
	import unittest2 as unittest
except:
	import unittest

def additional_tests():
	project_root = os.path.split(os.path.dirname(__file__))[0]
	return unittest.defaultTestLoader.discover(project_root)
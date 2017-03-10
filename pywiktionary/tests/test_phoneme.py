# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
from six import with_metaclass
from pywiktionary.phoneme import IPA2CMUBET


TestData = [
	("ɑd", "AA D ."),
	("[ɑd]", "AA D ."),
	("/ɑd/", "AA D ."),
	("/æt/", "AE T ."),
	("/hʌt/", "HH AH T ."),
	("/ɔːt/", "AO T ."),
	("/viː/", "V IY ."),
	("/wiː/", "W IY ."),
	("/jiːld/", "Y IY L D ."),
	("/ˈziː/", "Z IY ."),
]

class TestPhonemeMeta(type):
	def __new__(mcs, name, bases, dict):
	
		def gen_test_IPA2CMUBET(IPA, CMUBET):
			def test(self):
				return self.assertEqual(IPA2CMUBET(IPA), CMUBET)
			return test
		
		for i, (IPA, CMUBET) in enumerate(TestData):
			test_IPA2CMUBET_name = "test_IPA2CMUBET_%s" % i
			dict[test_IPA2CMUBET_name] = gen_test_IPA2CMUBET(IPA, CMUBET)
		return type.__new__(mcs, name, bases, dict)

class TestPhoneme(with_metaclass(TestPhonemeMeta, unittest.TestCase)):
	pass

if __name__ == "__main__":
	unittest.main()

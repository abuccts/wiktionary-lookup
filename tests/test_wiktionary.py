# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals

try:
	import unittest2 as unittest
except ImportError:
	import unittest
from six import with_metaclass
from pywiktionary.wiktionary import Wiktionary


class TestWiktionary(unittest.TestCase):

	def test_set_lang(self):
		wikidict = Wiktionary()
		self.assertEqual(wikidict.lang, "en")
		self.assertEqual(wikidict.api, "https://en.wiktionary.org/w/api.php")
		wikidict.set_lang("fr")
		self.assertEqual(wikidict.lang, "fr")
		self.assertEqual(wikidict.api, "https://fr.wiktionary.org/w/api.php")
	
	def test_parse(self):
		# TODO
		pass
	
	def test_parse_details(self):
		# TODO
		pass
	
	def test_parse_pronun(self):
		# TODO
		pass
	
	def test_lookup(self):
		# TODO
		pass

if __name__ == "__main__":
	unittest.main()

# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import json
try:
	from urllib import urlencode, urlopen
except ImportError:
	from urllib.parse import urlencode
	from urllib.request import urlopen

from pywiktionary.parser import Parser


class Wiktionary(object):
	def __init__(self, lang="English", CMUBET=True, phoneme_only=False):
		self.lang = lang
		self.CMUBET = CMUBET
		self.phoneme_only = phoneme_only
		self.api = "https://en.wiktionary.org/w/api.php"
		self.param = {"action": "query", "titles": None, "prop": "revisions", "rvprop": "content", "rvlimit": 1, "format": "json"}

	def set_lang(self, lang):
		self.lang = lang

	def lookup(self, word, lang=None, CMUBET=None, phoneme_only=None):
		lang = self.lang if lang is None else lang
		CMUBET = self.CMUBET if CMUBET is None else CMUBET
		phoneme_only = self.phoneme_only if phoneme_only is None else phoneme_only
		if lang != "English":
			CMUBET = False
		parser = Parser(lang=lang, CMUBET=CMUBET, phoneme_only=phoneme_only)
		
		self.param["titles"] = word.encode("utf-8")
		res = urlopen(self.api, urlencode(self.param).encode()).read()
		content = json.loads(res.decode("utf-8"))
		try:
			text = list(content["query"]["pages"].values())[0]["revisions"][0]["*"]
		except:
			return "word not found"
		return parser.parse(text)
		
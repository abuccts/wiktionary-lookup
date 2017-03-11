# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import re
import json
try:
	from urllib import urlencode, urlopen
except ImportError:
	from urllib.parse import urlencode
	from urllib.request import urlopen

from pywiktionary.phoneme import IPA2CMUBET
import argparse

POS = ["noun", "verb", "adjective", "adverb", "determiner",
       "article", "preposition", "conjunction", "proper noun",
       "letter", "character", "phrase", "proverb", "idiom",
       "symbol", "syllable", "numeral", "initialism", "interjection"]

class Wiktionary(object):
	def __init__(self, lang="en", CMUBET=True):
		self.lang = lang
		self.api = "https://" + lang + ".wiktionary.org/w/api.php"
		self.param = {"action": "query", "titles": None, "prop": "revisions", "rvprop": "content", "rvlimit": 1, "format": "json"}
		self.CMUBET = CMUBET
		self.regex = {
			"lang": re.compile("^lang="),
			"node": re.compile("{{([^}]+)}}"),
			"pronun": re.compile("\* ([^\n]+)\n"),
			"h2": re.compile("(?:\A|\n)={2}([a-zA-Z0-9 ]+)={2}\n"),
			"h3": re.compile("\n={3}([a-zA-Z0-9 ]+)={3}\n"),
			"h4": re.compile("\n={4}([a-zA-Z0-9 ]+)={4}\n")
		}

	def set_lang(self, lang):
		self.lang = lang
		self.api = "https://" + self.lang + ".wiktionary.org/w/api.php"

	def parse(self, text):
		result = {}
		h2_lst = self.regex["h2"].findall(text)
		h2_split = self.regex["h2"].split(text)
		i = 0
		while i < len(h2_split):
			if h2_split[i] in h2_lst:
				result[h2_split[i]] = self.parse_details(h2_split[i + 1])
				i += 1
			i += 1
		return result

	def parse_details(self, text, depth=3):
		result = {}
		details_lst = self.regex["h" + str(depth)].findall(text)
		details_split = self.regex["h" + str(depth)].split(text)
		pronun_result = {}
		pos_result = []
		etymology_result = details_split[0] if depth == 4 else ""
		i = 0
		while i < len(details_split):
			if details_split[i] in details_lst:
				name = details_split[i].lower()
				if name == "pronunciation":
					pronun_result = self.parse_pronun(details_split[i + 1])
				elif name in POS:
					pos_result.append(details_split[i])
				elif "etymology" in name:
					if name == "etymology":
						etymology_result = details_split[i + 1]
					else:
						result[details_split[i]] = self.parse_details(details_split[i + 1], depth=4)
				i += 1
			i += 1
		if len(pronun_result) > 0:
			result["Pronunciation"] = pronun_result
		if len(pos_result) > 0:
			result["Part of Speech"] = pos_result
#		if len(etymology_result) > 0:
#			result["Etymology"] = etymology_result
		return result

	def parse_pronun(self, text):
		result = []
		pronun_lst = self.regex["pronun"].findall(text)
		for each in pronun_lst:
			item = {}
			accent_result = []
			enPR_result = []
			IPA_result = []
			audio_result = []
			node_lst = self.regex["node"].findall(each)
			for node in node_lst:
				node_detail = node.split("|")
				if node_detail[0] == "a":
					accent_result += node_detail[1:]
				elif node_detail[0] == "enPR":
					enPR_result += node_detail[1:]
				elif node_detail[0] == "IPA":
					lang = re.sub(self.regex["lang"], "", node_detail[-1])
					IPA_result.append((node_detail[1:-1], lang))
				elif node_detail[0] == "audio":
					lang = re.sub(self.regex["lang"], "", node_detail[-1])
					audio_result.append(tuple(node_detail[1:-1]) + (lang,))
			if len(accent_result) > 0:
				item["Accent"] = accent_result[0] if len(accent_result) == 1 else accent_result
			if len(enPR_result) > 0:
				item["enPR"] = enPR_result[0] if len(enPR_result) == 1 else enPR_result
			if len(IPA_result) > 0:
				item["IPA"] = IPA_result[0] if len(IPA_result) == 1 else IPA_result
				if self.CMUBET:
					CMUBET_result = []
					for ipa_lst, ipa_lang in IPA_result:
						cmubet_lst = []
						for ipa_pronun in ipa_lst:
							cmubet_pronun = IPA2CMUBET(ipa_pronun)
							cmubet_lst.append(cmubet_pronun)
						CMUBET_result.append(cmubet_lst)
					item["CMUBET"] = CMUBET_result[0] if len(CMUBET_result) == 1 else CMUBET_result
			if len(audio_result) > 0:
				item["Audio"] = audio_result[0] if len(audio_result) == 1 else audio_result
			if len(item) > 0:
				result.append(item)
		return result

	def lookup(self, word):
		self.param["titles"] = word
		res = urlopen(self.api, urlencode(self.param).encode()).read()
		content = json.loads(res.decode("utf-8"))
		text = list(content["query"]["pages"].values())[0]["revisions"][0]["*"]
		return self.parse(text)

def json_option(parser):
	parser.add_argument(
		'--json', action='store_true',
		help='Output in machine readable json. This may contain additional information.')


def cli():
	# Make "wikitionary | cat" work with unicode output
	#   http://stackoverflow.com/questions/2276200/changing-default-encoding-of-python#17628350
	#   An alternative approach is to use PYTHONIOENCODING
	import sys
	import io
	sys.stdout = io.open(0, 'w', encoding='utf8')

	wiki = Wiktionary()
	PARSER = argparse.ArgumentParser(description='Fetch information from wikitionary')
	PARSER.add_argument('word', type=str)
	PARSER.add_argument(
		'--language',
		type=str.title,
		help='Display entry for this language (the default is english). Use "all" for all.')

	json_option(PARSER)
	args = PARSER.parse_args()

	result = wiki.lookup(args.word)

	if args.language == 'All':
		language_entries = result.items()
	elif args.language:
		language_entries = [(args.language, result[args.language])]
	elif 'English' in result:
		language_entries = [('English', result['English'])]
	else:
		language_entries = result.items()

	if args.json:
		print(json.dumps(result, indent=4))
	else:
		for language, language_entry in language_entries:
			pronunciation = format_pronunciation(language_entry)
			if pronunciation:
				print(language)
				print(indent(pronunciation))

def indent(s):
	return '\n'.join(['    ' + l for l in  s.split('\n')])

def format_pronunciation(entry):
	if 'Pronunciation' not in entry:
		return None

	result = []

	for pronunciation in entry['Pronunciation']:
		if not 'IPA' in pronunciation:
			continue
		else:
			accent = pronunciation.get('Accent', 'Standard')
			if isinstance(accent, list):
				accent = ', '.join(accent)
			result.append(accent)
			variants, _ = pronunciation['IPA']
			for variant in variants:
				result.append('    ' + variant)

	if not result:
		return None

	return u'\n'.join(result)

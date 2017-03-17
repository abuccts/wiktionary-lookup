# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from pywiktionary.wiktionary import Wiktionary
import json
import argparse

def json_option(parser):
	parser.add_argument(
		'--json', action='store_true',
		help='Output in machine readable json. This may contain additional information.')

def cli():
	# Make "wikitionary | cat" work with unicode output
	# http://stackoverflow.com/questions/2276200/changing-default-encoding-of-python#17628350
	# An alternative approach is to use PYTHONIOENCODING
	import sys
	import io
	sys.stdout = io.open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

	wiki = Wiktionary()
	PARSER = argparse.ArgumentParser(description='Fetch information from wikitionary')
	PARSER.add_argument('word', type=str)
	PARSER.add_argument(
		'--language',
		type=str.title,
		help='Display entry for this language (the default is English)')

	json_option(PARSER)
	args = PARSER.parse_args()

	args.language = "English" if args.language is None else args.language
	result = wiki.lookup(args.word, lang=args.language)

#	if args.language == 'All':
#		language_entries = result.items()
#	elif args.language:
#		language_entries = [(args.language, result[args.language])]
#	elif 'English' in result:
#		language_entries = [('English', result['English'])]
#	else:
#		language_entries = result.items()
	language_entries = [(args.language, result[args.language])]
	
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

	return '\n'.join(result)

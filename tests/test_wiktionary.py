# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals

try:
	import unittest2 as unittest
except ImportError:
	import unittest
from six import with_metaclass
from random import shuffle
from pywiktionary.wiktionary import Wiktionary


# list of languages
TestLang = [
	None,
	"French",
	"German",
	"Greek",
	"Russian",
]

# list of (word, lang, CMUBET, phoneme_only, result)
TestWord = [
	("read", "English", True, False,
		{'English': {'Part of Speech': ['Verb', 'Noun'], 'Pronunciation': [{'CMUBET': ['R IY D .'], 'IPA': (['/ɹiːd/'], 'en'), 'enPR': 'rēd'}, {'Audio': ('En-uk-to read.ogg', 'Audio (UK)', 'en')}, {'Audio': ('en-us-read.ogg', 'Audio (US)', 'en')}, {'CMUBET': ['R EH D .'], 'IPA': (['/ɹɛd/'], 'en'), 'enPR': 'rĕd'}, {'Audio': ('en-us-read-past.ogg', 'Audio (US)', 'en')}]}}
	),
	("add", "English", True, False,
		{'English': {'Part of Speech': ['Verb', 'Noun'], 'Pronunciation': [{'CMUBET': ['AE D .'], 'IPA': (['/æd/'], 'en')}, {'Audio': ('en-us-add.ogg', 'Audio (US)', 'en')}]}}
	),
	("fin", "English", True, False,
		{'English': {'Etymology 1': {'Part of Speech': ['Noun', 'Verb']}, 'Etymology 2': {'Part of Speech': ['Noun']}, 'Pronunciation': [{'CMUBET': ['F N .'], 'IPA': (['/fɪn/'], 'en'), 'enPR': 'fĭn'}, {'Audio': ('en-us-fin.ogg', 'Audio (US)', 'en')}]}}
	),
	("present", "English", True, False,
		{'English': {'Etymology 1': {'Part of Speech': ['Adjective', 'Noun'], 'Pronunciation': [{'CMUBET': ['P R EH Z N T .'], 'IPA': (['/ˈpɹɛzənt/'], 'en'), 'enPR': 'prĕzʹənt'}, {'Audio': ('en-us-present-adjective.ogg', 'Audio (US)', 'en')}]}, 'Etymology 2': {'Part of Speech': ['Noun', 'Verb'], 'Pronunciation': [{'CMUBET': ['P R Z EH N T .'], 'IPA': (['/pɹɪˈzɛnt/'], 'en'), 'enPR': "prĭzĕnt'"}, {'Accent': 'Canada', 'CMUBET': ['P R Z EH N T .'], 'IPA': (['/pɹəˈzɛnt/'], 'en')}, {'Audio': [('en-us-present-verb1.ogg', 'Audio (US)', 'en'), ('en-us-present-verb2.ogg', 'Audio (US)', 'en')]}]}}}
	),
	("present", "English", True, True,
		{'CMUBET': ['P R EH Z N T .', 'P R Z EH N T .', 'P R Z EH N T .'], 'IPA': ['/ˈpɹɛzənt/', '/pɹɪˈzɛnt/', '/pɹəˈzɛnt/']}
	),
	("français", "French", False, False,
		{'French': {'Part of Speech': ['Adjective', 'Noun'], 'Pronunciation': [{'IPA': (['/fʁɑ̃.sɛ/'], 'fr')}, {'Audio': ('Fr-le français-fr-ouest.ogg', 'Audio (France, West)', 'fr')}, {'Audio': ('Fr-français.ogg', 'Audio (France, Aquitaine)', 'fr')}, {'Audio': ('Qc-français.ogg', "Audio (Quebec, Val-d'Or)", 'fr')}, {'Audio': ('Fr-français-fr-CA-Québec-(Lac-Saint-Jean).oga', 'Audio (Quebec, Lac-Saint-Jean)', 'fr')}]}}
	),
	("pâquerette", "French", False, False,
		{'French': {'Part of Speech': ['Noun'], 'Pronunciation': [{'IPA': (['/pɑkʁɛt/'], 'fr')}, {'Audio': ('Fr-pâquerette.ogg', 'audio', 'fr')}]}}
	),
	("être", "French", False, False,
		{'French': {'Part of Speech': ['Verb', 'Noun'], 'Pronunciation': [{'IPA': (['/ɛtʁ/'], 'fr')}, {'Audio': ('Fr-être-fr-ouest.ogg', 'Audio (France, West)', 'fr')}, {'Accent': 'Quebec', 'IPA': (['[aɛ̯t{{x2i'], 'X')}, {'Audio': ('Qc-être.ogg', 'Audio (Quebec, Montreal)', 'fr')}, {'Accent': 'Louisiana', 'IPA': (['[ɛt(ɾə)]'], 'fr')}]}}
	),
	("être", "French", False, True,
		{'IPA': ['/ɛtʁ/', '[aɛ̯t{{x2i', '[ɛt(ɾə)]']}
	),
	("Wörterbücher", "German", False, False,
		{'German': {'Part of Speech': ['Noun'], 'Pronunciation': [{'IPA': (['/ˈvœʁtɐˌbyːçɐ/'], 'de')}, {'Audio': ('De-at-Wörterbücher.ogg', 'Audio (Austria)', 'de')}]}}
	),
	("Groß", "German", False, False,
		{'German': {'Part of Speech': ['Noun', 'Proper noun'], 'Pronunciation': [{'IPA': (['/ɡroːs/'], 'de')}]}}
	),
	("mäßig", "German", False, False,
		{'German': {'Part of Speech': ['Adjective'], 'Pronunciation': [{'IPA': (['/ˈmɛːsɪç/'], 'de')}, {'IPA': (['/ˈmeːsɪç/'], 'de')}, {'IPA': (['/ˈmɛːsɪk/'], 'de')}, {'IPA': (['/ˈmeːsɪk/'], 'de')}]}}
	),
	("mäßig", "German", False, True,
		{'IPA': ['/ˈmɛːsɪç/', '/ˈmeːsɪç/', '/ˈmɛːsɪk/', '/ˈmeːsɪk/']}
	),
	("ελληνικά", "Greek", False, False,
		{'Greek': {'Part of Speech': ['Noun', 'Adjective'], 'Pronunciation': [{'IPA': (['[eliniˈka]'], 'el')}]}}
	),
	("εσπεράντο", "Greek", False, False,
		{'Greek': {'Part of Speech': ['Noun'], 'Pronunciation': [{'IPA': (['/ɛs.pɛ.ˈɾan.dɔ/'], 'el')}]}}
	),
	("γέρος", "Greek", False, False,
		{'Greek': {'Part of Speech': ['Noun'], 'Pronunciation': [{'IPA': (['/ˈʝeɾos/'], 'el')}]}}
	),
	("γέρος", "Greek", False, True,
		{'IPA': ['/ˈʝeɾos/']}
	),
	("читать", "Russian", False, False,
		{'Russian': {'Part of Speech': ['Verb'], 'Pronunciation': [{'IPA': (['[t͡ɕɪˈtatʲ]'], 'ru')}, {'Audio': ('Ru-читать.ogg', 'Audio', 'ru')}]}}
	),
	("добавить", "Russian", False, False,
		{'Russian': {'Part of Speech': ['Verb'], 'Pronunciation': [{'IPA': (['[dɐˈbavʲɪtʲ]'], 'ru')}, {'Audio': ('Ru-добавить.ogg', 'Audio', 'ru')}]}}
	),
	("словарь", "Russian", False, False,
		{'Russian': {'Part of Speech': ['Noun'], 'Pronunciation': [{'IPA': (['[slɐˈvarʲ]'], 'ru')}, {'Audio': ('Ru-словарь.ogg', 'audio', 'ru')}]}}
	),
	("индекс", "Russian", False, False,
		{'Russian': {'Part of Speech': ['Noun'], 'Pronunciation': [{'IPA': (['[ˈindɨks]'], 'ru')}, {'Audio': ('Ru-индекс.ogg', 'Audio', 'ru')}]}}
	),
	("индекс", "Russian", False, True,
		{'IPA': ['[ˈindɨks]']}
	),
]

shuffle(TestWord)


class TestWiktionaryMeta(type):
	def __new__(mcs, name, bases, dict):
		
		def gen_test_set_lang(wikidict, lang):
			def test(self):
				if lang is None:
					return self.assertEqual(wikidict.lang, "English")
				wikidict.set_lang(lang)
				return self.assertEqual(wikidict.lang, lang)
			return test
		
		def gen_test_lookup(wikidict, word, lang, CMUBET, phoneme_only, result):
			def test(self):
				text = wikidict.lookup(word, lang=lang, CMUBET=CMUBET, phoneme_only=phoneme_only)
				return self.assertDictEqual(text, result)
			return test
		
		wikidict = Wiktionary()
		
		for i, lang in enumerate(TestLang):
			test_set_lang_name = "test_set_lang_%06d" % i
			dict[test_set_lang_name] = gen_test_set_lang(wikidict, lang)
		
		for i, (word, lang, CMUBET, phoneme_only, result) in enumerate(TestWord):
			test_lookup_name = "test_lookup_%06d" % i
			dict[test_lookup_name] = gen_test_lookup(wikidict, word, lang, CMUBET, phoneme_only, result)
		
		return type.__new__(mcs, name, bases, dict)

class TestWiktionary(with_metaclass(TestWiktionaryMeta, unittest.TestCase)):
	pass


if __name__ == "__main__":
	unittest.main()

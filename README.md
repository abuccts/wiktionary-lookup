wiktionary lookup
=================

[![Build Status](https://travis-ci.org/abuccts/wiktionary-lookup.svg?branch=master)](https://travis-ci.org/abuccts/wiktionary-lookup)
[![GPLv3 licensed](https://img.shields.io/badge/license-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0-standalone.html)

A Python toolkit which looks up given words in [Wiktionary](https://www.wiktionary.org/) and returns structured Python dict format. Support the following list at present,
* languages
* parts of speech
* pronunciations (IPA, CMUBET, enPR, audio link)

Requirements
------------
Written in pure Python, compatible with Python 2 and 3, no dependencies.

Usage
-----
First, create an instance of `Wiktionary` class:
```py
>>> from pywiktionary import Wiktionary
>>> wikidict = Wiktionary(lang="en", CMUBET=True)
```
Lookup a word using `lookup` method:
```py
>>> word = wikidict.lookup("read")
```
The entry of word "read" is at https://en.wiktionary.org/wiki/read, and here is the lookup result:
```py
>>> from pprint import pprint
>>> pprint(word)
{'English': {'Part of Speech': ['Verb', 'Noun'],
             'Pronunciation': [{'CMUBET': ['R IH D .'],
                                'IPA': (['/ɹiːd/'], 'en'),
                                'enPR': 'rēd'},
                               {'Audio': ('En-uk-to read.ogg',
                                          'Audio (UK)',
                                          'en')},
                               {'Audio': ('en-us-read.ogg',
                                          'Audio (US)',
                                          'en')},
                               {'CMUBET': ['R EH D .'],
                                'IPA': (['/ɹɛd/'], 'en'),
                                'enPR': 'rĕd'},
                               {'Audio': ('en-us-read-past.ogg',
                                          'Audio (US)',
                                          'en')}]},
 'Old English': {'Part of Speech': ['Adjective'],
                 'Pronunciation': [{'CMUBET': ['AE AA D .'],
                                    'IPA': (['/ˈræːɑd/'], 'ang')}]},
 'Swedish': {'Part of Speech': ['Verb']},
 'West Frisian': {'Part of Speech': ['Adjective']}}
```

More exmaples can be found at [Example Wiki Page](https://github.com/abuccts/wiktionary-lookup/wiki/Example).

# Command-line usage

The binary wiktionary is provided

```
# Show human readable information
wiktionary cat

# Output information for all languages
wiktionary --language all cat

# Output machine readable output - suitable for parsing
wiktionary --json cat
```

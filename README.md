wiktionary lookup
=================

[![Build Status](https://travis-ci.org/abuccts/wiktionary-lookup.svg?branch=master)](https://travis-ci.org/abuccts/wiktionary-lookup)
[![Coverage Status](https://coveralls.io/repos/github/abuccts/wiktionary-lookup/badge.svg?branch=master)](https://coveralls.io/github/abuccts/wiktionary-lookup?branch=master)
[![GPLv3 licensed](https://img.shields.io/badge/license-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0-standalone.html)

A Python toolkit which looks up given words in [Wiktionary](https://www.wiktionary.org/) and returns structured Python dict format. Support the following list at present,
* languages
* parts of speech
* pronunciations (IPA, CMUBET, enPR, audio link)

Requirements
------------
Written in pure Python, compatible with Python 2.6+ and 3.2+, no dependencies.

Installation
------------
```sh
# download the latest version
$ git clone https://github.com/abuccts/wiktionary-lookup.git
$ cd wiktionary-lookup

# install and run test
$ python setup.py install
$ python setup.py -q test
```

Usage
-----
First, create an instance of `Wiktionary` class:
```py
>>> from pywiktionary import Wiktionary
>>> wikidict = Wiktionary(lang="English", CMUBET=True, phoneme_only=False)
```
Lookup a word using `lookup` method:
```py
>>> word = wikidict.lookup("read")
```
The entry of word "read" is at https://en.wiktionary.org/wiki/read#English, and here is the lookup result:
```py
>>> from pprint import pprint
>>> pprint(word)
{'English': {'Part of Speech': ['Verb', 'Noun'],
             'Pronunciation': [{'CMUBET': ['R IY D .'],
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
                                          'en')}]}}
```
To lookup a word in a different language, specify the `lang` parameter (`CMUBET` parameter is only available for `lang="English"` at present):
```py
>>> word = wikidict.lookup("читать", lang="Russian")
>>> pprint(word)
{'Russian': {'Part of Speech': ['Verb'],
             'Pronunciation': [{'IPA': (['[t͡ɕɪˈtatʲ]'], 'ru')},
                               {'Audio': ('Ru-читать.ogg', 'Audio', 'ru')}]}}
```
Please note that the default language of `wikidict` is `"English"` which is set when the instance is created. To change the language of `wikidict` permanently, create another instance of `Wiktionary` class or use `set_lang` function:
```py
>>> wikidict.set_lang("French")
>>> word = wikidict.lookup("être")
>>> pprint(word)
{'French': {'Part of Speech': ['Verb', 'Noun'],
            'Pronunciation': [{'IPA': (['/ɛtʁ/'], 'fr')},
                              {'Audio': ('Fr-être-fr-ouest.ogg',
                                         'Audio (France, West)',
                                         'fr')},
                              {'Accent': 'Quebec', 'IPA': (['[aɛ̯tʁ]'], 'fr')},
                              {'Audio': ('Qc-être.ogg',
                                         'Audio (Quebec, Montreal)',
                                         'fr')},
                              {'Accent': 'Louisiana',
                               'IPA': (['[ɛt(ɾ)]'], 'fr')}]}}
```
For phoneme only output without other information, set `phoneme_only` parameter to `True`:
```py
>>> word_phoneme = wikidict.lookup("être", phoneme_only=True)
>>> pprint(word_phoneme)
{'IPA': ['/ɛtʁ/', '[aɛ̯tʁ]', '[ɛt(ɾ)]']}

```

More exmaples of different languages can be found at [Example Index Wiki Page](https://github.com/abuccts/wiktionary-lookup/wiki/Example%20Index).


For command line interface, please refer to [Command Line Usage Wiki Page](https://github.com/abuccts/wiktionary-lookup/wiki/Command-Line-Usage).


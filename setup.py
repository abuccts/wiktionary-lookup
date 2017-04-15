#! /usr/bin/env python
# -*- coding: utf-8  -*-

import sys

if ((sys.version_info[0] == 2 and sys.version_info[1] < 6) or
	(sys.version_info[1] == 3 and sys.version_info[1] < 2)):
	raise RuntimeError("Python 2.6+ or 3.2+ needed.")

py26 = (sys.version_info[0] == 2 and sys.version_info[1] == 6)

from setuptools import setup, find_packages
from pywiktionary import __version__

setup(
	name = "pywiktionary",
	packages = find_packages(exclude=("tests",)),
	tests_require = ["six", "unittest2"] if py26 else ["six"],
	test_suite = "tests",
	version = __version__,
	author = "abuccts",
	author_email = "abuccts@gmail.com",
	url = "https://github.com/abuccts/wiktionary-lookup",
	description = "lookup words and pronunciations in Wiktionary",
	keywords = "pywiktionary wiktionary wiktionary-lookup parse pronunciation",
	license = "GPLv3",
	entry_points = {
		"console_scripts": ["wiktionary=pywiktionary.cli:cli"]
	},
	classifiers=[
		"Development Status :: 2 - Pre-Alpha",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: BSD License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.2",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
	],
)

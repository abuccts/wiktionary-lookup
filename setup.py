#! /usr/bin/env python
# -*- coding: utf-8  -*-

from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
	name = "pywiktionary",
	packages = find_packages(exclude=("tests",)),
	tests_require = ["unittest2"] if (sys.version_info[:2] == [2, 6]) else [],
	test_suite = "tests",
	version = "0.0.1",
	author = "abuccts",
	author_email = "abuccts@gmail.com",
	url = "https://github.com/abuccts/wiktionary-lookup",
	description = "lookup words and pronunciations in Wiktionary",
	keywords = "pywikitionary wiktionary-lookup wiktionary parse pronunciation",
	license = "GPLv3",
	entry_points = {
		"console_scripts": ["wiktionary=pywiktionary.wiktionary:cli"]
	},
	classifiers=[
		"Development Status :: 1 - Planning",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent"
	],
)

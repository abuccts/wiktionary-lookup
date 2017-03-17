# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

try:
	import unittest2 as unittest
except ImportError:
	import unittest
from subprocess import check_output


usage = """usage: wiktionary [-h] [--language LANGUAGE] [--json] word

Fetch information from wikitionary

positional arguments:
  word

optional arguments:
  -h, --help           show this help message and exit
  --language LANGUAGE  Display entry for this language (the default is
                       English)
  --json               Output in machine readable json. This may contain
                       additional information.
"""

result = """English
    RP
        /kæt/
        /kat/
        [kʰat]
        [kʰaʔ]
    GenAm
        /kæt/
        [kʰæt]
        [kʰæʔ]
        [kʰeə̯t̚]
        [kʰæt̚]
        [kʰæʔt̚]
"""


class TestCLI(unittest.TestCase):
	def test_cli(self):
		self.assertEqual(check_output(["wiktionary", "-h"], universal_newlines=True), usage)
#		self.assertEqual(check_output(["wiktionary", "cat"]).decode("utf-8").splitlines(), result.splitlines())
#		self.assertEqual(check_output(["wiktionary", "--language", "English", "cat"]).decode("utf-8").splitlines(), result.splitlines())

if __name__ == "__main__":
	unittest.main()

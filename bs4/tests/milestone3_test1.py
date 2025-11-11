import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer


class TestNameXformerBasicM3(unittest.TestCase):
    def test_name_xformer_basic(self):
        """replace b with strong using name transformer"""
        html_doc = """
        <html>
        <body>
        <b>This is bold text</b>
        <p>This is a paragraph</p>
        <b>Another bold text</b>
        </body>
        </html>
        """

        b_to_strong = SoupReplacer(
            name_xformer=lambda tag: "strong" if tag.name == "b" else tag.name
        )
        soup = BeautifulSoup(html_doc, "html.parser", replacer=b_to_strong)

        # Check that b tags got replaced
        self.assertEqual(len(soup.find_all("b")), 0)
        self.assertEqual(len(soup.find_all("strong")), 2)

        strongs = soup.find_all("strong")
        self.assertEqual(strongs[0].string, "This is bold text")
        self.assertEqual(strongs[1].string, "Another bold text")


if __name__ == "__main__":
    unittest.main()

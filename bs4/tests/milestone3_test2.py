import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer


class TestNameXformerMultipleReplacementsM3(unittest.TestCase):
    def test_name_xformer_multiple_replacements(self):
        """Can handle multiple different tag types at once"""
        html_doc = """
        <div>
        <b>Bold</b>
        <i>Italic</i>
        <u>Underline</u>
        </div>
        """

        def multi_transform(tag):
            transforms = {"b": "strong", "i": "em", "u": "ins"}
            return transforms.get(tag.name, tag.name)

        replacer = SoupReplacer(name_xformer=multi_transform)
        soup = BeautifulSoup(html_doc, "html.parser", replacer=replacer)

        # Old tags should all be gone
        self.assertEqual(len(soup.find_all("b")), 0)
        self.assertEqual(len(soup.find_all("i")), 0)
        self.assertEqual(len(soup.find_all("u")), 0)

        # Should have the new ones instead
        self.assertEqual(len(soup.find_all("strong")), 1)
        self.assertEqual(len(soup.find_all("em")), 1)
        self.assertEqual(len(soup.find_all("ins")), 1)


if __name__ == "__main__":
    unittest.main()

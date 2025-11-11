import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer


class TestCombinedNameAndAttrsXformerM3(unittest.TestCase):
    def test_combined_name_and_attrs_xformer(self):
        """Using both name and attrs transformers together"""
        html_doc = """
        <div class="old">
        <b class="highlight">Bold text</b>
        </div>
        """

        def rename_b_tags(tag):
            return "strong" if tag.name == "b" else tag.name

        def add_data_attr(tag):
            attrs = tag.attrs.copy()
            attrs["data-transformed"] = "true"
            return attrs

        replacer = SoupReplacer(
            name_xformer=rename_b_tags,
            attrs_xformer=add_data_attr
        )
        soup = BeautifulSoup(html_doc, "html.parser", replacer=replacer)

        # b should be renamed to strong
        self.assertEqual(len(soup.find_all("b")), 0)
        strong = soup.find("strong")
        self.assertIsNotNone(strong)

        # All tags should have data-transformed attribute
        div = soup.find("div")
        self.assertEqual(div.get("data-transformed"), "true")
        self.assertEqual(strong.get("data-transformed"), "true")


if __name__ == "__main__":
    unittest.main()

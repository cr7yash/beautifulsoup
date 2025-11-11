import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer


class TestAllThreeTransformersM3(unittest.TestCase):
    def test_all_three_transformers(self):
        """All three transformers working together"""
        html_doc = "<div><b class='bold' style='color: red;'>Bold text</b><i class='italic'>Italic text</i></div>"

        def rename_tags(tag):
            return "strong" if tag.name == "b" else tag.name

        def modify_attrs(tag):
            attrs = tag.attrs.copy()
            attrs["data-modified"] = "yes"
            return attrs

        def remove_style(tag):
            if "style" in tag.attrs:
                del tag.attrs["style"]

        replacer = SoupReplacer(
            name_xformer=rename_tags,
            attrs_xformer=modify_attrs,
            xformer=remove_style
        )
        soup = BeautifulSoup(html_doc, "html.parser", replacer=replacer)

        # b should be renamed to strong
        strong = soup.find("strong")
        self.assertIsNotNone(strong)
        self.assertEqual(strong.string, "Bold text")

        # Should have data-modified attribute
        self.assertEqual(strong.get("data-modified"), "yes")

        # Should not have style attribute
        self.assertIsNone(strong.get("style"))

        # class should be preserved (not removed by xformer)
        self.assertIn("bold", strong.get("class", []))


if __name__ == "__main__":
    unittest.main()

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer


class TestXformerRemoveAttributeM3(unittest.TestCase):
    def test_xformer_remove_attribute(self):
        """Test removing attributes with xformer"""
        html_doc = """
        <div class="container" id="main">
        <p class="text">Content</p>
        <span id="span1" class="highlight">Highlight</span>
        </div>
        """

        def remove_class_attr(tag):
            if "class" in tag.attrs:
                del tag.attrs["class"]

        class_deleter = SoupReplacer(xformer=remove_class_attr)
        soup = BeautifulSoup(html_doc, "html.parser", replacer=class_deleter)

        # All class attributes should be removed
        div = soup.find("div")
        p = soup.find("p")
        span = soup.find("span")

        self.assertIsNone(div.get("class"))
        self.assertIsNone(p.get("class"))
        self.assertIsNone(span.get("class"))

        # Other attributes should remain
        self.assertEqual(div.get("id"), "main")
        self.assertEqual(span.get("id"), "span1")


if __name__ == "__main__":
    unittest.main()

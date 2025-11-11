import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer


class TestAttrsXformerBasicM3(unittest.TestCase):
    def test_attrs_xformer_basic(self):
        """Test modifying attributes"""
        html_doc = """
        <div class="old-class" id="myid">
        <p class="another-class">Text</p>
        </div>
        """

        def update_classes(tag):
            if "class" in tag.attrs:
                # Replace old-class with new-class
                classes = tag.attrs["class"]
                if "old-class" in classes:
                    classes = ["new-class" if c == "old-class" else c for c in classes]
                    return {**tag.attrs, "class": classes}
            return tag.attrs

        replacer = SoupReplacer(attrs_xformer=update_classes)
        soup = BeautifulSoup(html_doc, "html.parser", replacer=replacer)

        div = soup.find("div")
        self.assertIn("new-class", div.get("class", []))
        self.assertNotIn("old-class", div.get("class", []))
        self.assertEqual(div.get("id"), "myid")  # Other attrs preserved


if __name__ == "__main__":
    unittest.main()

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer


class TestMilestone3(unittest.TestCase):
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
        self.assertIsNone(soup.find("div").get("class"))
        self.assertIsNone(soup.find("p").get("class"))
        self.assertIsNone(soup.find("span").get("class"))

        # Other attributes should remain
        self.assertEqual(soup.find("div").get("id"), "main")
        self.assertEqual(soup.find("span").get("id"), "span1")

    def test_combined_name_and_attrs_xformer(self):
        """Using both name and attrs transformers together"""
        html_doc = '<div class="old"><b class="highlight">Bold text</b></div>'

        replacer = SoupReplacer(
            name_xformer=lambda t: "strong" if t.name == "b" else t.name,
            attrs_xformer=lambda t: {**t.attrs, "data-transformed": "true"}
        )
        soup = BeautifulSoup(html_doc, "html.parser", replacer=replacer)

        self.assertIsNone(soup.find("b"))
        strong = soup.find("strong")
        self.assertIsNotNone(strong)
        self.assertEqual(strong.get("data-transformed"), "true")
        self.assertEqual(soup.find("div").get("data-transformed"), "true")

    def test_all_three_transformers(self):
        """All three transformers working together"""
        html_doc = "<div><b class='bold' style='color: red;'>Bold text</b><i class='italic'>Italic text</i></div>"

        def remove_style(tag):
            if "style" in tag.attrs: del tag.attrs["style"]

        replacer = SoupReplacer(
            name_xformer=lambda t: "strong" if t.name == "b" else t.name,
            attrs_xformer=lambda t: {**t.attrs, "data-modified": "yes"},
            xformer=remove_style
        )
        soup = BeautifulSoup(html_doc, "html.parser", replacer=replacer)

        strong = soup.find("strong")
        self.assertIsNotNone(strong)
        self.assertEqual(strong.get("data-modified"), "yes")
        self.assertIsNone(strong.get("style"))
        self.assertIn("bold", strong.get("class", []))


if __name__ == "__main__":
    unittest.main()
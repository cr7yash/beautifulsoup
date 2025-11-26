import unittest
from bs4 import BeautifulSoup, SoupReplacer


class TestSoupReplacerSimple(unittest.TestCase):
    def test_html_tag_replacement(self):
        """
        Test replacing <b> tags with <blockquote> in an HTML document.
        """
        html_doc = """
            <html>
            <body>
            <b>This is bold text</b>
            <p>This is a paragraph</p>
            <b>Another bold text</b>
            </body>
            </html>
        """
        b_to_blockquote = SoupReplacer("b", "blockquote")
        soup = BeautifulSoup(html_doc, "html.parser", replacer=b_to_blockquote)

        self.assertEqual(len(soup.find_all("b")), 0)
        self.assertEqual(len(soup.find_all("blockquote")), 2)
        self.assertEqual(soup.blockquote.string, "This is bold text")

    def test_xml_tag_replacement(self):
        """
        Test replacing <item> tags with <entry> in an XML document.
        """
        xml_doc = """
            <root>
                <item>First item</item>
                <content>Some content here</content>
                <item>Second item</item>
                <data>
                    <item>Nested item</item>
                </data>
            </root>
        """
        item_to_entry = SoupReplacer("item", "entry")
        soup = BeautifulSoup(xml_doc, "xml", replacer=item_to_entry)

        self.assertEqual(len(soup.find_all("item")), 0)
        self.assertEqual(len(soup.find_all("entry")), 3)
        self.assertEqual(soup.entry.string, "First item")

if __name__ == "__main__":
    unittest.main()

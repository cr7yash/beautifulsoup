import sys
import os

# Add the local beautifulsoup package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer

# Test XML-style tag replacement
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

# Replace <item> tags with <entry> tags
item_to_entry = SoupReplacer("item", "entry")
print(BeautifulSoup(xml_doc, "xml", replacer=item_to_entry).prettify())

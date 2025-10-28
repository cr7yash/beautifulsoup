import sys
import os

# Add the local beautifulsoup package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer

# Test example from requirements
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
print(BeautifulSoup(html_doc, replacer=b_to_blockquote).prettify())

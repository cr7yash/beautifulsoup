from bs4 import BeautifulSoup, SoupStrainer
import sys

link_strainer = SoupStrainer('a')

with open(sys.argv[1], 'r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser", parse_only=link_strainer).prettify()
print(soup)

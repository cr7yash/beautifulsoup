from bs4 import BeautifulSoup, SoupStrainer
import sys

# SoupStrainer that matches tags with id attribute
id_strainer = SoupStrainer(attrs={'id': True})

with open(sys.argv[1], 'r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser", parse_only=id_strainer)

for tag in soup.find_all():
    print(tag)

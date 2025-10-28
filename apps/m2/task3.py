from bs4 import BeautifulSoup, SoupStrainer
import sys

all_tags_strainer = SoupStrainer(True)

with open(sys.argv[1], 'r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser", parse_only=all_tags_strainer)

for tag in soup.find_all():
    print(tag.name)
 
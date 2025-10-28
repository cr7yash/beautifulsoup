import sys, os

# Add the local beautifulsoup package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bs4 import BeautifulSoup, SoupReplacer

with open(sys.argv[1], 'r') as my_file:
    xml_file = my_file.read()
    
b_to_blockquote = SoupReplacer("b", "blockquote")

soup = BeautifulSoup(xml_file, 'html.parser', replacer=b_to_blockquote)
    
base_filename = os.path.basename(sys.argv[1])
output_filename = f"transformed_{base_filename}"

with open(output_filename, 'w', encoding='utf-8') as output_file:
    output_file.write(str(soup))

print("completed")
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from bs4 import BeautifulSoup, SoupReplacer

def add_class_to_p_tags(tag):
    if tag.name == 'p':
        new_attrs = dict(tag.attrs)
        new_attrs['class'] = ['test']
        return new_attrs
    return tag.attrs

with open(sys.argv[1], 'r') as my_file:
    xml_file = my_file.read()

replacer = SoupReplacer(attrs_xformer=add_class_to_p_tags)

soup = BeautifulSoup(xml_file, 'html.parser', replacer=replacer)

base_filename = os.path.basename(sys.argv[1])
output_filename = f"transformed_task7_{base_filename}"

with open(output_filename, 'w', encoding='utf-8') as output_file:
    output_file.write(str(soup))


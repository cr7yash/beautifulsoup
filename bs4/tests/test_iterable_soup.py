from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype, NavigableString

from . import SoupTest

class TestIterableSoupSimple(SoupTest):
    def test_empty(self):
        soup = self.soup("")
        assert list(iter(soup)) == []

    def test_single_tag(self):
        soup = self.soup("<a></a>")
        nodes = list(iter(soup))
        # only the <a> tag should appear
        assert len(nodes) == 1
        assert getattr(nodes[0], "name", None) == "a"

    def test_nested(self):
        soup = self.soup("<a><b></b></a>")
        names = [getattr(n, "name", None) for n in iter(soup) if getattr(n, "name", None)]
        assert names == ["a", "b"]

    def test_text_and_tags(self):
        soup = self.soup("<div>hi<span>there</span></div>")
        seq = list(iter(soup))
        # expect: div tag, 'hi', span tag, 'there'
        assert hasattr(seq[1], "startswith") and str(seq[1]).startswith("hi")
        assert getattr(seq[2], "name", None) == "span"

    def test_comment_and_doctype(self):
        soup = self.soup("<!DOCTYPE html><!--x--><p>y</p>")
        seq = list(iter(soup))
        assert any(isinstance(n, Doctype) for n in seq)
        assert any(isinstance(n, Comment) for n in seq)

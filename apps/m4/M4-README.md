Iterable BeautifulSoup — Technical brief (root included)

Overview
--------
`BeautifulSoup` now implements the iterator. That means you can write `for node in soup:` and receive every node in the document tree one at a time. The change was implemented to make full-tree traversal.

Behavior
----------------------
 - Iteration over a `BeautifulSoup` instance yields every `PageElement` (tags, strings, comments, doctypes, etc.) encountered in the document, and it includes the `BeautifulSoup` root object itself (equivalent to `soup.self_and_descendants`).

Examples
--------
Simple traversal:

```
from bs4 import BeautifulSoup

soup = BeautifulSoup('<!DOCTYPE html><!--x--><div>foo<span>bar</span></div>', 'html.parser')
for node in soup:
	print(type(node), repr(node))
```


Compatibility and migration notes
--------------------------------
- Prior to this change `BeautifulSoup` inherited `Tag.__iter__` which iterated direct children. That behavior is unchanged for `Tag` objects. The new `BeautifulSoup.__iter__` provides full-tree iteration and therefore is different from the old inherited behavior. Code that relied on `iter(soup)` producing only direct children should be updated to use `soup.children`.

Implementation notes
--------------------
- The implementation makes `BeautifulSoup` itself iterable by providing
	`__iter__` which returns the `self_and_descendants` generator. That means
	`iter(soup)` yields the root followed by every descendant node.
- Internally, `self_and_descendants` calls `_self_and(self.descendants)`, and
	`descendants` is a generator that walks the tree using `next_element` links
	and `yield`, so nodes are produced lazily and no list is materialized.

API summary
-----------
- `iter(soup)` — yields all descendant nodes.
- `soup.descendants` — existing property; unchanged and still available as a generator.
- `soup.children` — yields direct children only.


# Week-6

### Usage
```bash
python task7_soupreplacer.py ../<input-file-name>
```


# Technical Brief: Milestone 2 vs. Milestone 3

## Summary

This brief analyzes two approaches to the SoupReplacer API for BeautifulSoup: the simple tag replacement API from Milestone 2 versus the transformer-based API introduced in Milestone 3. Both APIs enable tag transformation during HTML/XML parsing, but they differ in features, ease of use, and use cases.

## API Comparison

### Milestone 2 API: Simple Tag Replacement

```python
# Constructor
SoupReplacer(og_tag: str, alt_tag: str)

# Usage
replacer = SoupReplacer("b", "strong")
soup = BeautifulSoup(html_doc, replacer=replacer)
```

**Capabilities:**
- Replace all instances of one tag name with another
- Case-insensitive tag matching
- Works during parsing (single pass)

**Limitations:**
- Only supports one-to-one tag name replacement
- Cannot modify attributes
- Cannot apply conditional logic
- Cannot perform side effects
- No support for complex transformations

### Milestone 3 API: Transformer-Based Replacement

```python
# Constructor
SoupReplacer(
    name_xformer: Optional[Callable[[Tag], str]] = None,
    attrs_xformer: Optional[Callable[[Tag], dict]] = None,
    xformer: Optional[Callable[[Tag], None]] = None
)

# Usage Examples
# 1. Name transformation with logic
replacer = SoupReplacer(
    name_xformer=lambda tag: "strong" if tag.name == "b" else tag.name
)

# 2. Attribute modification
replacer = SoupReplacer(
    attrs_xformer=lambda tag: {**tag.attrs, "data-processed": "true"}
)

# 3. Side effects (e.g., removing attributes)
replacer = SoupReplacer(
    xformer=lambda tag: tag.attrs.pop("style", None)
)

# 4. All three combined
replacer = SoupReplacer(
    name_xformer=modernize_tag,
    attrs_xformer=add_classes,
    xformer=remove_styles
)
```

**Capabilities:**
- **name_xformer**: Transform tag names with arbitrary logic
- **attrs_xformer**: Modify or replace tag attributes
- **xformer**: Perform side effects (add/remove attributes, etc.)
- All transformations happen during parsing.
- Can combine multiple transformers.
- Supports conditional logic and complex transformations.
- Full access to tag context (name, attributes, etc.)

**Limitations:**
- More complex implementation
- Requires tracking original tag names for proper closing
- Modified parser state machine to handle transformed tags

---

## Detailed Analysis

### 1. Features

**Milestone 2**: Limited to simple string replacement
```python
# Can only do this:
SoupReplacer("b", "strong")

# Cannot do:
# - Conditional replacements
# - Attribute modifications
# - Multiple tag types at once
```

**Milestone 3**: Full programmatic control
```python
# Conditional replacement based on tag state
name_xformer=lambda tag: "strong" if tag.name == "b" and "class" not in tag.attrs else tag.name

# Complex attribute transformations
attrs_xformer=lambda tag: {
    k: v for k, v in tag.attrs.items()
    if k not in ['style', 'color', 'bgcolor']
}

# Multiple transformations in one pass
SoupReplacer(name_xformer=f1, attrs_xformer=f2, xformer=f3)
```


### 2. Ease of Use

**Milestone 2**: Extremely simple
```python
replacer = SoupReplacer("b", "strong")  # Clear and concise
```

**Milestone 3**: Requires function definitions
```python
def transform_name(tag):
    if tag.name == "b":
        return "strong"
    return tag.name

replacer = SoupReplacer(name_xformer=transform_name)
```


### 3. Use Cases

**Milestone 2 is ideal for**:
- Quick tag renaming (e.g., `<b>` → `<strong>`)
- Batch processing with simple rules
- Users who want minimal configuration

**Milestone 3 is ideal for**:
- Preprocessing for frameworks like reactjs (add data attributes)
- Complex transformation 
- Programmatic HTML manipulation

---

Both APIs have :

- **Milestone 2**: Simplicity for common cases
- **Milestone 3**: Powerful flexibility for complex transformations

The implementation successfully maintains both APIs with clear separation of modes. The added complexity of Milestone 3 is justified by its expanded capabilities.

The transformer API represents a significant advancement in BeautifulSoup's capabilities, enabling use cases that were previously impossible or required post-processing.

---


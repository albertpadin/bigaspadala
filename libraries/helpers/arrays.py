import textwrap


def chunk_text(text, size=300, break_long_words=True):
    """
    Returns an array of strings based on a given number of character.
    >>> chunk_text("the quick brown fox jumps over the lazy dog", size=5, break_long_words=True)
    ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
    """
    text_chunks = textwrap.wrap(
        text.encode('utf-8'),
        size,
        break_long_words=break_long_words
    )

    return text_chunks

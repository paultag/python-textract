import pytest

from textract.core import Textract


data = [
    ["name", "1111", "legal", "Joe", "Smith"],
    ["name", "1111", "alias", "Jose", "Smithe"],
    ["name", "1112", "alias", "Jose", "Smith"],
]


t = Textract()

class Name(object):
    def __init__(self, entry=None, type_=None, given=None, family=None):
        self.entry = entry
        self.type = type_
        self.given = given
        self.family = family


@t.handle("name")
def foo(entry, type_, given, family):
    return Name(type_=type_, entry=entry, given=given, family=family)


def test_grouper():
    entries = t.entries(data)
    a = next(entries)
    assert len(a.attributes) == 2
    legal, alias = a.attributes

    assert legal.given == "Joe"
    assert legal.family == "Smith"
    assert legal.type == "legal"

    assert alias.given == "Jose"
    assert alias.family == "Smithe"
    assert alias.type == "alias"

    a = next(entries)
    assert len(a.attributes) == 1
    alias, = a.attributes
    assert alias.given == "Jose"
    assert alias.family == "Smith"
    assert alias.type == "alias"

    with pytest.raises(StopIteration):
        next(entries)

import pytest

from textract.core import Textract


data = [
    ["name", "1111", "legal", "Joe", "Smith"],
    ["name", "1111", "alias", "Jose", "Smithe"],
    ["name", "1112", "alias", "Jose", "Smith"],
    ["star", "1112", "gold"],
]


t = Textract()

class Name(object):
    def __init__(self, entry=None, type_=None, given=None, family=None):
        self.entry = entry
        self.type = type_
        self.given = given
        self.family = family

class Star(object):
    def __init__(self, entry=None, type_=None):
        self.entry = entry
        self.type = type_


@t.handle("star")
def star(entry, type_):
    return Star(entry=entry, type_=type_)


@t.handle("name")
def foo(entry, type_, given, family):
    return Name(type_=type_, entry=entry, given=given, family=family)


def test_grouper():
    entries = t.entries(data)
    entities = list(entries)
    assert len(entities) == 2
    one, two = entities

    assert len(one.attributes) == 2
    assert len(two.attributes) == 2

    joe, jose = one.attributes
    assert joe.given == "Joe"
    assert jose.given == "Jose"


def test_filter():
    entries = t.entries(data)
    entities = list(entries)
    assert len(entities) == 2
    one, two = entities

    assert len(list(one.attributes)) == 2
    assert len(list(one.attributes.by_type(Name))) == 2

    assert len(list(two.attributes)) == 2
    assert len(list(two.attributes.by_type(Name))) == 1
    assert len(list(two.attributes.by_type(Star))) == 1

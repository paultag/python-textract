class Attributes(list):
    def by_type(self, class_):
        return filter(lambda x: isinstance(x, class_), self)


class Entry(object):
    def __init__(self, id):
        self.id = id
        self.attributes = Attributes()

    def __str__(self):
        return "<Entry: {id}>".format(id=self.id)

    @classmethod
    def from_attribute(self, attribute):
        e = Entry(id=attribute.entry)
        e.add(attribute)
        return e

    def add(self, attribute):
        self.attributes.append(attribute)


class Textract(object):
    def __init__(self):
        self.handlers = {}

    def handle(self, key):
        def decorator(fn):
            self.handlers[key] = fn
            return fn
        return decorator

    def process_row(self, row):
        entry = self.handlers[row[0]](*row[1:])
        if not hasattr(entry, "entry"):
            raise AttributeError("Type '{}' has no attribute 'entry'".format(
                entry.__class__))
        return entry

    def process_rows(self, rows):
        for row in rows:
            yield self.process_row(row)

    def entries(self, rows):
        rows = self.process_rows(rows)
        entry = Entry.from_attribute(next(rows))
        for attribute in rows:
            if attribute.entry == entry.id:
                entry.add(attribute)
                continue
            yield entry
            entry = Entry.from_attribute(attribute)
        yield entry

    def populate(self, constructor, rows):
        for entry in self.entries(rows):
            yield constructor(entry)
